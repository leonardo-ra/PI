import socket
from time import sleep

HOST = "192.1.1.2"   # The remote host
PORT = 6000     # The same port as used by the server

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))      # Bind to the port  
s.listen()              # Wait for client connection
c, addr = s.accept()


while True:
    
    try:
        msg = c.recv(1024)
        msg = msg.decode()
        print(f"Received: {msg}")

        if msg == "test done?":
            tuplo = (0,0)   # o 1 extra e porque o polyscope precisa ou nao funciona
            string = str(tuplo)
            string2 = string.encode()
            c.send(string2)
            print("Sent "+string)

    except socket.error as socketerror:
        break