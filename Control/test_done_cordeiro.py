import socket
import time
import os
import sys
#script_dir = os.path.dirname( __file__ )
#mymodule_dir = os.path.join( script_dir, 'Comms_Test_Box')
#sys.path.append( mymodule_dir )
from Comms_Test_Box import TestBoxComms as Tbox

HOST = "192.1.1.2"   # The remote host
PORT = 6000     # The same port as used by the server

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))      # Bind to the port  
s.listen()              # Wait for client connection
c, addr = s.accept()

print("Starting program")

def getResults(Check = 0):
    slotRes, info, transceivers = Tbox.run(resultCheck = Check)  # ao chamar isto, o pc passa a comunicar com a caixa de testes, e só sai daqui quando os testes terminam todos.
    # portanto, se isto termina é porque test done. entao podemos enviar diretamente o slot e o resultado
    if (info == 'TESTS RUNNING') or (info == 'TRANSCEIVERS MISSING'):
        info = 0
        return slotRes, info, transceivers
    else:
        info = 1
    # transforma o resultado no formato 1 ou 0
        for i in range(2):
            if slotRes['Slot '+str(i+1)] == 'PASS':
                slotRes['Slot '+str(i+1)] = 1
            elif slotRes['Slot '+str(i+1)] == 'FAIL':
                slotRes['Slot '+str(i+1)]  = 2
        return slotRes, info, transceivers

#getResults()    # inicia os testes
i = 1
    # Send slot and result to the arm
#i=4 # for test purposes
transceivers = False
while True:

    try:
        
        msg = c.recv(1024)
        msg = msg.decode()
        print(f"Received: {msg}")
        #msg = "test done?"
        #msg = "test position"
        
        if msg == "test done?":
            if transceivers == False:
                print("SOME Transceivers missing")
                result, tdone, transceivers = getResults(Check = 0)
            else:
                print("ALL Transceivers Inserted")
                result, tdone, transceivers = getResults(Check = 1)
                 
            # envia um para indicar que um teste acabou
            
            tuplo = (tdone,0)   # o 1 extra e porque o polyscope precisa ou nao funciona
            string = str(tuplo)
            string2 = string.encode()
            c.send(string2)
            print("Sent "+string)

        elif msg == "test position":
            #if i == 1:  # se for a primeira vez que pede a posição
            #    result, tdone = getResults(Check = 1)
            slotn = 'Slot '+ str(i)
            print(slotn)
            
            if i == 1:
                result, tdone, transceivers = getResults(Check = 1)
                tuplo = (36,12.56,result[slotn])
            elif i == 2:
                tuplo = (86,12.56,result[slotn])
            elif i == 3:
                tuplo = (136,12.56,result[slotn])
            elif i == 4:
                tuplo = (186,12.56,result[slotn])

            string = str(tuplo)
            print(string)
            string2 = string.encode()
            c.send(string2)  #mandar o X, Y e o resultado do teste 1 para OK e 2 para NOK
            print("Sent "+string)
            i = (i+1)%4         

        #time.sleep(1)
    except socket.error as socketerror:
        break

s.close()
c.close()