import socket
import threading
from prompt_toolkit import PromptSession
from prompt_toolkit.patch_stdout import patch_stdout

s = socket.socket()

port = 12345
session = PromptSession()
def send_message():
    with patch_stdout():
        try:
            while True:
                msg = session.prompt()
                s.sendall(f"{username}: {msg}".encode())
        except:
            s.close()
        

def receive_msg():
    while True:
        msg = s.recv(1024).decode()
        print(msg)

try:
    s.connect(('127.0.0.1', port))
    print(s.recv(1024).decode())
    username = input("Your username: ") or "anonymous"
    s.sendall(username.encode())
    send = threading.Thread(target=send_message)
    rcv = threading.Thread(target=receive_msg)
    send.start()
    rcv.start()
except:
    s.close()