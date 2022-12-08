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

import time
# tratar da string do comando 4
#1string_example = "Serial Number: 1015001350 Part Number: PAN2XUXSSA3I Slot: 1 Module: A Start date: 12/09/2022 Start time: 10:06:57 End date: 12/09/2022 End time: 10:13:27 Software version (tester): v1.12 Firmware version (tester): v1.45 Temperature (tester): 35 XFP firmware version: v10.87 XFP power consumption: 2.47 DDMI Tx Power: 7.8 DDMI Rx Power: -16.5 DDMI Tx Bias Current: 37.75 DDMI Temperature: 37 DDMI Vcc: 3.25 Tx Power CH1: 8.78 Tx Power CH2: 8.82 Tx Power CH3: 8.42 Tx Power CH4: 7.02 Step 1 PASS/FAIL: PASS Step 2 PASS/FAIL: PASS Step 3 PASS/FAIL: PASS Step 4 PASS/FAIL: PASS Step 5 PASS/FAIL: PASS Step 6 PASS/FAIL: PASS Error Code: - Final Result:     "
string_example = "Serial Number: 1015001350\nPart Number: PAN2XUXSSA3I\nSlot: 1\nModule: A\nStart date: 12/09/2022\nStart time: 10:06:57\nEnd date: 12/09/2022\nEnd time: 10:13:27\nSoftware version (tester): v1.12\nFirmware version (tester): v1.45\nTemperature (tester): 35\nXFP firmware version: v10.87\nXFP power consumption: 2.47\nDDMI Tx Power: 7.8\nDDMI Rx Power: -16.5\nDDMI Tx Bias Current: 37.75\nDDMI Temperature: 37\nDDMI Vcc: 3.25\nTx Power CH1: 8.78\nTx Power CH2: 8.82\nTx Power CH3: 8.42\nTx Power CH4: 7.02\nStep 1 PASS/FAIL: PASS\nStep 2 PASS/FAIL: PASS\nStep 3 PASS/FAIL: PASS\nStep 4 PASS/FAIL: PASS\nStep 5 PASS/FAIL: PASS\nStep 6 PASS/FAIL: PASS\nError Code: -\nFinal Result: PASS"
#3string_example = '{"Serial Number": "1015001350", "Part Number": "PAN2XUXSSA3I", "Slot": "1", "Module": "A", "Start date": "12/09/2022"}'

# convert string into json, necessita que venha num formato igual ao 3
#import json 
#conv = json.loads(string_example)
#print(conv['Slot'])

# using eval(), dá erro quando tentar tratar das datas, Funciona se usarmos o formato 3, not good
#r = eval(string_example)
#print(r['Slot'])

# Creating a list of lists, we can access the value doing ex: xfp[0][1]
def test_result(example):
    xfp_stat = []
    ex = example.split('\n')        # dividir a string por parametro, não sei se vem em '\n', ou ','
    '''for i in range(len(ex)):     # do the division for everything, but spliting with ':' chops de time strings
        d = ex[i].split(':')
        xfp_stat.append(d)
        print(xfp_stat)
    '''
    serial  = ex[0].split(':')      # posição do serial number
    slot    = ex[2].split(':')      # posição do slot
    result  = ex[29].split(':')     # posição do Resultado do teste
    
    xfp_stat = [serial, slot, result]    # here, we have a list of lists
    #xfp_stat = dict(xfp_stat)
    #print(xfp_stat)
    return dict(xfp_stat)   # returns in dictionary format


def main():
    # send TCP command ('1 A') Connect System
    box_connect = TCP_command('1 A')
    while ('Successfully finished!' not in box_connect):
        print(box_connect + '\nSending TCP command again')
        # maybe wait some time?
        TCP_command('1 A')

    print(box_connect)

    # send TCP command ('2 A') Read Modules
    read_module = TCP_command('2 A')
    '''if('Successfully finished!' not in box_connect):
        print(box_connect + '\nSending TCP command again')
        # maybe wait some time?
        TCP_command('2 A')

    print(box_connect)'''

    test_finish = ' -'
    while (test_finish == ' -'):  # verificar o que realmente vem quando o teste ainda não terminou
        print(test_finish)

        # wait some time
        #time.sleep(120) # 2 min

        # sends TCP command ('4 A')
        # tracking = TCP_command('4 A') 
        
        res_test = test_result(string_example)  # mudar para tracking
        print(res_test['Slot'])  # Assim conseguimos aceder ao valor do Serial/Slot/Resultado

        test_finish = res_test['Final Result']

main()