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
    print(
        "\n\033[1;35mRunning Nikto scan. This may take a few minutes...\n\033[0m")

    # Prepare Nikto command
    nikto_command = ["nikto", "-h", target]

    # Check if target starts with "https" and add "-ssl" option accordingly
    if target.startswith("https"):
        nikto_command.append("-ssl")

    # Run Nikto scan
    try:
        nikto_output = subprocess.check_output(
            nikto_command, stderr=subprocess.STDOUT, text=True)

        # Parse Nikto output to extract relevant information
        nikto_results = parse_nikto_output(nikto_output)

        # Print the formatted results
        print_nikto_results(nikto_results)

    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")


def parse_nikto_output(nikto_output):
    # Parse the Nikto output and extract relevant information
    nikto_results = []

    # Extract lines starting from "+ " which contain vulnerability information
    vuln_lines = [line.strip()
                  for line in nikto_output.splitlines() if line.startswith("+ ")]

    # Parse vulnerability lines and populate nikto_results list
    for vuln_line in vuln_lines:
        # Remove the leading "+ " and split the line into category and description
        category, description = vuln_line[2:].split(":", 1)
        nikto_results.append(
            {"category": category.strip(), "description": description.strip()})

    return nikto_results


def print_nikto_results(scan_results):
    # Create a PrettyTable
    table = PrettyTable()

    # Define table headers
    table.field_names = ["Category", "Description"]

    # Populate the table with scan results
    for result in scan_results:
        table.add_row([result["category"], result["description"]])

    # Set column alignment
    table.align["Category"] = "l"
    table.align["Description"] = "l"

    # Print the table with color formatting
    print("\033[1;35mNikto Scan Results:\033[0m")
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
