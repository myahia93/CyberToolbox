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

    # Run Nikto scan
    try:
        result = subprocess.run(
            nikto_command, check=False, capture_output=True, text=True)
        nikto_output = result.stdout
        nikto_errors = result.stderr

        # Print errors if any
        if nikto_errors:
            print("\033[91mErrors occurred during the Nikto scan:\033[0m")
            print(nikto_errors)

        # Process Nikto output
        process_nikto_output(nikto_output)

    except subprocess.CalledProcessError as e:
        print(f"\033[91mAn error occurred: {e}\033[0m")
        # Continue processing the Nikto output even if an error occurs
        process_nikto_output(e.stdout)


def process_nikto_output(nikto_output):
    # Split the Nikto output into sections
    sections = nikto_output.split("\n\n")

    # Create a PrettyTable instance
    table = PrettyTable()

    # Define table headers
    table.field_names = ["ID", "Description", "Impact", "URL"]

    # Iterate through sections and parse relevant information
    for section in sections:
        lines = section.split("\n")
        if lines and lines[0].startswith("ID"):
            # Parse relevant information from the section
            info = lines[0].split(" - ")
            if len(info) == 2:
                id, description = info
            else:
                id, description = info[0], " ".join(info[1:])
            impact = lines[1][8:] if len(lines) > 1 else ""
            url = lines[-1][5:] if len(lines) > 2 else ""

            # Add row to the PrettyTable
            table.add_row([id, description, impact, url])

    # Set column alignments
    table.align["ID"] = "l"
    table.align["Description"] = "l"
    table.align["Impact"] = "l"
    table.align["URL"] = "l"

    # Print the PrettyTable
    print(table)


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
