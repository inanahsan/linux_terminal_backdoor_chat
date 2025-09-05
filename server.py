import socket
import threading
from prompt_toolkit import PromptSession
from prompt_toolkit import print_formatted_text
from prompt_toolkit.formatted_text import ANSI
from prompt_toolkit.patch_stdout import patch_stdout

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
session = PromptSession()
port = 12345
connections = {}
used_colors = {}

colors = [
    "\033[31m",
    "\033[32m",
    "\033[33m",
    "\033[34m",
    "\033[35m",
    "\033[36m",
    "\033[91m",
    "\033[92m",
    "\033[93m",
    "\033[94m",
]

my_color = "\033[95m"

s.bind(("", port))
s.listen(10)

def send_to_all(msg, excAddr = ""):
    for addr in connections:
        c = connections[addr]
        if excAddr and excAddr == addr:
            continue
        c.sendall(msg.encode())

def send_message():
    with patch_stdout():
        try:
            while True:
                msg = session.prompt()
                send_to_all(f"{my_color}{username}: {msg}\033[0m")
        except:
            s.close()

def receive_msg(addr):
    while True:
        c = connections[addr]
        msg = c.recv(1024).decode()
        if not msg:
            c.close()
            connections.pop(addr)
            break
        if addr in used_colors:
            msg = f"{used_colors[addr]}{msg}\033[0m"
        print_formatted_text(ANSI(msg))
        send_to_all(msg, addr)


try:
    username = input("Your username: ") or "anonymous"
    t1 = threading.Thread(target=send_message)
    t1.start()
    while True:
        (c,addr) = s.accept()
        connections[f"{addr[0]}_{addr[1]}"] = c
        used_colors[f"{addr[0]}_{addr[1]}"] = colors.pop()
        c.sendall("Thank you for connecting. Please add your username or blank string for anonymity".encode())
        uname = c.recv(1024).decode()
        if not uname:
            c.close()
            break
        print(f"Got connection from {addr} with username {uname}",)

        c.sendall(f"you are {uname}".encode())
        t2 = threading.Thread(target=receive_msg, args=(f"{addr[0]}_{addr[1]}",))
        t2.start()
except:
    s.close()