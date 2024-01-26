import ipaddress
import subprocess
import os
import requests
from urllib.parse import urlparse
from datetime import datetime


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

    # Generate a unique file name for the report
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    report_filename = f"report-{timestamp}.html"

    # Full path for the report in ~/nikto_reports
    reports_directory = os.path.expanduser("~/nikto_reports")
    report_path = os.path.join(reports_directory, report_filename)

    # Prepare Nikto command with output in the reports directory
    nikto_command = ["nikto", "-h", target, "-o", report_path]

    # Check if target starts with "https" and add "-ssl" option accordingly
    if target.startswith("https"):
        nikto_command.append("-ssl")

    # Check if the Python server is already active in the directory
    if not is_server_running():
        # If the server is not active, start it in the background
        start_server_command = ["python3", "-m", "http.server", "8085"]
        subprocess.Popen(start_server_command, cwd=reports_directory)

    try:
        # Execute the Nikto scan
        subprocess.run(nikto_command, stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE, check=True)
        # If the command runs successfully, stdout and stderr will not be printed
    except subprocess.CalledProcessError as e:
        # Print the error message only if the command fails
        print(f"An error occurred: {e.stderr.decode()}")

    # Get the public IP address dynamically
    ip_address = get_public_ip_address()

    # Display the message with the URL to access the report
    print(
        f"\n\n\033[1;35mYou can view the detailed report on http://{ip_address}:8085/{report_filename}\n\033[0m")


def is_server_running():
    # Check if the Python server is listening on the specified port (8085)
    try:
        subprocess.run(["nc", "-zv", "localhost", "8085"], check=True,
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except subprocess.CalledProcessError:
        return False


def get_public_ip_address():
    # Get the public IP address using httpbin
    try:
        response = requests.get("https://httpbin.org/ip")
        ip_address = response.json()["origin"]
        return ip_address
    except requests.RequestException:
        return "127.0.0.1"  # Default IP address if retrieval fails


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
