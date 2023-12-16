import os
from .nmap_functions import get_user_ip_input, nmap_scan


def nmap_scan(print_banner_function):
    nmap_banner = """
    \033[93m.__   __. .___  ___.      ___      .______   
    |  \ |  | |   \/   |     /   \     |   _  \  
    |   \|  | |  \  /  |    /  ^  \    |  |_)  | 
    |  . `  | |  |\/|  |   /  /_\  \   |   ___/  
    |  |\   | |  |  |  |  /  _____  \  |  |      
    |__| \__| |__|  |__| /__/     \__\ | _|\033[0m   
    """

    print(nmap_banner)


def nmap_menu(print_banner_function):
    while True:
        nmap_scan(print_banner_function)
        print("\n[1]> Scan a Network")
        print("[2]> Scan an IP Address")
        print("[0]> Return to main menu")

        try:
            option = int(input("Enter your option: "))
            if option == 1 or option == 2:
                ip_or_network = get_user_ip_input()
                if ip_or_network:
                    nmap_scan(ip_or_network)
            elif option == 0:
                return  # Retourne au menu principal
            else:
                os.system("clear")
                print("\033[91mInvalid option. Please enter 0, 1, or 2.\033[0m")
        except ValueError:
            os.system("clear")
            print("\033[91mInvalid input. Please enter a valid number.\033[0m")
