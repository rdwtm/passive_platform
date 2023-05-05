from utils import *
HOME_POSITION_CONF =[0, -1.57, 1.57, -1.57, -1.57, 0]
UCHWYT = get_positions("settings.json", "uchwyt")
PRZED = UCHWYT.copy()
PRZED[0] = PRZED[0]-0.2
GORA = PRZED.copy()
GORA[2] = GORA[2]+0.5

def uchwyt(robot):
    if not krancowka(robot):
        print("1")
        print(GORA)
        print(PRZED)
        print(UCHWYT)
        robot.move_to_pose(GORA, v=0.2)
        robot.move_to_pose(PRZED, v=0.2)
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


