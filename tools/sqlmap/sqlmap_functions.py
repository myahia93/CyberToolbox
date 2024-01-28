import re
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
    print("\033[0;34mLoading SQLmap...\033[0m")
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
        formatted_result['Vulnerabilities'] = ["\033[91mVulnerable\033[0m"]
        formatted_result['Injection Types'] = []

        # Extract injection types
        injection_lines = sqlmap_output.split('---\n')[1].split('\n')
        for line in injection_lines:
            if "Type:" in line:
                formatted_result['Injection Types'].append(
                    line.split("Type:")[1].strip())

    else:
        formatted_result['Vulnerabilities'] = ["\033[92mNot Vulnerable\033[0m"]

    # Extract additional information
    db_start_index = sqlmap_output.find("available databases")
    if db_start_index != -1:
        # Extract lines after "available databases"
        db_lines = sqlmap_output[db_start_index:].split('\n')[1:]
        # Stop when encountering an empty line
        formatted_result['Databases'] = []
        for line in db_lines:
            if line.strip():  # Check if the line is not empty
                formatted_result['Databases'].append(line.split(']')[
                                                     1].strip())
            else:
                break

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
        table.add_row(["DBMS", "\033[95m" +
                      formatted_result['DBMS']+"\033[0m"])

    # Add OS information
    if 'OS' in formatted_result:
        table.add_row(["Operating System", formatted_result['OS']])

    # Add Web Tech information
    if 'Web Tech' in formatted_result:
        table.add_row(["Web Application Tech", formatted_result['Web Tech']])

    # Add Database names
    if 'Databases' in formatted_result:
        table.add_row(["Databases", ", ".join(formatted_result['Databases'])])

    # Set column alignment and print the table
    table.align = "l"
    print(table)


def display_sqlmap_description():
    sqlmap_description = """
    
    \033[0;34m
    SQLmap (SQL Injection and Database Hacking Tool) is an open-source penetration testing tool
    that automates the detection and exploitation of SQL injection vulnerabilities in web applications.

    Key Features:
    - Automatic SQL injection detection: SQLmap can automatically detect and exploit SQL injection vulnerabilities.
    - Support for multiple database management systems (DBMS): SQLmap supports various DBMS, including MySQL, PostgreSQL, and Microsoft SQL Server.
    - Time-based blind SQL injection: SQLmap can perform time-based blind SQL injection attacks to infer information about the database.
    - Union-based blind SQL injection: SQLmap can exploit union-based blind SQL injection vulnerabilities to retrieve data from the database.

    SQLmap is a powerful tool used by security professionals and penetration testers to identify and exploit
    SQL injection vulnerabilities, which can be a serious threat to the security of web applications. 
    In \033[0;31mCyberToolbox\033[0;34m, the provided version of SQLmap is simplified and made more
    user-friendly through a series of questions posed to the user. This approach allows
    for precise and easy configuration of scans.

    Note: SQLmap should be used responsibly and with proper authorization. Unauthorized use of SQLmap against
    systems for which you do not have explicit permission is illegal and unethical.\033[0m
    """

    print(sqlmap_description)


# SQLMAP DUMP :
def sqlmap_dump(url, database):
    tables = get_database_tables(url, database)
    if not tables:
        print("\033[91mNo tables found or unable to retrieve tables.\033[0m")
        return

    choice = prompt_for_table_choice(tables)
    if choice == len(tables) + 1:
        selected_tables = tables
    else:
        selected_tables = [tables[choice - 1]]
    print()

    tables_data = {}
    for table in selected_tables:
        print(f"\033[92mDumping table: {table}\033[0m")
        columns = get_table_columns(url, database, table)
        if not columns:
            print(f"\033[91mNo columns found for table {table}.\033[0m")
            continue
        tables_data[table] = dump_table_data(url, database, table, columns)

    print_results(tables_data)


def prompt_for_table_choice(tables):
    while True:
        print("\n\033[1;34mAvailable tables:\033[0m")
        for idx, table in enumerate(tables, start=1):
            print(f"{idx}. {table}")
        print(f"{len(tables) + 1}. Dump all tables")

        choice = input(
            "\n\033[1;34mEnter the number of the table you want to dump or choose to dump all:\033[0m ")
        if choice.isdigit():
            choice = int(choice)
            if 1 <= choice <= len(tables) + 1:
                return choice
        print("\033[91mPlease enter a valid number.\033[0m")


def execute_sqlmap_command(command):
    try:
        process = subprocess.Popen(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        stdout, stderr = process.communicate()
        if stderr:
            print("Error:", stderr)
        return stdout
    except Exception as e:
        print("Error executing SQLMap command:", e)
        return None


def get_database_tables(url, database):
    command = ["sqlmap", "-u", url, "-D", database, "--tables", "--batch"]
    output = execute_sqlmap_command(command)
    tables = re.findall(r'\|\s+(\w+)\s+\|', output)
    return tables if tables else None


def get_table_columns(url, database, table):
    command = ["sqlmap", "-u", url, "-D", database,
               "-T", table, "--columns", "--batch"]
    output = execute_sqlmap_command(command)
    columns = re.findall(r'\|\s+(\w+)\s+\|', output)
    return columns if columns else None


def dump_table_data(url, database, table, columns):
    all_data = {}
    for column in columns:
        command = ["sqlmap", "-u", url, "-D", database,
                   "-T", table, "-C", column, "--dump", "--batch"]
        output = execute_sqlmap_command(command)
        # Data Extract
        data = re.findall(r'\|\s+(\w+)\s+\|', output)
        if data:
            filtered_data = [d for d in data if d not in ("Column", "Data")]
            if filtered_data:
                all_data[column] = filtered_data
    return all_data


def print_results(tables_data):
    for table, columns_data in tables_data.items():
        for column, data in columns_data.items():
            print(f"\n\033[1;34m-- {table}.{column} --\033[0m")
            pt = PrettyTable()
            pt.field_names = ["Data"]
            for entry in data:
                pt.add_row([entry])
            print(pt)
