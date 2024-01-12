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
    # Build SQLmap command
    sqlmap_command = f"sqlmap -u {url} --dbs"

    try:
        # Capture SQLmap command output
        original_output = subprocess.run(
            sqlmap_command.split(),
            text=True,
            capture_output=True,
            check=True
        ).stdout

        # Display original SQLmap output
        print("\n\033[94mOriginal SQLmap Output:\033[0m")
        print(original_output)

        # Process and format SQLmap result
        formatted_result = process_sqlmap_output(original_output)

        # Display formatted result
        print("\n\033[94mSummary:\033[0m")
        print_formatted_result(formatted_result)

    except subprocess.CalledProcessError as e:
        # Handle case where SQLmap command returns an error
        print("\033[91mError executing SQLmap:\033[0m")
        print(e.stderr)


def process_sqlmap_output(sqlmap_output):
    # Parse SQLmap output to extract necessary information
    # Add code here to extract and format SQLmap results
    formatted_result = {}  # Use a dictionary to store formatted results

    # Placeholder content, replace with actual extraction and formatting logic
    formatted_result['Vulnerabilities'] = ['Vuln1', 'Vuln2']
    formatted_result['Databases'] = ['db1', 'db2']

    return formatted_result


def print_formatted_result(formatted_result):
    # Create PrettyTable with formatted results
    table = PrettyTable()

    # Configure table columns (placeholders, adjust as needed)
    table.field_names = ["Category", "Details"]

    # Add content to the table (placeholders, adjust as needed)
    table.add_row(["Vulnerabilities", ", ".join(
        formatted_result.get('Vulnerabilities', []))])
    table.add_row(["Databases", ", ".join(
        formatted_result.get('Databases', []))])

    # Display PrettyTable
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
