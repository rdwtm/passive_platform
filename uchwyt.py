from utils import *
HOME_POSITION_CONF =[0, -1.57, 1.57, -1.57, -1.57, 0]
GORA = [-0.56681, -0.33716, 0.29092, 2.228, 2.210, -0.015]
PRZED = [-0.53584, -0.33664, -0.04871, 2.211, 2.214, -0.022]
UCHWYT = [-0.44426, -0.33662, -0.04893, 2.211, 2.214, -0.022]

def uchwyt(robot):
    if not krancowka(robot):
        print("1")
        robot.move_to_pose(GORA, v=0.05)
        robot.move_to_pose(PRZED, v=0.05)
        print("2")
        while not is_on_place(robot, PRZED):
            print("3")
            time.sleep(0.1)
        robot.move_to_pose(UCHWYT, v=0.05)
        while not is_on_place(robot, UCHWYT):
            print("4")
            time.sleep(0.1)
        robot.move_to_pose(PRZED, v=0.05)
        while not is_on_place(robot, PRZED):
            print("5")
            time.sleep(0.1)


