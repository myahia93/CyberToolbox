import os 
import subprocess
import re
from prettytable import PrettyTable

def display_sublister_description():
    sublister_description = """
    \033[95m
    Sublister is a powerful tool used in the field of cybersecurity for passive information gathering. 
    It is designed to discover subdomains of websites by using search engines and various external sources.

    Key Features:
    - Subdomain Discovery: Efficiently uncovers known subdomains of a target domain.
    - Multiple Data Sources: Gathers information from various search engines and external sources like VirusTotal, ThreatCrowd.
    - Passive Gathering: Performs reconnaissance without directly interacting with the target domain.
    - Extensive Reach: Can find subdomains that may not be visible through traditional methods.
    - User-Friendly: Offers a simple interface for users to conduct reconnaissance effectively.

    Sublister is an essential tool for penetration testers and cybersecurity professionals, 
    aiding in the initial stages of penetration testing and vulnerability assessment by revealing potential entry points in a domain's infrastructure.
    \033[0m
    """
    print(sublister_description)

def display_dig_description():
    dig_description = """
    \033[95m
    Dig (Domain Information Groper) is a versatile command-line tool primarily used for querying DNS servers. 
    It is a valuable resource for network administrators and cybersecurity professionals for DNS troubleshooting and information gathering.

    Key Features:
    - DNS Querying: Retrieves and displays DNS information, such as A records, MX records, and NS records.
    - Versatile and Detailed: Offers detailed information about the DNS response, including query time, server used, and more.
    - Support for Various Record Types: Capable of querying different types of DNS records.
    - Reverse DNS Lookups: Allows reverse DNS lookups to identify domain names associated with IP addresses.
    - Scriptable: Can be used in scripts and automated tasks, making it a versatile tool for DNS diagnostics and cybersecurity assessments.

    Dig is widely utilized for diagnosing DNS-related issues and performing comprehensive analysis of DNS infrastructure, 
    making it a staple tool in the arsenal of network and cybersecurity professionals.
    \033[0m
    """
    print(dig_description)


def display_sublister_command_progress(domain):
    command = f"\033[93msublist3r -d {domain}\033[0m"
    print("\nCurrent Command :", command, "\n")
    print("Sublist3r loading...\n")


def execute_sublister(domain):
    command = f"sublist3r -d {domain}"
    try:
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        print("\033[92m\nSublister command executed.\n\033[0m")
        
        # Calling the function to parse and display the output
        parse_sublister_output(result.stdout)

    except Exception as e:
        print(f"Error executing Sublister: {e}")

def clean_ansi_codes(text):
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', text)

def parse_sublister_output(output):
    if not output:
        print("\033[91mNo output to parse.\033[0m")
        return

    output = clean_ansi_codes(output)

    table = PrettyTable()
    table.field_names = ["Type", "Data"]

    # Extracting and cleaning subdomains
    subdomains = re.findall(r'([\w\.-]+\.[\w\.-]+(?:\.\w+)*)', output)
    cleaned_subdomains = set()
    for subdomain in subdomains:
        # Exclude IP addresses, version numbers, and other irrelevant elements
        if not re.match(r'\d+\.\d+\.\d+\.\d+', subdomain) and not re.match(r'\d+\.\d+\.\d+', subdomain) and not subdomain.endswith('..'):
            cleaned_subdomains.add(subdomain)

    # Adding subdomains to the table
    if cleaned_subdomains:
        table.add_row(["Subdomains", "\n".join(cleaned_subdomains)])

    if len(table._rows) > 0:
        print(table)
    else:
        print("\033[91m\nNo subdomains found.\033[0m")

def parse_dig_output(output):
    table = PrettyTable()
    table.field_names = ["Record Type", "Data"]

    ip_addresses = set()
    mail_servers = set()
    soa_record = None

    for line in output.splitlines():
        if line and not line.startswith(';') and not line.startswith(';;'):
            parts = line.split()
            if len(parts) >= 5:
                record_type = parts[3]
                data = ' '.join(parts[4:])

                if record_type == 'A':
                    ip_addresses.add(data)
                elif record_type == 'MX':
                    mail_servers.add(data)
                elif record_type == 'SOA':
                    soa_record = data

    if ip_addresses:
        table.add_row(["IP Addresses", "\n".join(ip_addresses)])
    if mail_servers:
        table.add_row(["Mail Servers", "\n".join(mail_servers)])
    if soa_record:
        table.add_row(["SOA Record", soa_record])

    return table

def execute_dig(target):
    command = f"dig {target} ANY +noall +answer"
    try:
        # Running the dig command and capturing the output
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        raw_output = result.stdout

        print("\033[92m\nDig command executed.\033[0m")

        # Show raw output
        print("\nRaw Output:\n")
        print(raw_output)

        # Show structured output in a table
        print("\n\033[92m\nStructured Output:\033[0m\n")
        table = parse_dig_output(raw_output)
        print(table)

    except Exception as e:
        print(f"Error executing Dig: {e}")



def sublister_menu():
    while True:
        print("\n\033[95mSublister Menu:\033[0m")
        print("\n[\033[92m1\033[0m]> \033[96mRun Sublister\033[0m")
        print("[\033[92m2\033[0m]> \033[96mSublister Description\033[0m")
        print("[\033[92m0\033[0m]> \033[96mReturn to DNSDump Menu\033[0m")

        try:
            choice = input("\nEnter your choice: ").strip()

            if choice == '1':
                domain = input("\nEnter the target domain: ")
                display_sublister_command_progress(domain)
                execute_sublister(domain)

            elif choice == '2':
                display_sublister_description()

            elif choice == '0':
                os.system("clear")
                return
            else:
                os.system("clear")
                print("\033[91mInvalid option. Please enter 0, 1, or 2.\033[0m")
        except ValueError:
            os.system("clear")
            print("\033[91mInvalid input. Please enter a valid number.\033[0m")

def dig_menu():
    while True:
        print("\n\033[95mDig Command Menu:\033[0m")
        print("\n[\033[92m1\033[0m]> \033[96mRun Dig Command\033[0m")
        print("[\033[92m2\033[0m]> \033[96mDig Command Description\033[0m")
        print("[\033[92m0\033[0m]> \033[96mReturn to DNSDump Menu\033[0m")

        try:
            choice = input("\nEnter your choice: ").strip()

            if choice == '1':
                target = input("\nEnter the target domain : ")
                execute_dig(target)
            elif choice == '2':
                display_dig_description()
            elif choice == '0':
                os.system("clear")
                return
            else:
                os.system("clear")
                print("\033[91mInvalid option. Please enter 0, 1, or 2.\033[0m")
        except ValueError:
            os.system("clear")
            print("\033[91mInvalid input. Please enter a valid number.\033[0m")

