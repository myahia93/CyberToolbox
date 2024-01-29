import ipaddress
import subprocess
import os
import socket
import fcntl
import struct
import datetime
from urllib.parse import urlparse


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


def start_http_server():
    # Get the absolute path to the home directory
    home_directory = os.path.expanduser("~")

    # Start the HTTP server in the background
    subprocess.Popen(["python3", "-m", "http.server", "8085"], cwd=os.path.join(home_directory, "nikto_reports"),
                     stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def perform_nikto_check(target):
    print(
        "\n\033[1;35mRunning Nikto scan. This may take a few minutes...\n\033[0m")

    # Generate a unique report name based on date and time
    report_name = f"report-{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"

    # Prepare Nikto command
    nikto_command = ["nikto", "-h", target, "-o", os.path.join(
        os.path.expanduser("~"), "nikto_reports", report_name + ".html"), "</dev/null"]

    # Check if target starts with "https" and add "-ssl" option accordingly
    if target.startswith("https"):
        nikto_command.append("-ssl")

    # Run Nikto scan and capture output in real-time
    process = subprocess.Popen(
        nikto_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

    # Print the output in real-time
    while True:
        output_line = process.stdout.readline()
        if output_line == '' and process.poll() is not None:
            break
        if output_line:
            print(output_line.strip())

    # Print the message with the URL to view the report
    ip_address = get_eth0_ip_address()
    print(
        f"\n\033[1;35mView the detailed report on http://{ip_address}:8085/{report_name}.html\n\033[0m")


def get_eth0_ip_address():
    # Create a socket to retrieve the IP address
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Use ioctl to get information about the eth0 interface
    # SIOCGIFADDR is used to retrieve the IP address
    interface_name = b'eth0'
    ip_address = fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', interface_name[:15])
    )[20:24]

    # Convert the IP address to human-readable format
    ip_address = socket.inet_ntoa(ip_address)

    return ip_address


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
