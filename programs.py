from commands import *

def prog1(robot):
    time.sleep(5)
    move_pos_lin(robot, "nad_klocek")
    move_pos_lin(robot, "klocek")
    time.sleep(0.5)
    move_pos_lin(robot, "nad_klocek")

    move_pos_lin(robot, "nad_klocek2")
    move_pos_lin(robot, "klocek2")
    time.sleep(0.5)
    move_pos_lin(robot, "nad_klocek2")


    move_pos_lin(robot, "nad_klocek3")
    move_pos_lin(robot, "klocek3")
    time.sleep(0.5)
    move_pos_lin(robot, "nad_klocek3")


    
def prog2(robot):
    pass
def prog3(robot):
    pass
def prog4(robot):
    pass
