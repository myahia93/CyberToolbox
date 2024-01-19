import ipaddress
import subprocess
from prettytable import PrettyTable


# User IP input (ip or network address)
def get_user_ip_input():
    while True:
        user_input = input(
            "\033[92mEnter the IP address or network (in format x.x.x.x or x.x.x.x/x): \033[0m")
        try:
            if '/' in user_input:
                ipaddress.IPv4Network(user_input)  # Try to parse as a network
            else:
                # Try to parse as an IP address
                ipaddress.IPv4Address(user_input)
            return user_input
        except (ipaddress.AddressValueError, ipaddress.NetmaskValueError):
            print(
                "\033[91mInvalid input. Please enter a valid IP address or network address.\033[0m", end='')
            print()  # Adds a line to separate the error message from the prompt


# Nmap Options :
available_options = {}


def initialize_available_options():
    global available_options
    available_options = {
        1: {"name": "Port Filtering", "flag": "-F", "submenu": True},
        2: {"name": "Operating System Detection (\033[91mSUDO REQUIRED\033[96m)", "flag": "-O", "submenu": False},
        3: {"name": "Service Version Detection", "flag": "-sV", "submenu": False},
        4: {"name": "Custom Nmap Option (For Nmap Expert)", "flag": "", "submenu": False},
    }


def get_additional_options_menu(ip_or_network):
    global available_options
    additional_options = ""

    while True:
        # Initialize available options
        initialize_available_options()

        # Save options to display in a variable
        display_options = dict(available_options)

        print("\nChoose an option:")

        # Display available options with green numbers
        for option_num, option_data in display_options.items():
            print(
                f"[\033[92m{option_num}\033[0m]> \033[96m{option_data['name']}\033[0m")

        print(
            "[\033[92m0\033[0m]> \033[96mNo additional option (continue to scan)\033[0m")

        print("\nConstruction of the Nmap command:")
        print("\033[93m", end='')  # Yellow color for Nmap command
        print(f"nmap {ip_or_network} {additional_options}", end='')
        print("\033[0m")  # Reset color to default

        try:
            option = int(input("\n\033[92mEnter your option: \033[0m"))
            if option == 0:
                break
            elif option in display_options:
                selected_option = display_options.pop(option)
                if selected_option["submenu"]:
                    additional_options += get_submenu_option(selected_option)
                elif selected_option["name"] == "Custom Nmap Option (For Nmap Expert)":
                    additional_options += input(
                        "\n\033[92mEnter your custom Nmap option: \033[0m") + " "
                else:
                    additional_options += selected_option["flag"] + " "
                # Remove the selected option from available options
                available_options.pop(option, None)
            else:
                print(
                    "\033[91mInvalid option. Please enter a valid number.\033[0m")
        except ValueError:
            print(
                "\033[91mInvalid input. Please enter a valid number.\033[0m", end='')
            print()  # Adds a line to separate the error message from the prompt)

    return additional_options


def get_submenu_option(selected_option):
    if selected_option["name"] == "Port Filtering":
        return get_port_filtering_options()
    else:
        return ""


def get_port_filtering_options():
    global available_options
    print("\nWhich port would you like to scan ?")
    print("\n[\033[92m1\033[0m]> \033[96mMost common ports (HTTP, SSH, Telnet, DNS, FTP...)\033[0m")
    print("[\033[92m2\033[0m]> \033[96mSpecify port or port range\033[0m")
    print("[\033[92m3\033[0m]> \033[96mScan all ports\033[0m")
    print("[\033[92m0\033[0m]> \033[96mReturn to previous menu\033[0m")

    try:
        option = int(input("\n\033[92mEnter your option: \033[0m"))
        if option == 1:
            return "-F "
        elif option == 2:
            return f"-p {input('Enter port or port range (in format xx or xx-xx):')} "
        elif option == 3:
            return "-p- "
        elif option == 0:
            return ""
        else:
            print("\033[91mInvalid option. Please enter a valid number.\033[0m")
    except ValueError:
        print("\033[91mInvalid input. Please enter a valid number.\033[0m", end='')
        print()  # Adds a line to separate the error message from the prompt)
        return ""


def display_nmap_description():
    nmap_description = """
    
    \033[93m
    Nmap (Network Mapper) is a powerful open-source tool for network exploration
    and security auditing. It is designed to discover hosts and services on a
    computer network, creating a "map" of the network. Nmap operates by sending
    raw IP packets to hosts on the network and then analyzing their responses.

    Key Features:
    - Host discovery: Nmap can identify hosts on a network and discover their IP addresses.
    - Port scanning: Nmap can scan for open ports on a host, helping identify running services.
    - Version detection: Nmap can determine the version of services running on open ports.
    - Operating System detection: Nmap can guess the operating system of a target host.
    - Scriptable interaction: Nmap supports scripting for advanced tasks and automation.

    Nmap is widely used by security professionals, system administrators, and network
    engineers for tasks such as network inventory, vulnerability scanning, and network
    monitoring. In \033[0;31mSecuToolkit\033[93m, the provided version of Nmap is simplified and made more
    user-friendly through a series of questions posed to the user. This approach allows
    for precise and easy configuration of scans.\033[0m

    """

    print(nmap_description)


# Final nmap scan
def nmap_scan(ip_or_network, additional_options):
    print("\n\033[93mLoading Nmap...\033[0m")
    nmap_command = f"nmap {additional_options} {ip_or_network}"

    try:
        # Capture the output of the original Nmap command
        original_output = subprocess.run(
            nmap_command.split(),
            text=True,
            capture_output=True,
            check=True
        ).stdout

        # Print the original Nmap output
        print("\n\033[94mOriginal Nmap Output:\033[0m")
        print(original_output)

        # Process and format the Nmap output using prettytable
        formatted_result = process_nmap_output(original_output)

        # Print the formatted result
        print("\n\033[94mSummary:\033[0m")
        print_formatted_result(formatted_result)

    except subprocess.CalledProcessError as e:
        # Handle the case where the Nmap command returns an error
        print("\033[91mError executing Nmap:\033[0m")
        print(e.stderr)


# Function to process the Nmap output and return formatted results
def process_nmap_output(nmap_output):
    formatted_result = []

    # Process and format the Nmap output using prettytable
    table = PrettyTable()
    table.field_names = ["Host", "Service", "Port", "State"]

    current_host = None  # Variable to keep track of the current host being processed

    lines = nmap_output.split('\n')
    for line in lines:
        if line.startswith("Nmap scan report"):
            # Extract only the host name without parentheses
            current_host = line.split("(")[0].split()[-1]
        elif "/tcp" in line:
            fields = line.split()
            service = fields[2]
            port = fields[0].split('/')[0]
            state = fields[1]
            color_state = f"\033[91m{state}\033[0m" if state == "closed" else f"\033[92m{state}\033[0m"
            table.add_row([current_host, service, port, color_state])
            formatted_result.append([current_host, service, port, color_state])

    # Set column alignment
    table.align = "l"

    return formatted_result


# Function to format and print the Nmap results
def print_formatted_result(formatted_result):
    # Create a PrettyTable with the formatted result
    table = PrettyTable()
    table.field_names = ["Host", "Service", "Port", "State"]

    for entry in formatted_result:
        table.add_row(entry)

    # Set column alignment and print the table
    table.align = "l"
    print(table)
