import os
from .hydra_functions import attack_submenu, display_hydra_description

def hydra_title(print_banner_function):
    hydra_banner = """
    \033[0;32m
 █████   █████                █████                    
░░███   ░░███                ░░███                     
 ░███    ░███  █████ ████  ███████  ████████   ██████  
 ░███████████ ░░███ ░███  ███░░███ ░░███░░███ ░░░░░███ 
 ░███░░░░░███  ░███ ░███ ░███ ░███  ░███ ░░░   ███████ 
 ░███    ░███  ░███ ░███ ░███ ░███  ░███      ███░░███ 
 █████   █████ ░░███████ ░░████████ █████    ░░████████
░░░░░   ░░░░░   ░░░░░███  ░░░░░░░░ ░░░░░      ░░░░░░░░ 
                    ░███                               
               ░░██████                
    \033[0m   
    """
    print(hydra_banner)

def hydra_menu(print_banner_function):
    show_banner = True  # Initialisation de la variable pour contrôler l'affichage de la bannière

    while True:
        if show_banner:
            hydra_title(print_banner_function)
        else:
            show_banner = True  # Réinitialise pour les prochaines itérations

        print("\n[\033[92m1\033[0m]> \033[96mAttack\033[0m")
        print("[\033[92m2\033[0m]> \033[96mHydra Description\033[0m")
        print("[\033[92m0\033[0m]> \033[96mReturn to main menu\033[0m")

        try:
            option = int(input("\n\033[92mEnter your option: \033[0m"))
            if option == 1:
               attack_submenu()
            elif option == 2:
                display_hydra_description()
                show_banner = False  # Empêche l'affichage de la bannière après avoir montré la description
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
