import math
import socket
import torch
import Extract_points_of_yolo
import cv2
import Calculate_camera_points
import json
from time import sleep
import sys  
import os
from Comms_Test_Box import TestBoxComms as Tbox

def load_model():
    model = torch.hub.load(r'C:\Users\Leo\Desktop\Eu\Trabalhoua\Matricula6Ano\1Sem\PI\Final(2)\yolov5', 'custom', path=r'C:\Users\Leo\Desktop\Eu\Trabalhoua\Matricula6Ano\1Sem\PI\Final(2)\yolov5\models\best (1).pt', source='local')
    return model


model = load_model()
HOST = "192.1.1.2"  #The remote host
PORT = 6000         #The same port as used by the server
capture_index = 1   # Index of camera we want to acess
cam = cv2.VideoCapture(capture_index, cv2.CAP_DSHOW)    #Create video stream
cam.set(cv2.CAP_PROP_AUTOFOCUS, 0)  #Turn the autofocus off
cam.set(3, 1280)
cam.set(4, 720)
cam.set(cv2.CAP_PROP_FPS, 60)

calibration_file = "camera_image_small.npz"
square_size_m = 0.05029    

calib = input('Do you wish to do Calibration? (Y/N)')
if calib == 'Y' or calib == 'y' or calib == '':
    print("Start Calibration")
    calib_image = cv2.imread('./Big/frame0.jpg')
    # With a calibration photo of the board
    square_pixel_size, angle_between_axis, origin_robot_plane = Calculate_camera_points.Find_Corner_Chessboard(calib_image)
    dic = {"square_pixel_size": square_pixel_size, "angle_between_axis": angle_between_axis, "origin_robot_plane": str(origin_robot_plane)}
    with open("calib_parameters.json", "w") as outfile:
        json.dump(dic, outfile)                        # Write calib parameters to json file
    outfile.close()
else:
    print("No calibration made")
    with open("calib_parameters.json", "r") as infile:
        json_object = json.load(infile)                 # Read calib parameters from json file
        square_pixel_size = json_object["square_pixel_size"]
        angle_between_axis = json_object["angle_between_axis"]
        origin_robot_plane = eval(json_object["origin_robot_plane"])
    infile.close()

print("Starting program")

def getResults(BoxCom = 'init'):
    slotRes, info, transceivers = Tbox.run(resultCheck = BoxCom)  # ao chamar isto, o pc passa a comunicar com a caixa de testes, e só sai daqui quando os testes terminam todos.
    # portanto, se isto termina é porque test done. entao podemos enviar diretamente o slot e o resultado
    if (info == 'TESTS RUNNING') or (info == 'TRANSCEIVERS MISSING'):
        info = 0
        return slotRes, info, transceivers
    else:
        info = 1
    # transforma o resultado no formato 1 ou 0
        for i in range(4):
            if slotRes['Slot '+str(i+1)] == 'PASS':
                slotRes['Slot '+str(i+1)] = 1
            elif slotRes['Slot '+str(i+1)] == 'FAIL':
                slotRes['Slot '+str(i+1)]  = 2
        return slotRes, info, transceivers

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))      # Bind to the port  
s.listen()              # Wait for client connection
c, addr = s.accept()    # Establish connection with client

getResults(BoxCom='init')

i=1 # for test purposes
j=1
transceivers = False
while True:

    try:
        msg = c.recv(1024)
        msg = msg.decode()

        if msg != '':
            print(f"Received: {msg}")
            if msg == "test done?":
                if transceivers == False:
                    #print("SOME Transceivers missing")
                    result, tdone, transceivers = getResults(BoxCom = 'start')
                else:
                    print("ALL Transceivers Inserted")
                    result, tdone, transceivers = getResults(BoxCom = 'check')
                
                # envia um para indicar que um teste acabou

                tuplo = (tdone,1)   # o 1 extra e porque o polyscope precisa ou nao funciona
                string = str(tuplo)
                string2 = string.encode()
                c.send(string2)
                print("Sent "+string)

            elif msg == "test position":

                slotn = 'Slot '+ str(i)
                print(slotn)

                if i == 1:
                    result, tdone, transceivers = getResults(BoxCom = 'check')
                    tuplo = (36,12.57,result[slotn])
                elif i == 2:
                    tuplo = (86,12.56,result[slotn])
                elif i == 3:
                    tuplo = (136,12.56,result[slotn])
                else:
                    tuplo = (186,12.56,result[slotn])
                string = str(tuplo)
                print(string)
                string2 = string.encode()
                c.send(string2)  #mandar o X, Y e o resultado do teste 1 para OK e 2 para NOK
                print("Sent "+string)
                print("i = " +str(i))
                i = i+1

            elif msg == 'take xfp photo':
                sleep(2)
                ret, frame = cam.read()
                assert ret # check if we got a frame
                
                # frame_undistorted = Calculate_camera_points.undistor_image(frame, calibration_file)     # Undistor the image we want to analyse
                detector = Extract_points_of_yolo.XFP(frame, model)                                     # Create a new object to identify XFPs
                center_x, center_y, angle_rad, info = detector()
                print('info:' +str(info))                                       # Use the call function of the object
                xfp_side=2.0

                if info != []:
                    if info[0][0]=='XFP_front':
                        xfp_side = 1.0 #front
                    elif info[0][0]=='XFP_back':
                        xfp_side = 2.0 #back
                    else:
                        xfp_side = 3.0 #on its side
                
                # Indice 0 is for when we identified more than one XFP, only catch the first one
                if center_x == []: # It means yolo couldn't find any device
                    print("Couldn't find anything with yolo")
                    tuplo = ()
                    string = str(tuplo)
                    string = string.encode()
                    c.send(string)
                    # Robot should move a bit to the side or something
                else:
                    x_point_to_robot, y_point_to_robot = Calculate_camera_points.yolo_point_to_robot_plane((center_x[0], center_y[0]), square_pixel_size, angle_between_axis, origin_robot_plane, square_size_m)
                    tuplo = (x_point_to_robot, y_point_to_robot, angle_rad[0] + math.pi/2,xfp_side,0.0)
                    string = str(tuplo)
                    string = string.encode()
                    c.send(string)
                    print(f"Sent: {tuplo}")
                cam.release()
                cam = cv2.VideoCapture(capture_index, cv2.CAP_DSHOW)    #Create video stream
                if not cam.isOpened():
                    cam.release()
                    cam =  cv2.VideoCapture(capture_index, cv2.CAP_DSHOW)    #Create video stream
            elif msg == 'find_free_port':
                if j == 1:
                    tuplo = (36,12.56)
                elif j == 2:
                    tuplo = (86,12.56)
                elif j == 3:
                    tuplo = (136,12.56)
                else:
                    tuplo = (186,12.56)
                string = str(tuplo)
                print(string)
                string2 = string.encode()
                c.send(string2)  #mandar o X, Y e o resultado do teste 1 para OK e 2 para NOK
                print("Sent "+string)
                j = j+1
            if i == 5:
               i=1
            if j == 5:
                j=1
                #time.sleep(1)
        else:
            print(f"! Polyscope program was stopped ! Ctrl+C on the terminal, Reboot the system")
            sleep(5)
    except socket.error as socketerror:
        break

s.close()
c.close()

