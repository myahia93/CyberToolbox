import os
import ipaddress


# User IP input (ip or network address)
def get_user_ip_input():
    while True:
        user_input = input(
            "Enter the IP address or network (in format x.x.x.x or x.x.x.x/x): ")
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

def get_additional_options_menu():
    additional_options = ""
    while True:
        print("\nChoose an option:")
        print("\n[1]> Port Filtering")
        print("[0]> No additional option (continue to scan)")

        try:
            option = int(input("\nEnter your option: "))
            if option == 1:
                additional_options += get_port_filtering_options()
            elif option == 0:
                break
            else:
                print("\033[91mInvalid option. Please enter 0 or 1.\033[0m")
        except ValueError:
            print(
                "\033[91mInvalid input. Please enter a valid number.\033[0m", end='')
            print()  # Adds a line to separate the error message from the prompt)
    return additional_options


def get_port_filtering_options():
    print("\nWhich port would you like to scan ?")
    print("\n[1]> Most common ports (HTTP, SSH, Telnet, DNS, FTP...)")
    print("[2]> Specify port or port range")
    print("[3]> Scan all ports")
    print("[0]> Return to previous menu")

    try:
        option = int(input("\nEnter your option: "))
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
    monitoring. It provides a comprehensive set of features for both simple and complex
    network scanning tasks.
    """

    print(nmap_description)


# Final nmap scan
def nmap_scan(ip_or_network, additional_options):
    nmap_command = f"nmap {additional_options} {ip_or_network}"
    os.system(nmap_command)
