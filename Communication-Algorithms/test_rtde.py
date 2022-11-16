from rtde_control import RTDEControlInterface
from rtde_receive import RTDEReceiveInterface
from rtde_io import RTDEIOInterface
from enum import IntEnum

import time

"""
Connect to robot and move to the first positon
"""
inputs=RTDEIOInterface("192.1.1.1")
rtde_c = RTDEControlInterface("192.1.1.1",RTDEControlInterface.FLAG_USE_EXT_UR_CAP)
rtde_c.moveJ([3.22, -1.53, -1.04, -2.11, 1.57, 0.06], 1, 0.5)
rtde_r = RTDEReceiveInterface("192.1.1.1")
actual_q = rtde_r.getActualQ()
print(actual_q)
#inputs.read_input_integer_register(18,1)
#if inputs.read_input_integer_register(18) == 1:
rtde_c.twofg_grip_ext(13, 50, 10)
#elif inputs.read_input_integer_register(18) == 2:
rtde_c.twofg_grip_int(13, 50, 10)

