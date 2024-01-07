import os
import ipaddress


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

def get_additional_options_menu(ip_or_network):
    additional_options = ""
    while True:
        print("\nChoose an option:")
        print("\n[\033[92m1\033[0m]> \033[96mPort Filtering\033[0m")
        print(
            "[\033[92m2\033[0m]> \033[96mOperating System Detection (SUDO REQUIRED)\033[0m")
        print("[\033[92m3\033[0m]> \033[96mService Version Detection\033[0m")
        print(
            "[\033[92m0\033[0m]> \033[96mNo additional option (continue to scan)\033[0m")

        print("\nConstruction of the Nmap command:")
        print("\033[93m", end='')  # Yellow color for Nmap command
        print(f"nmap {ip_or_network} {additional_options}", end='')
        print("\033[0m")  # Reset color to default

        try:
            option = int(input("\n\033[92mEnter your option: \033[0m"))
            if option == 1:
                additional_options += get_port_filtering_options()
            elif option == 2:
                additional_options += "-O "
            elif option == 3:
                additional_options += "-sV "
            elif option == 0:
                break
            else:
                print(
                    "\033[91mInvalid option. Please enter 0, 1, 2, or 3.\033[0m")
        except ValueError:
            print(
                "\033[91mInvalid input. Please enter a valid number.\033[0m", end='')
            print()  # Adds a line to separate the error message from the prompt)
    return additional_options


def get_port_filtering_options():
    question = ""
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
            question == "\033[92mEnter port or port range (in format xx or xx-xx):\033[0m"
            return f"-p {input(question)} "
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
    monitoring. In SecuToolkit, the provided version of Nmap is simplified and made more
    user-friendly through a series of questions posed to the user. This approach allows
    for precise and easy configuration of scans.\033[0m

    """

    print(nmap_description)


# Final nmap scan
def nmap_scan(ip_or_network, additional_options):
    nmap_command = f"nmap {additional_options} {ip_or_network}"
    os.system(nmap_command)
