import socket
import threading

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = 12345
connections = {}

s.bind(("", port))
s.listen(10)

# def remove_connection(removalAddr):
#     for connection in connections:
#         (c, addr) = connection
#         connections.remove((c,addr))

def send_to_all(msg, excAddr = ""):
    for addr in connections:
        c = connections[addr]
        if excAddr and excAddr == addr:
            continue
        c.sendall(msg.encode())

def send_message():
    try:
        while True:
            msg = input()
            send_to_all(f"{username}: {msg}")
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
        print(msg)
        send_to_all(msg, addr)


try:
    username = input("Your username: ") or "anonymous"
    t1 = threading.Thread(target=send_message)
    t1.start()
    while True:
        (c,addr) = s.accept()
        connections[f"{addr[0]}_{addr[1]}"] = c
        c.sendall("Thank you for connecting. Please add your username or blank string for anonymity".encode())
        uname = c.recv(1024).decode()
        if not uname:
            c.close()
            break
        print(f"Got connection from {addr} with username {uname}")

        c.sendall(f"you are {uname}".encode())
        t2 = threading.Thread(target=receive_msg, args=(f"{addr[0]}_{addr[1]}",))
        t2.start()
except:
    s.close()