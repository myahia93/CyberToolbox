import ipaddress
import subprocess
from urllib.parse import urlparse
from prettytable import PrettyTable


def check_target_validity():
    while True:
        # Ask the user to enter a target (URL or IP)
        target = input(
            "\n\033[92mEnter the target (URL or IP) to check: \033[0m")

        try:
            # Try to parse as an IP address
            ipaddress.IPv4Address(target)
            return target

        except ipaddress.AddressValueError:
            # If it's not a valid IP, check if it's a valid URL
            try:
                parsed_url = urlparse(target)
                if parsed_url.scheme and parsed_url.netloc:
                    return target
                else:
                    print(
                        "\033[91mInvalid URL. Please enter a valid URL.\033[0m")

            except ValueError:
                print(
                    "\033[91mInvalid target. Please enter a valid URL or IP address.\033[0m", end='')
                print()


def perform_nikto_check(target):
    print("\n\033[1;35mRunning Nikto scan. This may take a few minutes...\033[0m")

    # Prepare Nikto command
    nikto_command = ["nikto", "-h", target]

    # Check if target starts with "https" and add "-ssl" option accordingly
    if target.startswith("https"):
        nikto_command.append("-ssl")

    # Run Nikto scan and capture the output
    try:
        process = subprocess.Popen(
            nikto_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Variables to store the information
        basic_info = []
        vuln_info = []

        # Process each line of the output in real-time
        for line in iter(process.stdout.readline, ''):
            # Print the line in real-time
            print(line.strip())

            # Check for the start of basic information
            if line.startswith("+ Target"):
                basic_info.append(line.strip())

            # Check for the start of vulnerability information
            elif line.startswith("+ "):
                vuln_info.append(line.strip())

        # Wait for the process to finish
        process.communicate()

        # Print basic information
        print("\n\033[1;35mBasic Information:\033[0m")
        for info in basic_info:
            print(info)

        # Print table with vulnerabilities
        if vuln_info:
            print("\n\033[1;35mVulnerabilities:\033[0m")
            vuln_table = PrettyTable(["ID", "Description", "Impact", "URL"])
            for info in vuln_info:
                _, vuln_id, vuln_desc, vuln_impact, vuln_url = info.split(
                    "|", 4)
                vuln_table.add_row(
                    [vuln_id.strip(), vuln_desc.strip(), vuln_impact.strip(), vuln_url.strip()])
            print(vuln_table)

    except subprocess.CalledProcessError as e:
        # Handle errors without printing them
        print("\033[1;31mError during Nikto scan:\033[0m", e)


def display_nikto_description():
    nikto_description = """
    
    \033[1;35m
    Nikto is an open-source web server scanner that performs comprehensive tests against web servers for multiple items,
    including over 6700 potentially dangerous files/CGIs, outdated versions of over 1250 servers, and version-specific problems
    on over 270 servers. Nikto's focus is to find various default and insecure files, configurations, and programs on web servers.
    
    Key Features:
    - Extensive tests: Nikto performs a wide range of tests to identify potential vulnerabilities in web servers.
    - SSL support: Nikto supports scanning web servers over SSL.
    - Multiple plugins: Nikto has a modular architecture and supports multiple plugins to extend its capabilities.
    - Comprehensive reports: Nikto provides detailed reports of the scan results, aiding in vulnerability analysis.

    In \033[0;31mCyberToolbox\033[1;35m, Nikto is integrated to facilitate the identification of potential vulnerabilities in web servers.
    The simplified interface allows users to perform web server vulnerability checks quickly and efficiently.

    Note: Nikto should be used responsibly and with proper authorization. Unauthorized use of Nikto against
    systems for which you do not have explicit permission is illegal and unethical.\033[0m

    """

    print(nikto_description)
