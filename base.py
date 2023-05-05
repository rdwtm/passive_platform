from utils import *
import time
HOME_POSITION_CONF =[0, -1.57, 1.57, -1.57, -1.57, 0]
BASE_1_POSE = [-0.42, 0.5, 0.21766859736020782, 3.0911890504964474, 0.10019958260730014, -0.03245276753244325]
BASE_2_POSE = [-0.42, 0.5, 0.14, 3.0911890504964474, 0.10019958260730014, -0.03245276753244325]

def bazowanie(robot):

    set_brake(robot)
    if krancowka(robot):
        if not is_on_place(robot, tuple(BASE_2_POSE)):
            robot.move_to_configuration(HOME_POSITION_CONF,v=0.5)
            robot.move_to_pose(BASE_1_POSE, v=0.5)
            robot.move_to_pose(BASE_2_POSE, v=0.5)
            
        a = 0

        while not is_on_place(robot, tuple(BASE_2_POSE)):
            time.sleep(0.1)
            print("dojazd")
        kr = krancowka(robot)
        pose = check_position(robot)
        print("krańcówka " + str(kr))
        release_brake(robot)

        while krancowka(robot) == 1:
            dalej = is_on_place(robot, pose)
            print("dalej " + str(dalej))
            # pose = robot.tool_position
            if dalej:
                if distance(robot, -0.27743996273586136) < 0.03:
                    vel = 0.01
                    step = (0.0,-0.001,0.0,0.0,0.0,0.00)
                if distance(robot, -0.27743996273586136) < 0.1:
                    vel = 0.03
                    step = (0.0,-0.01,0.0,0.0,0.0,0.00)
                else:
                    vel = 0.5
                    step = (0.0,-0.1,0.0,0.0,0.0,0.00)
                print("krańcówka " + str(kr))
                pose = add_or_subtract_tuples(check_position(robot), step,'+')
                # print(robot._tool_position)
                print(pose)
                print("a"+str(a))
                print(distance(robot, -0.27743996273586136))
                
                robot.move_to_pose(pose, v=vel, a=0.1)
                a+=1
                time.sleep(0.001)
            kr = krancowka(robot)
        # print("krańcówka " + str(kr))
        time.sleep(0.5)
        set_brake(robot)
        time.sleep(0.5)
        set_brake(robot)
        pose = add_or_subtract_tuples(check_position(robot), (0.0, 0.05, 0.0, 0.0, 0.0, 0.0),'+')
        robot.move_to_pose(pose, v=0.5, a=0.5)
        time.sleep(0.1)
        pose = add_or_subtract_tuples(check_position(robot), (0.0, 0.0, 0.1, 0.0, 0.0, 0.0),'+')
        robot.move_to_pose(pose, v=0.5, a=0.5)
    time.sleep(0.5)
    set_brake(robot)
    time.sleep(0.5)
    set_brake(robot)
    robot.move_to_configuration(HOME_POSITION_CONF,v=0.5)
    # while not is_on_place(robot, tuple(HOME_POSITION_CONF)):
    #     time.sleep(0.1)
    robot.is_on_base = True
    robot.cart_trans = 0
    print("zakończono bazowanie")
    return
