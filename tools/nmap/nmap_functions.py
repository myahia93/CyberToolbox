import os
import ipaddress


# User IP input (ip or network address)
def get_user_ip_input():
    while True:
        option = int(input(
            "[1]> Scan a Network\n[2]> Scan an IP Address\n[0]> Return to main menu\nEnter your option: "))

        if option == 0:
            return None

        user_input_prompt = "Enter the network (in format x.x.x.x/x): " if option == 1 else "Enter the IP address: "
        validation_error_message = "Invalid network address. Please enter a valid network address." if option == 1 else "Invalid IP address. Please enter a valid IP address."

        user_input = input(user_input_prompt)

        try:
            if option == 1:
                ipaddress.IPv4Network(user_input)
            else:
                ipaddress.IPv4Address(user_input)
            return user_input
        except (ipaddress.AddressValueError, ipaddress.NetmaskValueError):
            os.system("clear")
            print(f"\033[91m{validation_error_message}\033[0m")


# Final nmap scan
def nmap_scan(ip_or_network):
    nmap_command = f"nmap {ip_or_network}"
    os.system(nmap_command)
