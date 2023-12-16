import os
import ipaddress


# User IP input (ip or network address)
def get_user_ip_input():
    while True:
        option = int(input(
            "[1]> Enter an IP Address\n[2]> Enter a Network\n[0]> Return to main menu\nEnter your option: "))
        if option == 1:
            while True:
                user_input = input("Enter the IP address: ")
                try:
                    ipaddress.IPv4Address(user_input)
                    return user_input
                except ipaddress.AddressValueError:
                    os.system("clear")
                    print(
                        "\033[91mInvalid input. Please enter a valid IP address.\033[0m")
        elif option == 2:
            while True:
                user_input = input("Enter the network (in format x.x.x.x/x): ")
                try:
                    ipaddress.IPv4Network(user_input)
                    return user_input
                except (ipaddress.AddressValueError, ipaddress.NetmaskValueError):
                    os.system("clear")
                    print(
                        "\033[91mInvalid input. Please enter a valid network address.\033[0m")
        elif option == 0:
            return None
        else:
            os.system("clear")
            print("\033[91mInvalid option. Please enter 0, 1, or 2.\033[0m")


# Final nmap scan
def nmap_scan(ip_or_network):
    nmap_command = f"nmap {ip_or_network}"
    os.system(nmap_command)
