import os 
from .dnsdump_functions import sublister_menu, dig_menu, display_sublister_description, display_dig_description

def dnsdump_title(print_banner_function):
    dnsdump_banner = """
    \033[95m
 ██████████   ██████   █████  █████████     ██████████   █████  █████ ██████   ██████ ███████████ 
░░███░░░░███ ░░██████ ░░███  ███░░░░░███   ░░███░░░░███ ░░███  ░░███ ░░██████ ██████ ░░███░░░░░███
 ░███   ░░███ ░███░███ ░███ ░███    ░░░     ░███   ░░███ ░███   ░███  ░███░█████░███  ░███    ░███
 ░███    ░███ ░███░░███░███ ░░█████████     ░███    ░███ ░███   ░███  ░███░░███ ░███  ░██████████ 
 ░███    ░███ ░███ ░░██████  ░░░░░░░░███    ░███    ░███ ░███   ░███  ░███ ░░░  ░███  ░███░░░░░░  
 ░███    ███  ░███  ░░█████  ███    ░███    ░███    ███  ░███   ░███  ░███      ░███  ░███        
 ██████████   █████  ░░█████░░█████████     ██████████   ░░████████   █████     █████ █████       
░░░░░░░░░░   ░░░░░    ░░░░░  ░░░░░░░░░     ░░░░░░░░░░     ░░░░░░░░   ░░░░░     ░░░░░ ░░░░░                                                                                                                  
    \033[0m   
    """
    print(dnsdump_banner)

def dnsdump_menu(print_banner_function):
    show_banner = True

    while True:
        if show_banner:
            dnsdump_title(print_banner_function)
        else:
            show_banner = True

        print("\n[\033[92m1\033[0m]> \033[96mSublister Menu\033[0m")
        print("[\033[92m2\033[0m]> \033[96mDig Command Menu\033[0m")
        print("[\033[92m0\033[0m]> \033[96mReturn to Main Menu\033[0m")

        try:
            option = int(input("\n\033[92mEnter your option: \033[0m"))
            if option == 1:
                sublister_menu()
            elif option == 2:
                dig_menu()
            elif option == 3:
                display_sublister_description()
                show_banner = False
            elif option == 4:
                display_dig_description()
                show_banner = False
            elif option == 0:
                os.system("clear")
                return
            else:
                os.system("clear")
                print("\033[91mInvalid option. Please enter a number between 0 and 4.\033[0m")
        except ValueError:
            os.system("clear")
            print("\033[91mInvalid input. Please enter a valid number.\033[0m")
