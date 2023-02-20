#!/usr/bin/env python


from socket import *
import sys
import pyfiglet as fig
from colorama import init, Fore
import time
import ipaddress
from tkinter import *


# __COLOURS
init()
yellow = Fore.LIGHTYELLOW_EX

red = Fore.LIGHTRED_EX
green = Fore.LIGHTGREEN_EX
blue = Fore.LIGHTBLUE_EX
cyan = Fore.LIGHTCYAN_EX
pink = Fore.MAGENTA
reset = Fore.RESET

# __title
title = (fig.figlet_format("EAZE - POT", font='slant'))
print(yellow + title + reset)
print("  " * 20, f"~{cyan}*.*{red} SHY.BUG {cyan}*.*{reset}\n")


# __taking input host-ip and port to setup
ip = str(input("enter your ip:"))
port = int(input("enter the port to open:"))


# __a fake message sent for the attacker when he/she tries to access the services
def fakemsg(client_connection):
    client_connection.send(b"successfully loggedin ")
    client_connection.send(b"\naccessing services without permission is a crime")


try:
    # __establishing the honeypot and waiting for the attackers
    get_socket_connection = socket(AF_INET, SOCK_STREAM)
    get_socket_connection.bind((ip, port))
    get_socket_connection.listen(50)
    print(f"{pink}\nhoneypot setup completed & ready to go {reset}")
    while True:
        # __taking the request from attacker just as a server and gaining attackers credentials
        client_connection, client_address = get_socket_connection.accept()
        print(f"{green}[+] intrusion captured on {time.ctime(time.time())}:{reset}\n\t{red}intruder ip=>{client_address[0]}:{client_address[1]}{reset}")
        fakemsg(client_connection)
        print(f"\t{blue}fake successful authentication sent")
        print(f"\n\tgetting intruder credentials......{reset}")
        data = client_connection.recv(2048)
        decoded_data = data.decode('utf-8')
        decode_list = decoded_data.splitlines()
        for line in decode_list:
            print(f"\t{line}")
        client_connection.close()

except error as identifier:
    print(f"{red}\n[-] {identifier} error occured{reset}")
    client_connection.close()
except KeyboardInterrupt:
    print(f"{red}\n[-] stoping honeypot{reset}")
    get_socket_connection.close()
    exit()
finally:
    get_socket_connection.close()
