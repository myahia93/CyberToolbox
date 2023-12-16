import os
import ipaddress


# User IP input (ip or network address)
def get_user_ip_input():
    while True:
        user_input = input("Enter the IP address or network: ")
        try:
            ipaddress.IPv4Address(user_input)
            return user_input
        except ipaddress.AddressValueError:
            try:
                ipaddress.IPv4Network(user_input)
                return user_input
            except ipaddress.NetmaskValueError:
                os.system("clear")
                print(
                    "\033[91mInvalid input. Please enter a valid IP address or network.\033[0m")


# Final nmap scan
def nmap_scan(ip_or_network):
    nmap_command = f"nmap {ip_or_network}"
    os.system(nmap_command)
