from ur_interface import URInterface
import time
from base import *

def connect():
    path = "/home/we043/Radek/passive_platform/urscripts/cb3_8.ur"
    with open(path, 'r') as f:
        file = f.read()
    robot = URInterface.URInterface("192.168.0.152", 33333, 30003, 30013, file)
    robot.connect()
    time.sleep(1)
    return robot










