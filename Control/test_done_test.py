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

'''s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))      # Bind to the port  
s.listen()              # Wait for client connection
c, addr = s.accept()    # Establish connection with client
'''

def getResults(Check = 0):
    slotRes, info = Tbox.run(resultCheck = Check)  # ao chamar isto, o pc passa a comunicar com a caixa de testes, e só sai daqui quando os testes terminam todos.
    # portanto, se isto termina é porque test done. entao podemos enviar diretamente o slot e o resultado
    if info == ('TESTS RUNNING' or 'TRANSCEIVERS MISSING'):
        info = 0
        return slotRes,info
    else:
        info = 1
    # transforma o resultado no formato 1 ou 0
        for i in range(2):
            if slotRes['Slot '+str(i+1)] == 'PASS':
                slotRes['Slot '+str(i+1)] = 1
            elif slotRes['Slot '+str(i+1)] == 'FAIL':
                slotRes['Slot '+str(i+1)]  = 0
        return slotRes, info

#result = getResults()
i = 1
while True:
    # Send slot and result to the arm
    try:
        #msg = c.recv(1024)
        #msg = msg.decode()
        #print(f"Received: {msg}")
        #msg = "test done?"
        msg = "test position"
        getResults()
        if msg == "test done?":
            result, tdone = getResults(Check = 1)
            # envia um para indicar que um teste acabou
            tuplo = (tdone,1)   # o 1 extra e porque o polyscope precisa ou nao funciona
            string = str(tuplo)
            print(string)
            #string2 = string.encode()
            #c.send(string2)
            print("Sent "+string)

        elif msg == "test position":
            if i == 1:  # se for a primeira vez que pede a posição
                result, tdone = getResults(Check = 1)
            slotn = 'Slot '+str(i)
            print(slotn)
            tuplo = (86,12.56,result[slotn])
            # deve calcular aqui a posição do slot?, ou no polyscope, já sabe qual a pos de cada slot, só temos de enviar o numero do slot?
            string = str(tuplo)
            print(string)
            #string2 = string.encode()
            #c.send(string2)  #mandar o X, Y e o resultado do teste 1 para OK e 2 para NOK
            print("Sent "+string)
            i += 1

        time.sleep(1)
    except socket.error as socketerror:
        break

#s.close()
#c.close()