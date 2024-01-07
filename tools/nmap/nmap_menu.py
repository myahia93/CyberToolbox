import os
from .nmap_functions import get_user_ip_input, nmap_scan, get_additional_options_menu, display_nmap_description


def nmap_title(print_banner_function):
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
        nmap_title(print_banner_function)
        print("\n[1]> Scan")
        print("[2]> Display Nmap Description")
        print("[0]> Return to main menu")

        try:
            option = int(input("Enter your option: "))
            if option == 1:
                ip_or_network = get_user_ip_input()
                if ip_or_network:
                    additional_options = get_additional_options_menu()
                    nmap_scan(ip_or_network, additional_options)
            elif option == 2:
                display_nmap_description()
            elif option == 0:
                return  # Return to main menu
            else:
                os.system("clear")
                print("\033[91mInvalid option. Please enter 0, 1, or 2.\033[0m")
        except ValueError:
            os.system("clear")
            print(
                "\033[91mInvalid input. Please enter a valid number.\033[0m", end='')
            print()
