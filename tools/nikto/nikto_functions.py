import ipaddress
import subprocess
from prettytable import PrettyTable


def display_nikto_description():
    nikto_description = """
    
    \033[93m
    Nmap (Network Mapper) is a powerful open-source tool for network exploration
    and security auditing. It is designed to discover hosts and services on a
    computer network, creating a "map" of the network. Nmap operates by sending
    raw IP packets to hosts on the network and then analyzing their responses.

    Key Features:
    - Host discovery: Nmap can identify hosts on a network and discover their IP addresses.
    - Port scanning: Nmap can scan for open ports on a host, helping identify running services.
    - Version detection: Nmap can determine the version of services running on open ports.
    - Operating System detection: Nmap can guess the operating system of a target host.
    - Scriptable interaction: Nmap supports scripting for advanced tasks and automation.

    Nmap is widely used by security professionals, system administrators, and network
    engineers for tasks such as network inventory, vulnerability scanning, and network
    monitoring. In \033[0;31mCyber Toolbox\033[93m, the provided version of Nmap is simplified and made more
    user-friendly through a series of questions posed to the user. This approach allows
    for precise and easy configuration of scans.\033[0m

    """

    print(nikto_description)
