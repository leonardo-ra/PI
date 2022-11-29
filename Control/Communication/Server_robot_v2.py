# Echo client program
import socket
import time

HOST = "192.1.1.2"   # The remote host
PORT = 6000     # The same port as used by the server

print("Starting program")
while True:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))      # Bind to the port  
    s.listen()              # Wait for client connection
    c, addr = s.accept()    # Establish connection with client

    try: 
        msg = c.recv(1024)
        msg = msg.decode()
        print(f"Received: {msg}")
        if msg == "socket_works":
            tuplo = (0.0, 200.0, 30.0)
            string = str(tuplo)
            string = string.encode()
            c.send(string)
            print("Yeah it works. I sent (200, 50, 10)")
    except socket.error as socketerror:
        break

c.close()
s.close()
print("Program Finish")