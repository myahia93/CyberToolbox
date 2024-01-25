import os
from .nikto_functions import display_nikto_description, check_target_validity, perform_nikto_check


def nikto_title(print_banner_function):
    nikto_banner = """
    \033[1;35m
 ██████   █████  ███  █████       █████            
░░██████ ░░███  ░░░  ░░███       ░░███             
 ░███░███ ░███  ████  ░███ █████ ███████    ██████ 
 ░███░░███░███ ░░███  ░███░░███ ░░░███░    ███░░███
 ░███ ░░██████  ░███  ░██████░    ░███    ░███ ░███
 ░███  ░░█████  ░███  ░███░░███   ░███ ███░███ ░███
 █████  ░░█████ █████ ████ █████  ░░█████ ░░██████ 
░░░░░    ░░░░░ ░░░░░ ░░░░ ░░░░░    ░░░░░   ░░░░░░  
                                                                                                     
    \033[0m   
    """
    print(nikto_banner)


def nmap_menu(print_banner_function):
    # Variable for controling the banner print
    show_banner = True

    while True:
        if show_banner:
            nikto_title(print_banner_function)
        else:
            show_banner = True
        print("\n[\033[92m1\033[0m]> \033[96mWebserver Vulnerability Check\033[0m")
        print("[\033[92m2\033[0m]> \033[96mNikto Description\033[0m")
        print("[\033[92m0\033[0m]> \033[96mReturn to main menu\033[0m")

        try:
            option = int(input("\n\033[92mEnter your option: \033[0m"))
            if option == 1:
                target = check_target_validity()
                if target:
                    perform_nikto_check(target)
                else:
                    print(
                        "\n\033[91mInvalid target. Please enter a valid URL or IP address.\033[0m")
            elif option == 2:
                display_nikto_description()
                show_banner = False
            elif option == 0:
                os.system("clear")
                return  # Return to main menu
            else:
                os.system("clear")
                print("\033[91mInvalid option. Please enter 0, 1, or 2.\033[0m")
        except ValueError:
            os.system("clear")
            print(
                "\033[91mInvalid input. Please enter a valid number.\033[0m", end='')
            print()
