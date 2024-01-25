import os
import subprocess


def display_hydra_description():
    hydra_description = """
    
    \033[0;32m
   Hydra (THC-Hydra) is an efficient and fast tool for brute-force testing of various protocols and services. 
   Hydra is often used to test password security by attempting to crack them using different combinations.

   Key Features:
   - Support for Numerous Protocols: Hydra can perform brute-force tests on a wide variety of protocols, 
   including FTP, HTTP, HTTPS, SMB, SSH, Telnet, and more.
   - Flexibility: Hydra allows great flexibility in configuring attacks, including the choice of password lists 
   and usernames.
   - Parallel Testing: Hydra is capable of performing parallel attacks on multiple hosts and ports simultaneously,
     speeding up the testing process.
   - Graphical User Interface: In addition to its command-line version, Hydra has a graphical interface (Hydra-GTK),
     making the tool more accessible to users who prefer a graphical interface.
   - Advanced Customization: Hydra allows advanced customizations for specific testing scenarios, including options
     for custom rules and conditions.

   Hydra is widely used by security professionals, system administrators, and security researchers 
   to assess the robustness of passwords on networks. In \033[0;31mCyberToolbox\033[0;32m, the provided version of 
   Hydra is simplified and made more user-friendly through a series of questions posed to the user, 
   allowing for precise and easy configuration of brute-force tests.\033[0m
    """
    print(hydra_description)


def execute_hydra(target, attack_type, user_list, pass_list, extra_params=""):
    command = f"hydra -L {user_list} -P {pass_list} {extra_params} {target} {attack_type}"
    try:
        subprocess.run(command, shell=True, check=True)
        print("Hydra command executed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error executing Hydra: {e}")


def attack_submenu():
    while True:
        print("\033[1m\nOptions d'attaque Hydra:\033[0m")
        print("\n[\033[92m1\033[0m]> \033[96mBrute Force FTP\033[0m")
        print("[\033[92m2\033[0m]> \033[96mBrute Force SSH\033[0m")
        print("[\033[92m3\033[0m]> \033[96mBrute Force Web\033[0m")
        print("[\033[92m0\033[0m]> \033[96mReturn to Hydra menu\033[0m")

        try:
            choice = input("\nEntrez votre choix : ")

            if choice == '1':
                target = input("Entrez l'IP/hostname pour FTP : ")
                user_list = input(
                    "Chemin vers la liste des noms d'utilisateur : ")
                pass_list = input("Chemin vers la liste des mots de passe : ")
                execute_hydra(target, "ftp", user_list, pass_list)

            elif choice == '2':
                target = input("Entrez l'IP/hostname pour SSH : ")
                user_list = input(
                    "Chemin vers la liste des noms d'utilisateur : ")
                pass_list = input("Chemin vers la liste des mots de passe : ")
                execute_hydra(target, "ssh", user_list, pass_list)

            elif choice == '3':
                target = input("Entrez l'URL du site Web : ")
                attack_type = input(
                    "Entrez le type de service à attaquer (par exemple, http-post-form, http-get-form) : ")
                user_list = input(
                    "Chemin vers la liste des noms d'utilisateur : ")
                pass_list = input("Chemin vers la liste des mots de passe : ")
                extra_params = input(
                    "Entrez les paramètres supplémentaires (ou laissez vide) : ")
                execute_hydra(target, attack_type, user_list,
                              pass_list, extra_params)
            elif choice == '0':
                os.system("clear")
                return
            else:
                os.system("clear")
                print(
                    "\033[91mOption invalide. Veuillez entrer 0, 1, 2 ou 3.\033[0m")

        except ValueError:
            os.system("clear")
            print(
                "\033[91mEntrée invalide. Veuillez entrer un nombre valide.\033[0m")
            print()
