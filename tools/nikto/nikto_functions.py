import ipaddress
import subprocess
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


# def perform_nikto_check(target):
#     print("\033[1;35mLoading Nikto...\033[0m")
#     # Prepare Nikto command
#     nikto_command = ["nikto", "-h", target]

#     # Check if target starts with "https" and add "-ssl" option accordingly
#     if target.startswith("https"):
#         nikto_command.append("-ssl")

#     # Run Nikto scan
#     try:
#         subprocess.run(nikto_command, check=True)
#     except subprocess.CalledProcessError as e:
#         print(f"An error occurred: {e}")

def perform_nikto_check(target):
    print("\n\033[1;35mRunning Nikto scan. This may take a few minutes...\033[0m")
    # Prepare Nikto command
    nikto_command = ["nikto", "-h", target]

    # Check if target starts with "https" and add "-ssl" option accordingly
    if target.startswith("https"):
        nikto_command.append("-ssl")
    # Run Nikto command and capture the output
    nikto_output = subprocess.getoutput(nikto_command)

    # Display Nikto results
    display_nikto_results(nikto_output)


def display_nikto_results(nikto_output):
    # Check if any host was found
    if "0 host(s) tested" in nikto_output:
        print("\033[91mNo host found.\033[0m")
        return

    # Create a PrettyTable
    table = PrettyTable()
    table.field_names = ["Target IP", "Target Hostname",
                         "Target Port", "Start Time", "Server", "Vulnerabilities"]

    # Parse Nikto output and populate PrettyTable
    lines = nikto_output.split("\n")
    host_info = {}
    for line in lines:
        if line.startswith("+ Target"):
            parts = line.split(":")
            key = parts[1].strip()
            value = parts[2].strip()
            host_info[key] = value
        elif line.startswith("+ Start Time"):
            host_info["Start Time"] = line.split(":")[1].strip()
        elif line.startswith("+ ERROR:"):
            print("\033[91mNikto encountered errors:\033[0m")
            print(nikto_output)
            return
        elif line.startswith("+ Scan terminated"):
            host_info["End Time"] = line.split(":")[1].strip()

    # Check if any vulnerabilities were found
    if len(host_info) == 0:
        print("\033[91mNo valid results found.\033[0m")
        return

    # Print the PrettyTable
    table.add_row([host_info.get("Target IP", ""), host_info.get("Target Hostname", ""),
                   host_info.get("Target Port", ""), host_info.get(
                       "Start Time", ""),
                   host_info.get("Server", ""), host_info.get("Vulnerabilities", "")])

    # Print the table with colors
    print("\n\033[95mNikto Scan Results\033[0m")
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
