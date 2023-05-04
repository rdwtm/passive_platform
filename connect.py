from ur_interface import URInterface
import time
path = "/home/we043/Radek/passive_platform/urscripts/cb3_8.ur"
with open(path, 'r') as f:
    file = f.read()
robot = URInterface.URInterface("192.168.0.152", 33333, 30003, 30013, file)
# print(robot)
robot.connect()
time.sleep(1)
robot.move_to_configuration([0, -1.57, 1.57, -1.57, -1.57, 0],v=0.2)
robot.move_to_pose([-0.39923568462864895, 0.752126277040094, 0.21766859736020782, 3.0911890504964474, 0.10019958260730014, -0.03245276753244325], v=0.2)
# robot.move_to_pose([-0.4265037309929893, -0.13188608749153627, 0.48758354970353424, -2.2216767035626788, -2.218647337645324, -0.004606962893893158], v=0.2)
# robot.move_to_configuration([-1.2430513540851038, -0.4791819614223023, 0.8352010885821741, -1.8864528141417445, -1.530928913746969, 0.2626086473464966],v=0.2)




def add_or_subtract_tuples(a, b, op='+'):
    if op == '+':
        return tuple(x + y for x, y in zip(a, b))
    elif op == '-':
        return tuple(x - y for x, y in zip(a, b))
    else:
        raise ValueError('Invalid operator: {}. Use "+" or "-".')

def is_on_place(robot, point):
    err = add_or_subtract_tuples(robot.tool_position, point, "-")
    err = tuple(map(abs, err))
    print ("error"+str(err))
    if err < (0.001,0.001,0.001,0.001,0.001,0.001):
        return True
    else:
        return False



# for i in range(1):
#     # print("joint" + str(robot.joint_positions))
#     # print(robot.robot_connected)
#     # print(robot.robot_enabled)
#     # print(robot.robot_power)

#     # print("inputs" + s[26])
#     # print(robot.digital_outputs)

#     # print("tool" + str(robot._tool_position))

time.sleep(0.01)
def bazowanie(robot):
    a = 0
    while not is_on_place(robot, (-0.39923568462864895, 0.752126277040094, 0.21766859736020782, 3.0911890504964474, 0.10019958260730014, -0.03245276753244325)):
        time.sleep(0.1)
    i = int.from_bytes(robot.digital_inputs, byteorder='big')
    s = bin(i)[2:]
    pose = robot._tool_position

    while int(s[26]) == 1:
        if is_on_place(robot, pose):
            
            pose = add_or_subtract_tuples(pose, (0.0,-0.01,0.0,0.0,0.0,0.00),'+')
            print(robot._tool_position)
            print(pose)
            print(a)
            robot.move_to_pose(pose, v=0.05)
            a+=1

bazowanie(robot)







