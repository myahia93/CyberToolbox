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


def get_additional_options():
    while True:
        print("\n[1]> Port Filtering Options")
        print("[0]> Return to main menu")

        try:
            option = int(input("Enter your option: "))
            if option == 1:
                return get_port_filtering_options()
            elif option == 0:
                return None
            else:
                os.system("clear")
                print("\033[91mInvalid option. Please enter 0 or 1.\033[0m")
        except ValueError:
            os.system("clear")
            print(
                "\033[91mInvalid input. Please enter a valid number.\033[0m", end='')
            print()  # Adds a line to separate the error message from the prompt


def get_port_filtering_options():
    print("\n[1]> Scan the most common ports (-F)")
    print("[2]> Scan a specific port or range of ports (-p)")
    print("[3]> Scan all ports (-p-)")
    print("[0]> Return to additional options")

    while True:
        try:
            option = int(input("Enter your option: "))
            if option == 1:
                return "-F"
            elif option == 2:
                return "-p " + input("Enter the port or range of ports: ")
            elif option == 3:
                return "-p-"
            elif option == 0:
                return None
            else:
                os.system("clear")
                print(
                    "\033[91mInvalid option. Please enter 0, 1, 2, or 3.\033[0m")
        except ValueError:
            os.system("clear")
            print(
                "\033[91mInvalid input. Please enter a valid number.\033[0m", end='')
            print()  # Adds a line to separate the error message from the prompt


# Final nmap scan
def nmap_scan(ip_or_network, additional_options):
    nmap_command = f"nmap {additional_options} {ip_or_network}"
    os.system(nmap_command)
