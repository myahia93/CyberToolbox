import os
import subprocess
import re
from prettytable import PrettyTable


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
   to assess the robustness of passwords on networks. In \033[96mCyberToolbox\033[0;32m, sthe provided version of 
   Hydra is simplified and made more user-friendly through a series of questions posed to the user, 
   allowing for precise and easy configuration of brute-force tests.\033[0m
    """
    print(hydra_description)


def display_hydra_command_progress(target, attack_type, user_input, pass_input, is_user_file, is_pass_file, extra_params):
    user_param = '-L' if is_user_file else '-l'
    pass_param = '-P' if is_pass_file else '-p'
    command = f"\033[93mhydra {user_param} {user_input} {pass_param} {pass_input} {target} {attack_type} {extra_params}\033[0m"
    print("\nConstruction de la commande Hydra en cours :")
    print(command + "\n")


def execute_hydra(target, attack_type, username, password, is_username_file, is_password_file, extra_params=""):
    user_param = '-L' if is_username_file else '-l'
    pass_param = '-P' if is_password_file else '-p'
    command = f"hydra {user_param} {username} {pass_param} {password} {target} {attack_type} {extra_params}"
    try:
        result = subprocess.run(command, shell=True, check=False,
                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        if result.returncode in [0, 255]:  # Add other codes if needed
            print("\033[92m\nHydra command executed.\n\033[0m")
            if result.stdout:
                parse_hydra_output(result.stdout)
        else:
            print(f"Hydra exited with error code: {result.returncode}")
    except Exception as e:
        print(f"Error executing Hydra: {e}")


def parse_hydra_output(output):
    if not output:
        print("\033[91mNo output to parse.\033[0m")
        return

    table = PrettyTable()
    table.field_names = ["Service", "Host", "Login", "Password"]

    # Mise à jour de l'expression régulière pour inclure SSH, FTP et Web
    found_passwords_ssh = re.findall(
        r'\[\d+\]\[ssh\] host: ([^ ]+) +login: ([^ ]+) +password: ([^\s]+)', output)
    found_passwords_ftp = re.findall(
        r'\[\d+\]\[ftp\] host: ([^ ]+) +login: ([^ ]+) +password: ([^\s]+)', output)
    found_passwords_web = re.findall(
        r'\[\d+\]\[(http-[^\]]+)\] host: ([^ ]+) +login: ([^ ]+) +password: ([^\s]+)', output)

    # Ajout de la vérification des tentatives infructueuses pour le web
    unsuccessful_attempts_web = re.findall(
        r'\[\d+\]\[(http-[^\]]+)\] host: ([^ ]+) +login: ([^ ]+) +password: .+login incorrect', output)

    for host, login, password in found_passwords_ssh:
        table.add_row(
            ["SSH", host, f"\033[92m{login}\033[0m", f"\033[92m{password}\033[0m"])

    for host, login, password in found_passwords_ftp:
        table.add_row(
            ["FTP", host, f"\033[92m{login}\033[0m", f"\033[92m{password}\033[0m"])

    for service, host, login, password in found_passwords_web:
        table.add_row([service.upper(), host,
                      f"\033[92m{login}\033[0m", f"\033[92m{password}\033[0m"])

    for service, host, login in unsuccessful_attempts_web:
        table.add_row([service.upper(), host,
                      f"\033[91m{login}\033[0m", "\033[91mFailed\033[0m"])

    if len(table._rows) > 0:
        print(table)  # Affiche le tableau
    else:
        print("\033[91m\nNo valid passwords found.\033[0m")


def attack_submenu():
    while True:
        print("\033[1m\nOptions d'attaque Hydra:\033[0m")
        print("\n[\033[92m1\033[0m]> \033[96mBrute Force FTP\033[0m")
        print("[\033[92m2\033[0m]> \033[96mBrute Force SSH\033[0m")
        print("[\033[92m3\033[0m]> \033[96mBrute Force Web\033[0m")
        print("[\033[92m0\033[0m]> \033[96mReturn to Hydra menu\033[0m")

        try:
            choice = input("\nEntrez votre choix : ")

            # Inside attack_submenu function
 # Dans la fonction attack_submenu, assurez-vous d'ajouter l'argument extra_params
            if choice in ['1', '2']:
                service = "ftp" if choice == '1' else "ssh"
                target = input(
                    f"Entrez l'IP/hostname pour {service.upper()} : ")
                # Ajoutez extra_params avec une valeur par défaut vide
                display_hydra_command_progress(
                    service, target, "", "", False, False, "")

                user_type = input(
                    "Nom d'utilisateur (u) ou fichier (f)? [\033[92mu/f\033[0m]: ").strip().lower()
                is_user_file = user_type == 'f'
                user_input = input(
                    "\033[96mNom d'utilisateur :\033[0m " if not is_user_file else "\033[96mChemin vers la liste des noms d'utilisateur :\033[0m ")
                display_hydra_command_progress(
                    service, target, user_input, "", is_user_file, False, "")

                pass_type = input(
                    "Mot de passe (p) ou fichier (f)? [\033[92mp/f\033[0m]: ").strip().lower()
                is_pass_file = pass_type == 'f'
                pass_input = input(
                    "\033[96mMot de passe :\033[0m " if not is_pass_file else "\033[96mChemin vers la liste des mots de passe :\033[0m ")
                display_hydra_command_progress(
                    service, target, user_input, pass_input, is_user_file, is_pass_file, "")

                execute_hydra(target, service, user_input,
                              pass_input, is_user_file, is_pass_file, "")

            elif choice == '3':
                target = input("Entrez l'URL ou l'IP cible : ")
                attack_type = input(
                    "Entrez le type de service à attaquer (par exemple, http-post-form, http-get-form) : ")
                # Ajoutez extra_params avec une valeur par défaut vide
                display_hydra_command_progress(
                    target, attack_type, "", "", False, False, "")

                user_type = input(
                    "Nom d'utilisateur (u) ou fichier (f)? [\033[92mu/f\033[0m]: ").strip().lower()
                is_user_file = user_type == 'f'
                user_input = input(
                    "\033[96mNom d'utilisateur :\033[0m " if not is_user_file else "\033[96mChemin vers la liste des noms d'utilisateur :\033[0m ")
                display_hydra_command_progress(
                    target, attack_type, user_input, "", is_user_file, False, "")

                pass_type = input(
                    "Mot de passe (p) ou fichier (f)? [\033[92mp/f\033[0m]: ").strip().lower()
                is_pass_file = pass_type == 'f'
                pass_input = input(
                    "\033[96mMot de passe :\033[0m " if not is_pass_file else "\033[96mChemin vers la liste des mots de passe :\033[0m ")
                display_hydra_command_progress(
                    target, attack_type, user_input, pass_input, is_user_file, is_pass_file, "")

                # Texte en violet
                print(
                    "\033[95mAide: Les paramètres supplémentaires permettent de spécifier les détails du formulaire web.\033[0m")
                print(
                    "\033[95mPar exemple, pour un formulaire avec un champ d'identifiant 'id' et un champ de mot de passe 'mdp',\033[0m")
                print(
                    "\033[95met un message d'erreur 'Identifiant ou mot de passe incorrect', vous entreriez :\033[0m")
                # Exemple en cyan)
                print(
                    '\033[96m"/login.php:id=^USER^&mdp=^PASS^:Identifiant ou mot de passe incorrect!"\033[0m')

                extra_params = input(
                    "\nEntrez les paramètres supplémentaires (ou laissez vide) : ")
                # Affichez la progression finale ici avec extra_params
                display_hydra_command_progress(
                    target, attack_type, user_input, pass_input, is_user_file, is_pass_file, extra_params)

                execute_hydra(target, attack_type, user_input,
                              pass_input, is_user_file, is_pass_file, extra_params)

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
