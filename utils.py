import time
import json
import math

def intersection_points(line, center, radius):
    a = line[0]
    b = line[1]
    c = line[2]

    x_c = center[0]
    y_c = center[1]

    # Obliczenie wartości delta
    delta = (2*a*x_c + 2*b*y_c + 2*c)**2 - 4*(a**2 + b**2)*(c**2 + y_c**2 + x_c**2 - radius**2)

    # Sprawdzenie, czy prosta przecina okrąg
    if delta < 0:
        print("Prosta nie przecina okręgu.")
        return []

    # Obliczenie punktów przecięcia
    x1 = (-2*a*x_c - 2*b*y_c - 2*c + math.sqrt(delta)) / (2*(a**2 + b**2))
    x2 = (-2*a*x_c - 2*b*y_c - 2*c - math.sqrt(delta)) / (2*(a**2 + b**2))
    return (x1, x2)


def add_or_subtract_tuples(a, b, op='+'):
    if op == '+':
        return tuple(x + y for x, y in zip(a, b))
    elif op == '-':
        return tuple(x - y for x, y in zip(a, b))
    else:
        raise ValueError('Invalid operator: {}. Use "+" or "-".')

def is_on_place(robot, point):
    err = add_or_subtract_tuples(check_position(robot), point, "-")
    err = tuple(map(abs, err))
    print ("error"+str(err))
    all_less_than_0_001 = True

    for val in err:
        if val >= 0.001:
            all_less_than_0_001 = False
            break

    if all_less_than_0_001:
        return True
    else:
        return False
    
def krancowka(robot):
    i = int.from_bytes(robot.digital_inputs, byteorder='big')
    s = bin(i)[2:]

    while str(s[0:18]) != str(100000011110000000):
        i = int.from_bytes(robot.digital_inputs, byteorder='big')
        s = bin(i)[2:]
        # print(s[26])
        # print(s)
    return int(s[26])

def set_DO(robot, id, state):
    robot.set_IO(id,state)

def set_brake(robot):
    set_DO(robot, 0, 1)
    time.sleep(1)
    set_DO(robot, 0, 0)
    time.sleep(0.5)

def release_brake(robot):
    set_DO(robot, 1, 1)
    time.sleep(1)
    set_DO(robot, 1, 0)
    time.sleep(0.5)

def check_position(robot):
    position = robot.tool_position
    # print("check:")
    while sum(position)>100:
        position = robot.tool_position
        print("bląd: " )
        print(position)
    return position

def distance(robot, position):
    pos=check_position(robot)[1]
    return abs(pos-position)

def get_positions(file = "positions.json", name=""):
    # otwarcie pliku i wczytanie zawartości do zmiennej
    with open(file, 'r') as f:
        positions = json.load(f)

    # przeszukanie listy pozycji w celu znalezienia pozycji o nazwie "position_1"
    for position in positions:
        if position['name'] == name:
            return position['tcp_pose'], position['translation']
        
def transform_manager(robot, pos):
    tcp_pose, transform = get_positions(name=pos)
    global_pos_y = tcp_pose[1]-transform
    # r = math.sqrt(pow(tcp_pose[0],2)+pow(transform-tcp_pose[1],2)+pow(tcp_pose[2],2))
    # # rmin = -1
    # # rmax = 1
    # # trmin = 0
    # # while rmin < -0.6:
    # #     rmin = trmin - r
    # #     trmin += 0.1
    # # trmax = 0.7
    # # while rmax > 0.6:
    # #     rmax = trmax - r
    # #     trmax -= 0.1
    
    # print(tcp_pose)
    # print(r)
    # trmin = -0.7 - r
    # trmax = 0.7 - r


    line = (1, 0, 0)
    center = (global_pos_y, 0.0)
    radius = 0.7

    points = intersection_points(line, center, radius)
    trmin = min(points)
    trmax = max(points)

    if trmin < 0:
        trmin = 0
    if trmax > 0.7:
        trmax = 0.7
    a = math.sqrt(pow(tcp_pose[0],2)+pow(-robot.cart_trans+transform-tcp_pose[1],2)+pow(tcp_pose[2],2))
    print (a)
    if a  < 0.8:
        print(robot.cart_trans)
        print(False)
        return False
    else:
        print(trmin)
        print(trmax)
        print(robot.cart_trans)
        print((trmin+trmax)/2)
        return (trmin+trmax)/2
    

    


      
