import os
from .sqlmap_functions import display_sqlmap_description, check_url_validity, perform_sqlmap_check


def sqlmap_title(print_banner_function):
    sqlmap_banner = """
    \033[93m.__   __. .___  ___.      ___      .______   
    |  \ |  | |   \/   |     /   \     |   _  \  
    |   \|  | |  \  /  |    /  ^  \    |  |_)  | 
    |  . `  | |  |\/|  |   /  /_\  \   |   ___/  
    |  |\   | |  |  |  |  /  _____  \  |  |      
    |__| \__| |__|  |__| /__/     \__\ | _|\033[0m   
    """

    print(sqlmap_banner)


def sqlmap_menu(print_banner_function):
    while True:
        sqlmap_title(print_banner_function)
        print("\n[\033[92m1\033[0m]> \033[96mDatabase Vulnerability Check\033[0m")
        print("[\033[92m2\033[0m]> \033[96mSQLmap Description\033[0m")
        print("[\033[92m0\033[0m]> \033[96mReturn to main menu\033[0m")

        try:
            option = int(input("\n\033[92mEnter your option: \033[0m"))
            if option == 1:
                # Ask the user to enter an URL
                url = input("\n\033[92mEnter the URL to check: \033[0m")
                if check_url_validity(url):
                    perform_sqlmap_check(url)
                else:
                    print(
                        "\n\033[91mInvalid URL. Please enter a valid URL.\033[0m")
            elif option == 2:
                display_sqlmap_description()
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
