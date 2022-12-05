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
        if msg == "test done?":
            #o número enviado deste lado (do python) tem de ter também o número de variáveis a enviar, neste caso 1
            test_yes=(1,1) #trigger para avançar do "test done?"
            test_yes = str(test_yes) #transforma em string
            c.send(test_yes.encode()) #mandar variaveis. Ainda não percebi muito bem porque é que ele n as lê do lado do Polyscope
            msg = c.recv(1024)
            msg = msg.decode()
            print(f"Received: {msg}")
            #Posição adquirida pela câmara e calculada pela câmara, a nossa "test position"
            #exemplo:
            #numero de variaveis enviadas: 6... Mas segundo o Pedro se calhar deveriam ser 3 (X,Y,Alpha)
            test_pos=(3.45, 4.81, -6.22, 0.00, 0.00, -0.035) 
            test_pos=str(test_pos)
            c.send(test_pos.encode())
            #
            test_res=(1,1)
            test_res=str(test_res)
            c.send(test_res.encode())
            
            
    except socket.error as socketerror:
        break

c.close()
s.close()
print("Program Finish")