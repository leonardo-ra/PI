from rtde_control import RTDEControlInterface
from rtde_receive import RTDEReceiveInterface
from rtde_io import RTDEIOInterface
from enum import IntEnum

import time

"""
Connect to robot and move to the first positon
"""
rtde_c = RTDEControlInterface("192.1.1.1")
rtde_c.moveJ([3.22, -1.53, -1.04, -2.11, 1.57, 0.06], 1, 0.3)
#rtde_c.moveJ([184.5 , -79.13, -101.70, -87.13, 90.05, 3.65]) (MAIS PROXIMO DO XFP)
#rtde_c.moveJ([-47.91, -41.47, 95.77, -53.86, 40.57, 180.15]) (JUNTO À CAIXA em paralelo com a mesa)
rtde_r = RTDEReceiveInterface("192.1.1.1")
actual_q = rtde_r.getActualQ()
print(actual_q)