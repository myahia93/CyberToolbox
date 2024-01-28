# Import statements for necessary modules
import subprocess
import re
from prettytable import PrettyTable

# Function to display the description of theHarvester
def display_theharvester_description():
    description = """
    \033[0;32m
    theHarvester is a tool for gathering e-mail accounts, subdomain names, virtual hosts, open ports/ banners, 
    and employee names from different public sources (search engines, pgp key servers).
    It's a really simple tool to use and is used to perform the first steps of reconnaissance in information gathering 
    or penetration testing engagements.

    Key Features:
    - Collects emails, names, subdomains, IPs, and URLs.
    - Uses multiple data sources, including search engines, and Shodan.
    - Simple and flexible to use for reconnaissance and information gathering.

    In \033[96mCyberToolbox\033[0;32m, theHarvester is integrated to facilitate the information gathering phase in 
    cybersecurity assessments, allowing for efficient data collection about a target organization or network.\033[0m
    """
    print(description)

# Function to display the constructed theHarvester command
def display_theharvester_command(domain, data_sources, limit):
    command = f"\033[93mtheHarvester -d {domain} -b {data_sources} -l {limit}\033[0m"
    print("\nConstructing theHarvester command:")
    print(command + "\n")

# Function to execute theHarvester command
def execute_theharvester(domain, data_sources, limit):
    command = f"theHarvester -d {domain} -b {data_sources} -l {limit}"
    try:
        result = subprocess.run(command, shell=True, check=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        if result.returncode == 0:
            print("\033[92m\ntheHarvester command executed.\n\033[0m")
            if result.stdout:
                parse_theharvester_output(result.stdout)
        else:
            print(f"theHarvester exited with error code: {result.returncode}")
    except Exception as e:
        print(f"Error executing theHarvester: {e}")

# Function to parse and display the output of theHarvester
def parse_theharvester_output(output):
    if not output:
        print("\033[91mNo output to parse.\033[0m")
        return

    table = PrettyTable()
    table.field_names = ["Type", "Data"]

    # Email extraction
    emails = re.findall(r'[\w\.-]+@[\w\.-]+\.\w+', output)

    # Extracting hosts
    hosts_matches = re.findall(r'([\w\.-]+\.[\w\.-]+(?:\.\w+)*)', output)
    hosts = [host for host in hosts_matches if not re.match(r'\d+\.\d+\.\d+\.\d+', host) and not re.match(r'\d+\.\d+\.\d+', host)]

    # Adding emails to the table
    if emails:
        email_count = len(emails)  # Count emails
        table.add_row(["Emails", "\n".join(emails)])

    # Adding a longer separator line
    if emails and hosts:
        table.add_row(["------", "------"])  # Increased length

    # Adding hosts to the table
    if hosts:
        table.add_row(["Hosts", "\n".join(set(hosts))])  # Using set to remove duplicates

    if len(table._rows) > 0:
        print(table)
    else:
        print("\033[91m\nNo relevant data found.\033[0m")


# Menu function for interacting with the user to configure and run theHarvester
def theharvester_menu():
 
            # Request target domain
            domain = input("\nEnter the target domain: ")
            partial_command = f"theHarvester -d {domain}"
            print(f"\033[93m\nCurrent command: {partial_command}\033[0m\n")

            # Request data sources
            data_sources = input("Enter the data sources (e.g., yahoo, bing): ")
            partial_command += f" -b {data_sources}"
            print(f"\033[93m\nCurrent command: {partial_command}\033[0m\n")

            # Request result limit
            limit = input("Enter the limit for results: ")
            partial_command += f" -l {limit}"
            print(f"\033[93m\nFinal command: {partial_command}\033[0m\n")
            print("\ntheHarvester loading...\n")

            # Run full command
            execute_theharvester(domain, data_sources, limit)

      


