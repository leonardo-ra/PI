# Commands to Communicate:
    # '1 A' - Connect System
    # '2 A' - Read Modules
    # '3 A' - Start Test
    # '4 A' - Tracking Results

# criar comunicação TCP com a caixa (default)
# • IP address: 127.0.0.1 
# • Port number: 13000 
# • Transfer data buffer(size): 8192 bytes 

# logic:
    # send '1 A' and waits for Success

    # while True
        # send '2 A' and waits for Success of 4 slots
        # send '3 A' to start the test
        # send '4 A' to receive the stat/results
import socket
import time
import os
import json

# string Defines
#stringTCP1 = 'Terminado com sucesso'    # ter este
#stringTCP2 = ['Erro','encontrado']    #não ter um destes dois
#stringTCP3 = 'Iniciou com sucesso'  # ter este
#stringTCP4 = 'Final Result'                     # rever

# tratar da string do comando 4
#1string_example = "Serial Number: 1015001350 Part Number: PAN2XUXSSA3I Slot: 1 Module: A Start date: 12/09/2022 Start time: 10:06:57 End date: 12/09/2022 End time: 10:13:27 Software version (tester): v1.12 Firmware version (tester): v1.45 Temperature (tester): 35 XFP firmware version: v10.87 XFP power consumption: 2.47 DDMI Tx Power: 7.8 DDMI Rx Power: -16.5 DDMI Tx Bias Current: 37.75 DDMI Temperature: 37 DDMI Vcc: 3.25 Tx Power CH1: 8.78 Tx Power CH2: 8.82 Tx Power CH3: 8.42 Tx Power CH4: 7.02 Step 1 PASS/FAIL: PASS Step 2 PASS/FAIL: PASS Step 3 PASS/FAIL: PASS Step 4 PASS/FAIL: PASS Step 5 PASS/FAIL: PASS Step 6 PASS/FAIL: PASS Error Code: - Final Result:     "
#string_example = "Serial Number: 1015001350\r\nPart Number: PAN2XUXSSA3I\r\nSlot: 1\r\nModule: A\r\nStart date: 12/09/2022\r\nStart time: 10:06:57\r\nEnd date: 12/09/2022\r\nEnd time: 10:13:27\r\nSoftware version (tester): v1.12\r\nFirmware version (tester): v1.45\r\nTemperature (tester): 35\r\nXFP firmware version: v10.87\r\nXFP power consumption: 2.47\r\nDDMI Tx Power: 7.8\r\nDDMI Rx Power: -16.5\r\nDDMI Tx Bias Current: 37.75\r\nDDMI Temperature: 37\r\nDDMI Vcc: 3.25\r\nTx Power CH1: 8.78\r\nTx Power CH2: 8.82\r\nTx Power CH3: 8.42\r\nTx Power CH4: 7.02\r\nStep 1 PASS/FAIL: PASS\r\nStep 2 PASS/FAIL: PASS\r\nStep 3 PASS/FAIL: PASS\r\nStep 4 PASS/FAIL: PASS\r\nStep 5 PASS/FAIL: PASS\r\nStep 6 PASS/FAIL: PASS\r\nError Code: -\r\nFinal Result: PASS\r\n\r\nSerial Number: 1015001350\r\nPart Number: PAN2XUXSSA3I\r\nSlot: 2\r\nModule: A\r\nStart date: 12/09/2022\r\nStart time: 10:06:57\r\nEnd date: 12/09/2022\r\nEnd time: 10:13:27\r\nSoftware version (tester): v1.12\r\nFirmware version (tester): v1.45\r\nTemperature (tester): 35\r\nXFP firmware version: v10.87\r\nXFP power consumption: 2.47\r\nDDMI Tx Power: 7.8\r\nDDMI Rx Power: -16.5\r\nDDMI Tx Bias Current: 37.75\r\nDDMI Temperature: 37\r\nDDMI Vcc: 3.25\r\nTx Power CH1: 8.78\r\nTx Power CH2: 8.82\r\nTx Power CH3: 8.42\r\nTx Power CH4: 7.02\r\nStep 1 PASS/FAIL: PASS\r\nStep 2 PASS/FAIL: PASS\r\nStep 3 PASS/FAIL: PASS\r\nStep 4 PASS/FAIL: PASS\r\nStep 5 PASS/FAIL: PASS\r\nStep 6 PASS/FAIL: PASS\r\nError Code: -\r\nFinal Result: PASS"
#3string_example = '{"Serial Number": "1015001350", "Part Number": "PAN2XUXSSA3I", "Slot": "1", "Module": "A", "Start date": "12/09/2022"}'

# Creating a dictionary
def test_result(example):
    xfp4 = []
    exe = example.split('\r\n\r\n')
    print(exe)
    for i in range(2):
        ex = exe[i].split('\r\n')        # dividir a string por parametro
        serial  = ex[0].split(':')      # posição do serial number
        slot    = ex[2].split(':')      # posição do slot
        result  = ex[29].split(':')     # posição do Resultado do teste
        xfp_stat = [serial, slot, result]    # here, we have a list of lists
        xfp4.append(dict(xfp_stat))
        
    return xfp4 #dict(xfp_stat)   # returns in dictionary format

def TCP_command(msg):
    # make connection with app
    HOST = "127.0.0.1"  # IP address 
    PORT = 13000        # Port number

    echoClient = socket.socket()        # create a socket client
    echoClient.connect((HOST, PORT))    # connect with app

    echoClient.send(msg.encode())       # send message
    msgReceived = echoClient.recv(4096)#256)  # receive message
    recv = msgReceived.decode()         # decode message
    return recv

def main(language = 'Portuguese'):
    # get language
    with open('Comms_Test_Box/language.json', 'r') as f:
        lang = json.load(f)

    languages = lang[language]
    #print(languages)
    stringTCP1 = languages[0]    # ter este
    stringTCP2 = languages[1]    #não ter um destes dois
    stringTCP3 = languages[2]    # ter este
    stringTCP4 = languages[3]    # rever

    # open the application
    os.system('start .\Comms_Test_Box\SW_CalBoard\App.exe')
    time.sleep(2)

    # test connection to the application
    # send TCP command ('1 A') Connect System
    #box_connect = "Terminado com sucesso fully finished!\nModule A is ready to be used!" #"Module A: OLT CH1 not!\n Error code: 3"
    box_connect = TCP_command('1 B')
    while (stringTCP1 not in box_connect):
        print(box_connect + 'Sending TCP command Connect System again\n')
        # maybe wait some time?
        time.sleep(10)
        box_connect = TCP_command('1 B')
    print(box_connect)
    
    # send TCP command ('2 A') Read Modules
    #read_module = "Erro: Module A is not connected!"
    #read_module = "Slot 1, Module A, Serial Number: 1014009530Slot 2, Module A, Serial Number: nao encontrado Not foundSlot 3, Module A, Serial Number: 1015001319Slot 4, Module A, Serial Number: 1015001342" 
    #read_module = "Slot 1, Module A, Serial Number: 1015001350\nSlot 2, Module A, Serial Number: 1015001356\nSlot 3, Module A, Serial Number: 1015001129\nSlot 4, Module A, Serial Number: 1015001319"
    read_module = TCP_command('2 B')
    while ((stringTCP2[0] in read_module) or (stringTCP2[1] in read_module)):# Se der erro, nenhum esta ligado, e no nosso caso acho que apenas nos interessa que estejam os quatro inseridos
        print(read_module + 'Sending TCP command Read Module again\n')
        time.sleep(10) # maybe wait some time? or send which slot is not found to the robot
        read_module = TCP_command('2 B')
    print(read_module)

    # send TCP command ('3 A') Start Test
    #start_test = "Error: Module A is not connected!" 
    #start_test = "Iniciou com sucesso Successfully started!Testing is running in background..."
    time.sleep(10)
    start_test = TCP_command('3 B')
    while (stringTCP3 not in start_test):
        print(start_test + 'Sending TCP command Start Test again\n')
        # diria que aqui os erros que podem dar dependem dos commandos anteriores, por isso ou vai atras enviar os outros comandos, 
        # ou nunca dá erro porque já o elimina-mos nos passos anteriores
        start_test = TCP_command('3 B')
    print(start_test)

    # send TCP command ('4 A') Tracking Results
    time.sleep(10)
    tracking = TCP_command('4 B')
    
    res_test = test_result(tracking)  # mudar para tracking
    #print(res_test)
    
    # ATENÇÃO: a string virá com 4 slots, separados por \n\n
    while (res_test[0][stringTCP4] == ' -'):  # 
        # wait some time
        time.sleep(30) # 2 min       
        tracking = TCP_command('4 B')
        print(tracking)
        res_test = test_result(tracking)  # mudar para tracking

    print(res_test)

#main()