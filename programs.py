from commands import *

def prog1(robot):

    move_pos_lin(robot, "nad_klocek")
    move_pos_lin(robot, "klocek")
    time.sleep(0.5)
    robot.close_grip()
    move_pos_lin(robot, "nad_klocek")

    move_pos_lin(robot, "nad_klocek1")
    move_pos_lin(robot, "klocek1")
    time.sleep(0.5)
    robot.open_grip()
    move_pos_lin(robot, "nad_klocek1")

    
def prog2(robot):
    pass
def prog3(robot):
    pass
def prog4(robot):
    pass
