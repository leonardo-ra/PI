import sys
sys.path.append('C:\\Users\\User\\Desktop\\PIC\\PIC\\Robô final\\PI\\Modulous')
import math
import socket
import torch
import Extract_points_of_yolo
import cv2
import Calculate_camera_points
import json
from time import sleep
import sys
from Comms_Test_Box import TestBoxComms as Tbox
import argparse
import sys
import select

class robot:
    def __init__(self, arg1, arg2, arg3, arg4, arg5):
        self.model_catch, self.model_box = self.load_model()            # Load yolo models, to catch XFP and for the test box
        self.HOST = arg1                                                # The remote host IP
        self.PORT = arg2                                                # The same port as used by the server
        self.capture_index = arg3                                       # Index of camera we want to access
        self.calibration_file = arg4                                    # Calibration file name to calibrate XFP catch
        self.square_size_in_m = arg5                                    # Size of chess square in meters
        self.transceivers = False
        self.i = 1                                                      # For test purposes
        self.j = 1                                                      # For test purposes
        self.cam = cv2.VideoCapture(self.capture_index, cv2.CAP_DSHOW)  # Create video stream
        self.cam.set(cv2.CAP_PROP_AUTOFOCUS, 0)  #Turn the autofocus off
        self.cam.set(3, 1280)
        self.cam.set(4, 720)
        self.cam.set(cv2.CAP_PROP_FPS, 60)
        self.photo = None                                               # Initialyze variable as None = no photo taken

    def load_model(self):
        model1 = torch.hub.load(r'C:\Users\User\Desktop\PIC\PIC\Robô final\Final2\yolov5', 'custom', path=r'C:\Users\User\Desktop\PIC\PIC\Robô final\Final2\yolov5\models\best (1).pt', source='local')
        model2 = torch.hub.load(r'C:\Users\User\Desktop\PIC\PIC\Robô final\Final2\yolov5', 'custom', path=r'C:\Users\User\Desktop\PIC\PIC\Robô final\Final2\yolov5\models\best_box2.pt', source='local')
        return model1, model2

    def initial_calibration(self):
        print("Start Calibration")
        calib_image = cv2.imread('./Big/frame0.jpg')
        # With a calibration photo of the board
        self.square_pixel_size, self.angle_between_axis, self.origin_robot_plane = Calculate_camera_points.Find_Corner_Chessboard(calib_image)
        dic = {"square_pixel_size": self.square_pixel_size, "angle_between_axis": self.angle_between_axis, "origin_robot_plane": str(self.origin_robot_plane)}
        with open("calib_parameters.json", "w") as outfile:
            json.dump(dic, outfile)                        # Write calib parameters to json file
        outfile.close()
        print("Calibration finished!")

    def load_calibration(self):
        try:
            with open("calib_parameters.json", "r") as infile:
                json_object = json.load(infile)                 # Read calib parameters from json file
                self.square_pixel_size = json_object["square_pixel_size"]
                self.angle_between_axis = json_object["angle_between_axis"]
                self.origin_robot_plane = eval(json_object["origin_robot_plane"])
            infile.close()
            print("No calibration made! Variables loaded from json file")
        except FileNotFoundError:
            print("ERROR: The file you are trying to access was not found.")
            sys.exit(1)

    def message_to_send(self, tuplo):
        string = str(tuplo)
        string2 = string.encode()
        self.conn.send(string2)
        print("Sent: " + string)    

    def take_photo(self):
        self.photo = None
        ret, self.photo = self.cam.read()
        if not ret:
            print("Error: Could not take photo.")
            self.photo = None
        else:
            print("Photo taken.")

    def robot_communication(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((self.HOST, self.PORT))                              # Bind to the port  
        s.listen()                                                  # Wait for client connection
        print("Listening for incoming connections")
        self.conn, addr = s.accept()                                        # Establish connection with client
        print(f"Connection established with {addr}")

    def getResults(self, BoxCom = 'init'):
        self.slotRes, self.info, self.transceivers = Tbox.run(resultCheck = BoxCom)  # PC starts to communicate with test box and only stops when all the test have finished.
        if (self.info == 'TESTS RUNNING') or (self.info == 'TRANSCEIVERS MISSING'):
            self.info = 0
        else:
            self.info = 1
        # Change result to 1 ("Pass") or to 0 ("Fail")
            for k in range(4):
                if self.slotRes['Slot '+str(k+1)] == 'PASS':
                    self.slotRes['Slot '+str(k+1)] = 1
                elif self.slotRes['Slot '+str(k+1)] == 'FAIL':
                    self.slotRes['Slot '+str(k+1)]  = 2

    def test_done_function(self):
        if self.transceivers == False:
            #print("SOME Transceivers missing")
            self.getResults(BoxCom = 'start')
        else:
            print("ALL Transceivers Inserted")
            self.getResults(BoxCom = 'check')
        
        # Send 1 to indicate that the test finished

        tuplo = (self.info, 1)   # Extra 1 because of requirements of Polyscope
        self.message_to_send(tuplo)

    def test_position_function(self):
        slotn = 'Slot '+ str(self.i)
        print(slotn)

        if self.i == 1:
            self.getResults(BoxCom = 'check')
            tuplo = (36,12.57,self.slotRes[slotn])
        elif self.i == 2:
            tuplo = (86,12.56,self.slotRes[slotn])
        elif self.i == 3:
            tuplo = (136,12.56,self.slotRes[slotn])
        else:
            tuplo = (186,12.56,self.slotRes[slotn])

        self.message_to_send(tuplo)
        print("i = " + str(self.i))
        self.i = self.i+1

    def catch_xfp_function(self):
        self.take_photo()
        # frame_undistorted = Calculate_camera_points.undistor_image(frame, calibration_file)   # Undistor the image we want to analyse
        detector = Extract_points_of_yolo.XFP(self.photo, self.model_catch)                     # Create a new object to identify XFPs
        center_x, center_y, angle_rad, info = detector()                                        # Use the call function of the object
        xfp_side=2.0

        # Indice 0 is for when we identified more than one XFP, only catch the first one
        if info:
            if info[0][0]=='XFP_front':
                xfp_side = 1.0 # front
            elif info[0][0]=='XFP_back':
                xfp_side = 2.0 # back
            else:
                xfp_side = 3.0 # on its side
           
        if center_x == []: # It means yolo couldn't find any device
            print("Couldn't find anything with yolo")
            tuplo = ()
            self.message_to_send(tuplo)
        else:
            x_point_to_robot, y_point_to_robot = Calculate_camera_points.yolo_point_to_robot_plane((center_x[0], center_y[0]), self.square_pixel_size, self.angle_between_axis, self.origin_robot_plane, self.square_size_in_m)
            tuplo = (x_point_to_robot, y_point_to_robot, angle_rad[0] + math.pi/2, xfp_side, 0.0)
            self.message_to_send(tuplo)

        cv2.destroyAllWindows()

    def free_port_function(self):
        if self.j == 1:
            tuplo = (36,12.56)
        elif self.j == 2:
            tuplo = (86,12.56)
        elif self.j == 3:
            tuplo = (136,12.56)
        else:
            tuplo = (186,12.56)
        self.message_to_send(tuplo)
        self.j = (self.j + 1) % 5

    def main(self):
        """
        Initial Calibration to catch XFP
        """
        calib = input('Do you wish to do Calibration? (Y/N)')
        if calib == 'Y' or calib == 'y' or calib == '':
            self.initial_calibration()
        else:
            self.load_calibration()

        """
        Start connection with robot Polyscope
        """
        print("--------------------------------Starting program----------------------------------------")
        self.robot_communication()
        self.getResults(BoxCom='init')

        while True:
            try:
                ready, _, _ = select.select([self.conn], [], [], 3600)
                if ready:
                    data = self.conn.recv(1024)
                    message = data.decode()
                    if message:
                        print(f"Received message: {message}")
                        if message == "test done?":
                            self.test_done_function()
                        elif message == "test position":
                            self.test_position_function()
                        elif message == "take xfp photo":
                            self.catch_xfp_function()
                        elif message == "find_free_port":
                            self.free_port_function()
                        if self.i == 5:
                            self.i = 1
                        if self.j == 5:
                            self.j = 1
                    else:
                        print("! Polyscope program was stopped ! Ctrl+C on the terminal, Reboot the system")
                        sleep(5)
            except socket.error as socketerror:
                print("Error: ", socketerror)
                break
            
            sleep(0.1) # Pauses the execution of the script for 0.1 seconds, to avoid overloading the server.

        self.conn.close()  # Closes connection with the robot

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    
    # Add command-line arguments
    parser.add_argument("-hp", "--host_ip", type=str, help="Host IP used to make TCP connection to the robot polyscope", default="192.1.1.2")
    parser.add_argument("-port", "--port", type=int, help="Port used to make TCP connection to the robot polyscope", default=6000)
    parser.add_argument("-cam_ind", "--camera_index", type=int, help="Index of camera we want to access", default=1)
    parser.add_argument("-calib_file", "--calibration_file", type=str, help="Calibration file name to calibrate XFP catch", default= "camera_image_small.npz")
    parser.add_argument("-squ_size", "--square_size_in_m", type=float, help="Size of chess square in meters", default=0.05029)
    # Parse command-line arguments
    args = vars(parser.parse_args())
    
    # Create an instance of the program and run the main method
    program = robot(args["host_ip"], args["port"], args["camera_index"], args["calibration_file"], args["square_size_in_m"])
    program.main()