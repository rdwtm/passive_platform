from utils import *
from uchwyt import *

def move_pos_lin(robot, pos, v=0.5, a=0.5):
    if type(pos) == str:
        position, transform = get_positions(name=pos)
    elif type(pos) == tuple:
        position = pos
    else:
        raise TypeError
    ret = transform_manager(robot, 'klocek')
    if ret != False:
        print('return :')
        print(ret)
        uchwyt_przesuw(robot, ret)
    print(position)
    position[1]-=(transform-robot.cart_trans)
    print(position)
    robot.move_to_pose_linear(position, v=v, a=a)
    while not is_on_place(robot, position):
        time.sleep(0.1)
    return


# def move_cart(robot, cart_pos):
