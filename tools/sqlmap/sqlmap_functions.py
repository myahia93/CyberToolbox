import os
import requests
import subprocess
from bs4 import BeautifulSoup
from prettytable import PrettyTable


def check_url_validity():
    while True:
        # Ask the user to enter an URL
        url = input(
            "\n\033[92mEnter the URL to check: \033[0m")
        try:
            # Verify that the URL is accessible
            response = requests.get(url)
            response.raise_for_status()

            # Check whether the site uses a form for entering URLs
            soup = BeautifulSoup(response.content, 'html.parser')
            form = soup.find('form')

            if form:
                return url
            else:
                print(
                    "\033[91mThe provided URL does not have a form for input.\nPlease enter an URL that contain a form for input\033[0m")

        except requests.RequestException:
            print(
                "\033[91mInvalid URL. Please enter a valid URL.\033[0m", end='')
            print()


def perform_sqlmap_check(url):
    # Execute SQLmap command
    sqlmap_command = f"sqlmap -u {url} --dbs"
    sqlmap_output = subprocess.run(
        sqlmap_command.split(),
        text=True,
        capture_output=True
    ).stdout

    # Print the original SQLmap output
    print("\n\033[94mOriginal SQLmap Output:\033[0m")
    print(sqlmap_output)

    # Process and format the SQLmap output
    formatted_result = process_sqlmap_output(sqlmap_output)

    # Print the formatted result
    print("\n\033[94mSummary:\033[0m")
    print_formatted_result(formatted_result)


def process_sqlmap_output(sqlmap_output):
    formatted_result = {}

    # Split SQLmap output into lines
    lines = sqlmap_output.split('\n')

    # Check if SQLmap detected injection points
    if "sqlmap resumed the following injection point(s)" in sqlmap_output:
        formatted_result['Vulnerabilities'] = ["Vulnerable"]
        formatted_result['Injection Types'] = []

        # Extract injection types
        injection_lines = sqlmap_output.split('---\n')[1].split('\n')
        for line in injection_lines:
            if "Type:" in line:
                formatted_result['Injection Types'].append(
                    line.split("Type:")[1].strip())

    else:
        formatted_result['Vulnerabilities'] = ["Not Vulnerable"]

    # Extract additional information
    db_start_index = sqlmap_output.find("available databases")
    if db_start_index != -1:
        # Extract database names
        db_lines = sqlmap_output[db_start_index:].split(
            '\n')[2:-4]  # Exclude unnecessary lines
        formatted_result['Databases'] = [line.split(']')[1].strip(
        ) if ']' in line else line.strip() for line in db_lines]

    for line in lines:
        if "the back-end DBMS is" in line:
            formatted_result['DBMS'] = line.split(
                "the back-end DBMS is")[1].strip()
        elif "web server operating system" in line:
            formatted_result['OS'] = line.split(":")[1].strip()
        elif "web application technology" in line:
            formatted_result['Web Tech'] = line.split(":")[1].strip()

    return formatted_result


def print_formatted_result(formatted_result):
    # Create a PrettyTable with the formatted result
    table = PrettyTable()
    table.field_names = ["Category", "Value"]

    # Add vulnerability information
    table.add_row(["Vulnerability", formatted_result['Vulnerabilities'][0]])

    # Add injection types
    if 'Injection Types' in formatted_result:
        table.add_row(["Injection Types", ", ".join(
            formatted_result['Injection Types'])])

    # Add DBMS information
    if 'DBMS' in formatted_result:
        table.add_row(["DBMS", formatted_result['DBMS']])

    # Add OS information
    if 'OS' in formatted_result:
        table.add_row(["Operating System", formatted_result['OS']])

    # Add Web Tech information
    if 'Web Tech' in formatted_result:
        table.add_row(["Web Application Tech", formatted_result['Web Tech']])

    # Add Database names
    if 'Databases' in formatted_result:
        table.add_row(["Databases", "\n".join(formatted_result['Databases'])])

    # Set column alignment and print the table
    table.align = "l"
    print(table)


def display_sqlmap_description():
    sqlmap_description = """
    
    \033[93m
    SQLmap (SQL Injection and Database Hacking Tool) is an open-source penetration testing tool
    that automates the detection and exploitation of SQL injection vulnerabilities in web applications.

    Key Features:
    - Automatic SQL injection detection: SQLmap can automatically detect and exploit SQL injection vulnerabilities.
    - Support for multiple database management systems (DBMS): SQLmap supports various DBMS, including MySQL, PostgreSQL, and Microsoft SQL Server.
    - Time-based blind SQL injection: SQLmap can perform time-based blind SQL injection attacks to infer information about the database.
    - Union-based blind SQL injection: SQLmap can exploit union-based blind SQL injection vulnerabilities to retrieve data from the database.

    SQLmap is a powerful tool used by security professionals and penetration testers to identify and exploit
    SQL injection vulnerabilities, which can be a serious threat to the security of web applications. 
    In \033[96mCyberToolbox\033[93m, the provided version of SQLmap is simplified and made more
    user-friendly through a series of questions posed to the user. This approach allows
    for precise and easy configuration of scans.

    Note: SQLmap should be used responsibly and with proper authorization. Unauthorized use of SQLmap against
    systems for which you do not have explicit permission is illegal and unethical.\033[0m
    """

    print(sqlmap_description)
