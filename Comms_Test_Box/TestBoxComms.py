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


# Creating a dictionary
def test_result(example):
    xfp4 = []
    slots = {}
    exe = example.split('\r\n\r\n')
    #print(exe)
    for i in range(2):
        ex = exe[i].split('\r\n')        # dividir a string por parametro
        serial  = ex[0].split(':')      # posição do serial number
        slot    = ex[2].split(':')      # posição do slot
        result  = ex[29].split(':')     # posição do Resultado do teste
        xfp_stat = [serial, slot, result]    # here, we have a list of lists
        xfp4.append(dict(xfp_stat))     # list of dictionaries
        slots['Slot '+str(i+1)] = xfp4[i]['Final Result'].strip()   # only slot and result, the strip removes a space, not needed
    return xfp4, slots #dict(xfp_stat)   # returns in dictionary format

def TCP_command(msg):
    # make connection with app
    HOST = "127.0.0.1"  # IP address 
    PORT = 13000        # Port number

    echoClient = socket.socket()        # create a socket client
    echoClient.connect((HOST, PORT))    # connect with app

    echoClient.send(msg.encode())       # send message
    msgReceived = echoClient.recv(4096) # receive message
    recv = msgReceived.decode()         # decode message
    return recv

def run(language = 'Portuguese', resultCheck = 1, module = 'A'):
    # get language
    with open('Comms_Test_Box/language.json', 'r') as f:
        lang = json.load(f)

    languages = lang[language]
    #print(languages)
    stringTCP1 = languages[0]    # ter este
    stringTCP2 = languages[1]    #não ter um destes dois
    stringTCP3 = languages[2]    # ter este
    stringTCP4 = languages[3]    # rever
    dummy = {'Slot 1':None,'Slot 2':None,'Slot 3':None,'Slot 4':None,}
    trans = False
    # open the application
    os.system('start .\Comms_Test_Box\SW_CalBoard\App.exe')
    time.sleep(2)
    if resultCheck == 0:
        # test connection to the application
        # send TCP command ('1 A') Connect System
        #box_connect = "Terminado com sucesso fully finished!\nModule A is ready to be used!" #"Module A: OLT CH1 not!\n Error code: 3"
        box_connect = TCP_command('1 '+module)
        while (stringTCP1 not in box_connect):
            print(box_connect + 'Sending TCP command Connect System again\n')
            # maybe wait some time?
            time.sleep(10)
            box_connect = TCP_command('1 '+module)
        print(box_connect)
        
        # send TCP command ('2 A') Read Modules
        #read_module = "Erro: Module A is not connected!"
        #read_module = "Slot 1, Module A, Serial Number: 1014009530\r\nSlot 2, Module A, Serial Number: nao encontrado Not found\r\nSlot 3, Module A, Serial Number: 1015001319\r\nSlot 4, Module A, Serial Number: 1015001342" 
        #read_module = "Slot 1, Module A, Serial Number: 1015001350\nSlot 2, Module A, Serial Number: 1015001356\nSlot 3, Module A, Serial Number: 1015001129\nSlot 4, Module A, Serial Number: 1015001319"
        read_module = TCP_command('2 '+module)
        if ((stringTCP2[0] in read_module) or (stringTCP2[1] in read_module)):
            print('TRANSCEIVERS MISSING','\n',read_module)
            res_test = 'TRANSCEIVERS MISSING'
            trans = False
            return dummy, res_test, trans            
        print(read_module)
        trans = True
        # send TCP command ('3 A') Start Test
        #start_test = "Error: Module A is not connected!" 
        #start_test = "Iniciou com sucesso Successfully started!Testing is running in background..."
        #time.sleep(10)
        start_test = TCP_command('3 '+module)
        while (stringTCP3 not in start_test):
            print(start_test + 'Sending TCP command Start Test again\n')
            # diria que aqui os erros que podem dar dependem dos commandos anteriores, por isso ou vai atras enviar os outros comandos, 
            # ou nunca dá erro porque já o elimina-mos nos passos anteriores
            time.sleep(5)
            start_test = TCP_command('3 '+module)
        print(start_test)

        #1string_example = "Serial Number: 1015001350 Part Number: PAN2XUXSSA3I Slot: 1 Module: A Start date: 12/09/2022 Start time: 10:06:57 End date: 12/09/2022 End time: 10:13:27 Software version (tester): v1.12 Firmware version (tester): v1.45 Temperature (tester): 35 XFP firmware version: v10.87 XFP power consumption: 2.47 DDMI Tx Power: 7.8 DDMI Rx Power: -16.5 DDMI Tx Bias Current: 37.75 DDMI Temperature: 37 DDMI Vcc: 3.25 Tx Power CH1: 8.78 Tx Power CH2: 8.82 Tx Power CH3: 8.42 Tx Power CH4: 7.02 Step 1 PASS/FAIL: PASS Step 2 PASS/FAIL: PASS Step 3 PASS/FAIL: PASS Step 4 PASS/FAIL: PASS Step 5 PASS/FAIL: PASS Step 6 PASS/FAIL: PASS Error Code: - Final Result:     "
        #string_example = "Serial Number: 1015001350\r\nPart Number: PAN2XUXSSA3I\r\nSlot: 1\r\nModule: A\r\nStart date: 12/09/2022\r\nStart time: 10:06:57\r\nEnd date: 12/09/2022\r\nEnd time: 10:13:27\r\nSoftware version (tester): v1.12\r\nFirmware version (tester): v1.45\r\nTemperature (tester): 35\r\nXFP firmware version: v10.87\r\nXFP power consumption: 2.47\r\nDDMI Tx Power: 7.8\r\nDDMI Rx Power: -16.5\r\nDDMI Tx Bias Current: 37.75\r\nDDMI Temperature: 37\r\nDDMI Vcc: 3.25\r\nTx Power CH1: 8.78\r\nTx Power CH2: 8.82\r\nTx Power CH3: 8.42\r\nTx Power CH4: 7.02\r\nStep 1 PASS/FAIL: PASS\r\nStep 2 PASS/FAIL: PASS\r\nStep 3 PASS/FAIL: PASS\r\nStep 4 PASS/FAIL: PASS\r\nStep 5 PASS/FAIL: PASS\r\nStep 6 PASS/FAIL: PASS\r\nError Code: -\r\nFinal Result: -\r\n\r\nSerial Number: 1015001350\r\nPart Number: PAN2XUXSSA3I\r\nSlot: 2\r\nModule: A\r\nStart date: 12/09/2022\r\nStart time: 10:06:57\r\nEnd date: 12/09/2022\r\nEnd time: 10:13:27\r\nSoftware version (tester): v1.12\r\nFirmware version (tester): v1.45\r\nTemperature (tester): 35\r\nXFP firmware version: v10.87\r\nXFP power consumption: 2.47\r\nDDMI Tx Power: 7.8\r\nDDMI Rx Power: -16.5\r\nDDMI Tx Bias Current: 37.75\r\nDDMI Temperature: 37\r\nDDMI Vcc: 3.25\r\nTx Power CH1: 8.78\r\nTx Power CH2: 8.82\r\nTx Power CH3: 8.42\r\nTx Power CH4: 7.02\r\nStep 1 PASS/FAIL: PASS\r\nStep 2 PASS/FAIL: PASS\r\nStep 3 PASS/FAIL: PASS\r\nStep 4 PASS/FAIL: PASS\r\nStep 5 PASS/FAIL: PASS\r\nStep 6 PASS/FAIL: PASS\r\nError Code: -\r\nFinal Result: -"
        #string_example = "Serial Number: 1015001350\r\nPart Number: PAN2XUXSSA3I\r\nSlot: 1\r\nModule: A\r\nStart date: 12/09/2022\r\nStart time: 10:06:57\r\nEnd date: 12/09/2022\r\nEnd time: 10:13:27\r\nSoftware version (tester): v1.12\r\nFirmware version (tester): v1.45\r\nTemperature (tester): 35\r\nXFP firmware version: v10.87\r\nXFP power consumption: 2.47\r\nDDMI Tx Power: 7.8\r\nDDMI Rx Power: -16.5\r\nDDMI Tx Bias Current: 37.75\r\nDDMI Temperature: 37\r\nDDMI Vcc: 3.25\r\nTx Power CH1: 8.78\r\nTx Power CH2: 8.82\r\nTx Power CH3: 8.42\r\nTx Power CH4: 7.02\r\nStep 1 PASS/FAIL: PASS\r\nStep 2 PASS/FAIL: PASS\r\nStep 3 PASS/FAIL: PASS\r\nStep 4 PASS/FAIL: PASS\r\nStep 5 PASS/FAIL: PASS\r\nStep 6 PASS/FAIL: PASS\r\nError Code: -\r\nFinal Result: PASS\r\n\r\nSerial Number: 1015001350\r\nPart Number: PAN2XUXSSA3I\r\nSlot: 2\r\nModule: A\r\nStart date: 12/09/2022\r\nStart time: 10:06:57\r\nEnd date: 12/09/2022\r\nEnd time: 10:13:27\r\nSoftware version (tester): v1.12\r\nFirmware version (tester): v1.45\r\nTemperature (tester): 35\r\nXFP firmware version: v10.87\r\nXFP power consumption: 2.47\r\nDDMI Tx Power: 7.8\r\nDDMI Rx Power: -16.5\r\nDDMI Tx Bias Current: 37.75\r\nDDMI Temperature: 37\r\nDDMI Vcc: 3.25\r\nTx Power CH1: 8.78\r\nTx Power CH2: 8.82\r\nTx Power CH3: 8.42\r\nTx Power CH4: 7.02\r\nStep 1 PASS/FAIL: PASS\r\nStep 2 PASS/FAIL: PASS\r\nStep 3 PASS/FAIL: PASS\r\nStep 4 PASS/FAIL: PASS\r\nStep 5 PASS/FAIL: PASS\r\nStep 6 PASS/FAIL: PASS\r\nError Code: -\r\nFinal Result: FAIL"
        
        # send TCP command ('4 A') Tracking Results
        #time.sleep(10)
        tracking = TCP_command('4 '+module)
        #res_test,slot = test_result(string_example)#tracking)  # mudar para tracking
        res_test,slot = test_result(tracking)
        # ATENÇÃO: a string virá com 4 slots, separados por \n\n
        if (res_test[0][stringTCP4] == ' -'):  # 
            res_test = 'TESTS RUNNING'
            print(res_test)
            return dummy, res_test, trans
            # wait some time
            #time.sleep(120) # 2 min       
            #tracking = TCP_command('4 B')
            #print(tracking)
            #res_test, slot = test_result(tracking)  # mudar para tracking
        
        #print(res_test,'\n', slot)
        return slot, res_test, trans

    elif resultCheck == 1:
        trans = True
        #1string_example = "Serial Number: 1015001350 Part Number: PAN2XUXSSA3I Slot: 1 Module: A Start date: 12/09/2022 Start time: 10:06:57 End date: 12/09/2022 End time: 10:13:27 Software version (tester): v1.12 Firmware version (tester): v1.45 Temperature (tester): 35 XFP firmware version: v10.87 XFP power consumption: 2.47 DDMI Tx Power: 7.8 DDMI Rx Power: -16.5 DDMI Tx Bias Current: 37.75 DDMI Temperature: 37 DDMI Vcc: 3.25 Tx Power CH1: 8.78 Tx Power CH2: 8.82 Tx Power CH3: 8.42 Tx Power CH4: 7.02 Step 1 PASS/FAIL: PASS Step 2 PASS/FAIL: PASS Step 3 PASS/FAIL: PASS Step 4 PASS/FAIL: PASS Step 5 PASS/FAIL: PASS Step 6 PASS/FAIL: PASS Error Code: - Final Result:     "
        #string_example = "Serial Number: 1015001350\r\nPart Number: PAN2XUXSSA3I\r\nSlot: 1\r\nModule: A\r\nStart date: 12/09/2022\r\nStart time: 10:06:57\r\nEnd date: 12/09/2022\r\nEnd time: 10:13:27\r\nSoftware version (tester): v1.12\r\nFirmware version (tester): v1.45\r\nTemperature (tester): 35\r\nXFP firmware version: v10.87\r\nXFP power consumption: 2.47\r\nDDMI Tx Power: 7.8\r\nDDMI Rx Power: -16.5\r\nDDMI Tx Bias Current: 37.75\r\nDDMI Temperature: 37\r\nDDMI Vcc: 3.25\r\nTx Power CH1: 8.78\r\nTx Power CH2: 8.82\r\nTx Power CH3: 8.42\r\nTx Power CH4: 7.02\r\nStep 1 PASS/FAIL: PASS\r\nStep 2 PASS/FAIL: PASS\r\nStep 3 PASS/FAIL: PASS\r\nStep 4 PASS/FAIL: PASS\r\nStep 5 PASS/FAIL: PASS\r\nStep 6 PASS/FAIL: PASS\r\nError Code: -\r\nFinal Result: -\r\n\r\nSerial Number: 1015001350\r\nPart Number: PAN2XUXSSA3I\r\nSlot: 2\r\nModule: A\r\nStart date: 12/09/2022\r\nStart time: 10:06:57\r\nEnd date: 12/09/2022\r\nEnd time: 10:13:27\r\nSoftware version (tester): v1.12\r\nFirmware version (tester): v1.45\r\nTemperature (tester): 35\r\nXFP firmware version: v10.87\r\nXFP power consumption: 2.47\r\nDDMI Tx Power: 7.8\r\nDDMI Rx Power: -16.5\r\nDDMI Tx Bias Current: 37.75\r\nDDMI Temperature: 37\r\nDDMI Vcc: 3.25\r\nTx Power CH1: 8.78\r\nTx Power CH2: 8.82\r\nTx Power CH3: 8.42\r\nTx Power CH4: 7.02\r\nStep 1 PASS/FAIL: PASS\r\nStep 2 PASS/FAIL: PASS\r\nStep 3 PASS/FAIL: PASS\r\nStep 4 PASS/FAIL: PASS\r\nStep 5 PASS/FAIL: PASS\r\nStep 6 PASS/FAIL: PASS\r\nError Code: -\r\nFinal Result: -"
        #string_example = "Serial Number: 1015001350\r\nPart Number: PAN2XUXSSA3I\r\nSlot: 1\r\nModule: A\r\nStart date: 12/09/2022\r\nStart time: 10:06:57\r\nEnd date: 12/09/2022\r\nEnd time: 10:13:27\r\nSoftware version (tester): v1.12\r\nFirmware version (tester): v1.45\r\nTemperature (tester): 35\r\nXFP firmware version: v10.87\r\nXFP power consumption: 2.47\r\nDDMI Tx Power: 7.8\r\nDDMI Rx Power: -16.5\r\nDDMI Tx Bias Current: 37.75\r\nDDMI Temperature: 37\r\nDDMI Vcc: 3.25\r\nTx Power CH1: 8.78\r\nTx Power CH2: 8.82\r\nTx Power CH3: 8.42\r\nTx Power CH4: 7.02\r\nStep 1 PASS/FAIL: PASS\r\nStep 2 PASS/FAIL: PASS\r\nStep 3 PASS/FAIL: PASS\r\nStep 4 PASS/FAIL: PASS\r\nStep 5 PASS/FAIL: PASS\r\nStep 6 PASS/FAIL: PASS\r\nError Code: -\r\nFinal Result: PASS\r\n\r\nSerial Number: 1015001350\r\nPart Number: PAN2XUXSSA3I\r\nSlot: 2\r\nModule: A\r\nStart date: 12/09/2022\r\nStart time: 10:06:57\r\nEnd date: 12/09/2022\r\nEnd time: 10:13:27\r\nSoftware version (tester): v1.12\r\nFirmware version (tester): v1.45\r\nTemperature (tester): 35\r\nXFP firmware version: v10.87\r\nXFP power consumption: 2.47\r\nDDMI Tx Power: 7.8\r\nDDMI Rx Power: -16.5\r\nDDMI Tx Bias Current: 37.75\r\nDDMI Temperature: 37\r\nDDMI Vcc: 3.25\r\nTx Power CH1: 8.78\r\nTx Power CH2: 8.82\r\nTx Power CH3: 8.42\r\nTx Power CH4: 7.02\r\nStep 1 PASS/FAIL: PASS\r\nStep 2 PASS/FAIL: PASS\r\nStep 3 PASS/FAIL: PASS\r\nStep 4 PASS/FAIL: PASS\r\nStep 5 PASS/FAIL: PASS\r\nStep 6 PASS/FAIL: PASS\r\nError Code: -\r\nFinal Result: FAIL"
        
        # send TCP command ('4 A') Tracking Results
        #time.sleep(10)
        tracking = TCP_command('4 '+module)
        #res_test,slot = test_result(string_example)#tracking)  # mudar para tracking
        res_test,slot = test_result(tracking)
        # ATENÇÃO: a string virá com 4 slots, separados por \n\n
        if (res_test[0][stringTCP4] == ' -'):  # 
        #if (res_test[0][stringTCP4] != ' PASS') or (res_test[0][stringTCP4] !=' FAIL'):  # 
            res_test = 'TESTS RUNNING'
            print(res_test)
            return dummy, res_test, trans
        print('TESTS FINISHED')
        #print(res_test,'\n', slot)
        return slot, res_test, trans