import socket
import threading
import time

s = socket.socket()

port = 12345

def send_message():
    try:
        while True:
            msg = input()
            s.send(f"{username}: {msg}".encode())
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
    s.send(username.encode())
    send = threading.Thread(target=send_message)
    rcv = threading.Thread(target=receive_msg)
    send.start()
    rcv.start()
except:
    s.close()