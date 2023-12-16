import os

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
        print("\n[1]> Nmap Option 1")
        print("[2]> Nmap Option 2")
        print("[0]> Return to main menu")

        try:
            option = int(input("Enter your option: "))
            if option == 1:
                # Mettez ici le code pour l'option 1 du sous-menu Nmap
                pass
            elif option == 2:
                # Mettez ici le code pour l'option 2 du sous-menu Nmap
                pass
            elif option == 0:
                return  # Retourne au menu principal
            else:
                os.system("clear")
                print("\033[91mInvalid option. Please enter a number between 0 and 2.\033[0m")
        except ValueError:
            os.system("clear")
            print("\033[91mInvalid input. Please enter a valid number.\033[0m")
