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
        time.sleep(1)
        robot.move_to_pose(PRZED, v=0.05)
        while not is_on_place(robot, PRZED):
            print("5")
            time.sleep(0.1)

def uchwyt_przesuw1(robot, p):
    print(robot.is_on_base)
    if robot.is_on_base:
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
        release_brake(robot)
        time.sleep(1)
        trans = (0.0, p, 0.0, 0.0, 0.0, 0.0)
        pos = add_or_subtract_tuples(check_position(robot),trans,"+")
        robot.move_to_pose_linear(pos, v=0.05)
        while not is_on_place(robot, pos):
            print("5")
            time.sleep(0.1)
        time.sleep(1)
        set_brake(robot)
        time.sleep(1)
        trans = (-0.1, 0.0, 0.0, 0.0, 0.0, 0.0)
        pos = add_or_subtract_tuples(check_position(robot),trans,"+")
        robot.move_to_pose_linear(pos, v=0.05)
        while not is_on_place(robot, pos):
            print("6")
            time.sleep(0.1)
        time.sleep(1)
        trans = (0.1, 0.0, 0.0, 0.0, 0.0, 0.0)
        pos = add_or_subtract_tuples(check_position(robot),trans,"+")
        robot.move_to_pose_linear(pos, v=0.05)
        while not is_on_place(robot, pos):
            print("7")
            time.sleep(0.1)
        time.sleep(1)
        release_brake(robot)
        time.sleep(1)
        trans = (0.0, -p, 0.0, 0.0, 0.0, 0.0)
        pos = add_or_subtract_tuples(check_position(robot),trans,"+")
        robot.move_to_pose_linear(pos, v=0.05)
        while not is_on_place(robot, pos):
            print("8")
            time.sleep(0.1)
        time.sleep(1)
        set_brake(robot)
        time.sleep(1)
        trans = (-0.1, 0.0, 0.0, 0.0, 0.0, 0.0)
        pos = add_or_subtract_tuples(check_position(robot),trans,"+")
        robot.move_to_pose_linear(pos, v=0.05)
        while not is_on_place(robot, pos):
            print("9")
            time.sleep(0.1)


def uchwyt_przesuw(robot, p):
    print(robot.is_on_base)
    cart_trans = -robot.cart_trans
    ### pozycje przed przejazdem
    gora = add_or_subtract_tuples(GORA, (0.0, cart_trans, 0.0, 0.0, 0.0, 0.0),"+")
    przed = add_or_subtract_tuples(PRZED, (0.0, cart_trans, 0.0, 0.0, 0.0, 0.0),"+")
    uchwyt = add_or_subtract_tuples(UCHWYT, (0.0, cart_trans, 0.0, 0.0, 0.0, 0.0),"+")
    if robot.is_on_base:
        robot.move_to_pose(gora, v=0.2)
        robot.move_to_pose(przed, v=0.2)
        print("2")
        while not is_on_place(robot, przed):
            print("3")
            time.sleep(0.1)
        robot.move_to_pose(uchwyt, v=0.05)
        while not is_on_place(robot, uchwyt):
            print("4")
            time.sleep(0.1)
        release_brake(robot)
        time.sleep(1)

        ### pozycje po przejeździe
        gora = add_or_subtract_tuples(GORA, (0.0, cart_trans+p, 0.0, 0.0, 0.0, 0.0),"+")
        przed = add_or_subtract_tuples(PRZED, (0.0, cart_trans+p, 0.0, 0.0, 0.0, 0.0),"+")
        uchwyt = add_or_subtract_tuples(UCHWYT, (0.0, cart_trans+p, 0.0, 0.0, 0.0, 0.0),"+")
        robot.move_to_pose_linear(uchwyt, v=0.05)
        while not is_on_place(robot, uchwyt):
            print("5")
            time.sleep(0.1)
        time.sleep(1)
        set_brake(robot)
        time.sleep(1)
        robot.move_to_pose_linear(przed, v=0.05)
        while not is_on_place(robot, przed):
            print("5")
            time.sleep(0.1)
        robot.cart_trans=cart_trans+p