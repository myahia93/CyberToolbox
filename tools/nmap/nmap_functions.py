import os
import ipaddress


# User IP input (ip or network address)
def get_user_ip_input():
    while True:
        user_input = input(
            "Enter the IP address or network (in format x.x.x.x or x.x.x.x/x): ")
        try:
            ipaddress.IPv4Network(user_input)  # Try to parse as a network
        except ipaddress.AddressValueError:  # If it fails, try to parse as an IP address
            try:
                ipaddress.IPv4Address(user_input)
                return user_input
            except ipaddress.AddressValueError:
                os.system("clear")
                print(
                    "\033[91mInvalid input. Please enter a valid IP address or network address.\033[0m")
        except ipaddress.NetmaskValueError:
            os.system("clear")
            print(
                "\033[91mInvalid input. Please enter a valid network address.\033[0m")


# Final nmap scan
def nmap_scan(ip_or_network):
    nmap_command = f"nmap {ip_or_network}"
    os.system(nmap_command)
