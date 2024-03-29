#!/usr/bin/env python3

import os
import sys
from tools.nmap.nmap_menu import nmap_menu
from tools.sqlmap.sqlmap_menu import sqlmap_menu
from tools.hydra.hydra_menu import hydra_menu
from tools.nikto.nikto_menu import nikto_menu
from tools.theharvester.harvester_menu import harvester_menu
from tools.dnsdump.dnsdump_menu import dnsdump_menu


def print_banner():
    main_banner = """
\033[0;31m   █████████             █████                           ███████████                   ████  █████                         
  ███░░░░░███           ░░███                           ░█░░░███░░░█                  ░░███ ░░███                          
 ███     ░░░  █████ ████ ░███████   ██████  ████████    ░   ░███  ░   ██████   ██████  ░███  ░███████   ██████  █████ █████
░███         ░░███ ░███  ░███░░███ ███░░███░░███░░███       ░███     ███░░███ ███░░███ ░███  ░███░░███ ███░░███░░███ ░░███ 
░███          ░███ ░███  ░███ ░███░███████  ░███ ░░░        ░███    ░███ ░███░███ ░███ ░███  ░███ ░███░███ ░███ ░░░█████░  
░░███     ███ ░███ ░███  ░███ ░███░███░░░   ░███            ░███    ░███ ░███░███ ░███ ░███  ░███ ░███░███ ░███  ███░░░███     
 ░░█████████  ░░███████  ████████ ░░██████  █████           █████   ░░██████ ░░██████  █████ ████████ ░░██████  █████ █████
  ░░░░░░░░░    ░░░░░███ ░░░░░░░░   ░░░░░░  ░░░░░           ░░░░░     ░░░░░░   ░░░░░░  ░░░░░ ░░░░░░░░   ░░░░░░  ░░░░░ ░░░░░ 
                   ░███                                                                                                    
                ██████
\033[0;94m                                 .:. Coded by Ismael Mohcine Walid Amina Abdelmajid Minas .:.
\033[0m                                	
     """
    print(main_banner)


def main():
    while True:
        print_banner()
        print("\n[\033[92m1\033[0m]> \033[96mNmap\033[0m")
        print("[\033[92m2\033[0m]> \033[96mSQLmap\033[0m")
        print("[\033[92m3\033[0m]> \033[96mHydra\033[0m")
        print("[\033[92m4\033[0m]> \033[96mNikto\033[0m")
        print("[\033[92m5\033[0m]> \033[96mTheHarvester\033[0m")
        print("[\033[92m6\033[0m]> \033[96mDNSdump\033[0m")
        print("[\033[91m0\033[0m]> \033[91mExit the program\033[0m")

        try:
            option = int(input("\n\033[92mEnter your option: \033[0m"))
            if option == 1:
                nmap_menu(print_banner)
            elif option == 2:
                sqlmap_menu(print_banner)
            elif option == 3:
                hydra_menu(print_banner)
            elif option == 4:
                nikto_menu(print_banner)
            elif option == 5:
                harvester_menu(print_banner)
            elif option == 6:
                dnsdump_menu(print_banner)
            elif option == 0:
                print("\033[92m\nExiting the program. Goodbye!\033[m")
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
