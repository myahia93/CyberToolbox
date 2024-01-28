import os
from .harvester_functions import display_theharvester_description, theharvester_menu


def harvester_title(print_banner_function):
    harvester_banner = """
    \033[0;36m
 ███████████ █████               █████   █████                                                   █████                      
░█░░░███░░░█░░███               ░░███   ░░███                                                   ░░███                       
░   ░███  ░  ░███████    ██████  ░███    ░███   ██████   ████████  █████ █████  ██████   █████  ███████    ██████  ████████ 
    ░███     ░███░░███  ███░░███ ░███████████  ░░░░░███ ░░███░░███░░███ ░░███  ███░░███ ███░░  ░░░███░    ███░░███░░███░░███
    ░███     ░███ ░███ ░███████  ░███░░░░░███   ███████  ░███ ░░░  ░███  ░███ ░███████ ░░█████   ░███    ░███████  ░███ ░░░ 
    ░███     ░███ ░███ ░███░░░   ░███    ░███  ███░░███  ░███      ░░███ ███  ░███░░░   ░░░░███  ░███ ███░███░░░   ░███     
    █████    ████ █████░░██████  █████   █████░░████████ █████      ░░█████   ░░██████  ██████   ░░█████ ░░██████  █████    
   ░░░░░    ░░░░ ░░░░░  ░░░░░░  ░░░░░   ░░░░░  ░░░░░░░░ ░░░░░        ░░░░░     ░░░░░░  ░░░░░░     ░░░░░   ░░░░░░  ░░░░░     
                                                                                                                             
    \033[0m   
    """
    print(harvester_banner)


def harvester_menu(print_banner_function):
    # Variable for controling the banner print
    show_banner = True

    while True:
        if show_banner:
            harvester_title(print_banner_function)
        else:
            show_banner = True
        print("\n[\033[92m1\033[0m]> \033[96mRun TheHarvester\033[0m")
        print("[\033[92m2\033[0m]> \033[96mTheHarvester Description\033[0m")
        print("[\033[92m0\033[0m]> \033[96mReturn to main menu\033[0m")

        try:
            option = int(input("\n\033[92mEnter your option: \033[0m"))
            if option == 1:
               theharvester_menu()
            elif option == 2:
                display_theharvester_description()
                show_banner = False  # Prevent displaying banner after showing description
            elif option == 0:
                os.system("clear")
                return  # Return to main menu
            else:
                os.system("clear")
                print("\033[91mInvalid option. Please enter 0, 1, or 2.\033[0m")
        except ValueError:
            os.system("clear")
            print("\033[91mInvalid input. Please enter a valid number.\033[0m", end='')
            print()
