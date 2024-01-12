import os
import sys
from tools.nmap.nmap_menu import nmap_menu
from tools.sqlmap.sqlmap_menu import sqlmap_menu

# def sqlmap_attack():
#     os.system("clear")
#     print_banner()
#     print("Launching SQLmap")
#     url = input("Enter URL: ")
#     os.system(f"python sqlmap.py -u {url}")


def hydra_bruteforce():
    os.system("clear")
    print_banner()
    print("Launching Hydra Bruteforce")
    # Ajoutez votre commande Hydra ici


def print_banner():
    main_banner = """
     \033[91m_______. \033[94m_______   \033[91m______  \033[94m__    __  \033[91m.___________.  \033[94m______     \033[91m______    \033[94m__       __  \033[91m___  __  \033[94m.___________.
    /       ||   ____| /      ||  |  |  | |           | /  __  \   /  __  \  |  |     |  |/  / |  | |           |
   |   (----`|  |__   |  ,----'|  |  |  | \033[91m`---|  |----`\033[94m|  |  |  | |  |  |  | |  |     |  '  /  |  | \033[91m`---|  |----`
    \   \    |   __|  |  |     |  |  |  |     |  |     |  |  |  | |  |  |  | |  |     |    <   |  |     |  |     
.----)   |   |  |____ |  `----.|  `--'  |     |  |     |  `--'  | |  `--'  | |  `----.|  .  \  |  |     |  |     
|_______/    |_______| \______| \______/      |__|      \______/   \______/  |_______||__|\__\ |__|     |__|                                                                                                               

                    \033[94m .:. Coded by @Ismael Mohcine Walid Amina Abdelmajid Minas .:.\033[0m
 """

    print(main_banner)


def main():
    while True:
        print_banner()
        print("\n[1]> Nmap")
        print("[2]> SQLmap")
        print("[3]> Hydra (Bruteforce)")
        print("[0]> Exit the program")

        try:
            option = int(input("Enter your option: "))
            if option == 1:
                nmap_menu(print_banner)
            elif option == 2:
                sqlmap_menu(print_banner)
            elif option == 3:
                hydra_bruteforce()
            elif option == 0:
                print("\033[92mExiting the program. Goodbye!\033[m")
                sys.exit()
            else:
                os.system("clear")
                print(
                    "\033[91mInvalid option. Please enter a number between 0 and 3.\033[0m")
        except ValueError:
            os.system("clear")
            print("\033[91mInvalid input. Please enter a valid number.\033[0m")


if __name__ == "__main__":
    main()
