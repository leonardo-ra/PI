import socket
import time

HOST = "192.1.1.2"   # The remote host
PORT = 6000     # The same port as used by the server

print("Starting program")

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))      # Bind to the port  
s.listen()              # Wait for client connection
c, addr = s.accept()    # Establish connection with client

while True:
    
    try:
        msg = c.recv(1024)
        msg = msg.decode()
        print(f"Received: {msg}")

        if msg == "test done?":
            # envia um para indicar que um teste acabou
            tuplo = (1,1)   # o 1 extra e porque o polyscope precisa ou nao funciona
            string = str(tuplo)
            print(string)
            string2 = string.encode()
            c.send(string2)
            print("Sent "+string)

        elif msg == "test position":
            tuplo = (86,12.56,1)
            string = str(tuplo)
            print(string)
            string2 = string.encode()
            c.send(string2)  #mandar o X, Y e o resultado do teste 1 para OK e 2 para NOK
            print("Sent "+string)

        time.sleep(1)
    except socket.error as socketerror:
        break

s.close()
c.close()