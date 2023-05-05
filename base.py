from utils import *
import time
HOME_POSITION_CONF =[0, -1.57, 1.57, -1.57, -1.57, 0]
BASE_1_POSE = [-0.42, 0.5, 0.21766859736020782, 3.0911890504964474, 0.10019958260730014, -0.03245276753244325]
BASE_2_POSE = [-0.42, 0.5, 0.15, 3.0911890504964474, 0.10019958260730014, -0.03245276753244325]

def bazowanie(robot):
    set_brake(robot)
    if not is_on_place(robot, tuple(BASE_2_POSE)):
        robot.move_to_configuration(HOME_POSITION_CONF,v=0.5)
        robot.move_to_pose(BASE_1_POSE, v=0.5)
        robot.move_to_pose(BASE_2_POSE, v=0.5)
        # robot.move_to_pose([-0.4265037309929893, -0.13188608749153627, 0.48758354970353424, -2.2216767035626788, -2.218647337645324, -0.004606962893893158], v=0.2)
        # robot.move_to_configuration([-1.2430513540851038, -0.4791819614223023, 0.8352010885821741, -1.8864528141417445, -1.530928913746969, 0.2626086473464966],v=0.2)
    a = 0
    data=[]

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
                vel = 0.01
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
            time.sleep(0.1)
        kr = krancowka(robot)
    # print("krańcówka " + str(kr))
    time.sleep(0.5)
    set_brake(robot)
    time.sleep(0.5)
    set_brake(robot)
    set_brake(robot)
    robot.move_to_configuration(HOME_POSITION_CONF,v=0.5)
    print("asdf")
    # while not is_on_place(robot, (-0.39923568462864895, 0.752126277040094, 0.21766859736020782, 3.0911890504964474, 0.10019958260730014, -0.03245276753244325)):
    #     time.sleep(0.1)
    print("zakończono bazowanie")