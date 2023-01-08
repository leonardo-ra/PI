import socket
import time
import os
import sys

script_dir = os.path.dirname( __file__ )
mymodule_dir = os.path.join( script_dir, '..', 'Comms_Test_Box')
sys.path.append( mymodule_dir )
import TestBoxComms as Tbox
HOST = "192.1.1.2"   # The remote host
PORT = 6000     # The same port as used by the server

print("Starting program")

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))      # Bind to the port  
s.listen()              # Wait for client connection
c, addr = s.accept()    # Establish connection with client


def getResults():
    slotRes, moreInfo = Tbox.run()  # ao chamar isto, o pc passa a comunicar com a caixa de testes, e só sai daqui quando os testes terminam todos.
    # portanto, se isto termina é porque test done. entao podemos enviar diretamente o slot e o resultado

    # transforma o resultado no formato 1 ou 0
    for i in range(4):
        if slotRes['Slot '+str(i+1)] == 'PASS':
            slotRes['Slot '+str(i+1)] = 1
        elif slotRes['Slot '+str(i+1)] == 'FAIL':
            slotRes['Slot '+str(i+1)]  = 0
    return slotRes

result = getResults()
i = 1
while i <= 4:
    # Send slot and result to the arm
    tdone = 1   # test is done
    try:
        msg = c.recv(1024)
        msg = msg.decode()
        print(f"Received: {msg}")

        if msg == "test done?":
            # envia um para indicar que um teste acabou
            tuplo = (tdone,1)   # o 1 extra e porque o polyscope precisa ou nao funciona
            string = str(tuplo)
            print(string)
            string2 = string.encode()
            c.send(string2)
            print("Sent "+string)

        elif msg == "test position":

            tuplo = (86,12.56,result['Slot '+str(i)])
            # deve calcular aqui a posição do slot?, ou no polyscope, já sabe qual a pos de cada slot, só temos de enviar o numero do slot?
            string = str(tuplo)
            print(string)
            string2 = string.encode()
            c.send(string2)  #mandar o X, Y e o resultado do teste 1 para OK e 2 para NOK
            print("Sent "+string)

        time.sleep(1)
    except socket.error as socketerror:
        break

    i += 1

s.close()
c.close()