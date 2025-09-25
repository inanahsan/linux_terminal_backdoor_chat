import socket
import threading
from prompt_toolkit import PromptSession
from prompt_toolkit import print_formatted_text
from prompt_toolkit.formatted_text import ANSI
from prompt_toolkit.patch_stdout import patch_stdout
import os

s = socket.socket()

port = 12345
ip = input("Please enter server ip: ")
session = PromptSession()
def send_message():
    with patch_stdout():
        try:
            while True:
                msg = session.prompt()
                if not msg:
                    continue
                elif msg == "___clear___":
                    os.system('clear')
                s.sendall(f"{username}: {msg}".encode())
        except:
            s.close()
        

def receive_msg():
    while True:
        msg = s.recv(1024).decode()
        if not msg:
            s.close()
            print("server closed, please contact server or run \nsource start_script.sh server")
            break  
        elif not (msg.find("___clear___") == -1):
            os.system('clear')
            continue
        print_formatted_text(ANSI(msg))

try:
    s.connect((ip, port))
    print(s.recv(1024).decode())
    username = input("Your username: ") or "anonymous"
    username.replace(":","")
    s.sendall(username.encode())
    send = threading.Thread(target=send_message)
    rcv = threading.Thread(target=receive_msg)
    send.start()
    rcv.start()
except:
    s.close()