from rtde_control import RTDEControlInterface as RTDEControl
from rtde_receive import RTDEReceiveInterface as RTDEReceive
from rtde_io import RTDEIOInterface as RTDEIO
from enum import IntEnum


import time



class Robot(RTDEControl, RTDEReceive, RTDEIO):  #This is a constructor class that applies the same IP to the three RTDE: Control (to send info), Receive (to receive info) and IO (to later control the gripper))
    def __init__(self, ip):                     #Initializes the three with the same IP address.
        RTDEControl.__init__(self, ip, RTDEControl.FLAG_CUSTOM_SCRIPT) #This 'Flag' allows us to controll the gripper externally, it can also be the RTDEControl.FLAG_CUSTOM_SCRIPT. Both methods will load the preamble of the Gripper UR Cap that we are using, so that you can call them gripper script commands from this rtde_control script.
        RTDEReceive.__init__(self, ip)          #Receive info 
        RTDEIO.__init__(self, ip)               # 


robot = Robot("192.1.1.1")
print("now moving the gripper")
robot.twofg_grip_ext(20, 30, 20)