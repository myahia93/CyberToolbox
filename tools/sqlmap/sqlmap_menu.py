import os
from .sqlmap_functions import display_sqlmap_description, check_url_validity, perform_sqlmap_check


def sqlmap_title(print_banner_function):
    sqlmap_banner = """
    \033[0;34m
  █████████            ████     ██████   ██████                    
 ███░░░░░███          ░░███    ░░██████ ██████                     
░███    ░░░   ████████ ░███     ░███░█████░███   ██████   ████████ 
░░█████████  ███░░███  ░███     ░███░░███ ░███  ░░░░░███ ░░███░░███
 ░░░░░░░░███░███ ░███  ░███     ░███ ░░░  ░███   ███████  ░███ ░███
 ███    ░███░███ ░███  ░███     ░███      ░███  ███░░███  ░███ ░███
░░█████████ ░░███████  █████    █████     █████░░████████ ░███████ 
 ░░░░░░░░░   ░░░░░███ ░░░░░    ░░░░░     ░░░░░  ░░░░░░░░  ░███░░░  
                 ░███                                     ░███     
                 █████                                    █████    
                ░░░░░                                    ░░░░░     \033[0m
 """
    print(sqlmap_banner)


def sqlmap_menu(print_banner_function):
    # Variable for controling the banner print
    show_banner = True

    while True:
        if show_banner:
            sqlmap_menu(print_banner_function)
        else:
            show_banner = True
        print("\n[\033[92m1\033[0m]> \033[96mDatabase Vulnerability Check\033[0m")
        print("[\033[92m2\033[0m]> \033[96mSQLmap Description\033[0m")
        print("[\033[92m0\033[0m]> \033[96mReturn to main menu\033[0m")

        try:
            option = int(input("\n\033[92mEnter your option: \033[0m"))
            if option == 1:
                url = check_url_validity()
                if url:
                    perform_sqlmap_check(url)
                else:
                    print(
                        "\n\033[91mInvalid URL. Please enter a valid URL.\033[0m")
            elif option == 2:
                display_sqlmap_description()
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
