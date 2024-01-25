import ipaddress
import os
from urllib.parse import urlparse
from prettytable import PrettyTable
from termcolor import colored


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


def perform_nikto_check(url):
    loading_message = "\nRunning Nikto scan. This may take a few minutes..."
    print(colored(loading_message, "purple"))

    # Build Nikto command
    nikto_command = f"nikto -h {url}"

    # Execute Nikto command and capture output
    nikto_output = os.popen(nikto_command).read()

    # Display Nikto results in a PrettyTable
    display_nikto_results(nikto_output)


def display_nikto_results(nikto_output):
    # Check if Nikto reported any errors
    if "+ ERROR:" in nikto_output:
        print(colored("\nNikto encountered errors:", "red"))
        print(nikto_output)
        return

    # Check if any host was found
    if "0 host(s) tested" in nikto_output:
        print(colored("\nNo host found.", "red"))
        return

    # Create a PrettyTable
    table = PrettyTable()
    table.field_names = ["Host", "Port", "Server", "Vulnerabilities"]

    # Parse Nikto output and populate PrettyTable
    lines = nikto_output.split("\n")
    for line in lines:
        if line.startswith("+ Target IP:"):
            host_ip = line.split(":")[1].strip()
        elif line.startswith("+ Target Port:"):
            port = line.split(":")[1].strip()
        elif line.startswith("+ Server:"):
            server = line.split(":")[1].strip()
        elif line.startswith("+") and not line.startswith("+ ERROR:"):
            vulnerability = line[1:].strip()
            table.add_row([host_ip, port, server, vulnerability])

    # Check if any vulnerabilities were found
    if table.rowcount == 0:
        print(colored("\nNo vulnerabilities found.", "green"))
        return

    # Print the PrettyTable with colored headers
    print(colored("\nNikto Scan Results", "blue"))
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
