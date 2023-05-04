from ur_interface import URInterface
import time
path = "/home/we043/Radek/passive_platform/urscripts/cb3_8.ur"
with open(path, 'r') as f:
    file = f.read()
robot = URInterface.URInterface("192.168.0.152", 33333, 30003, 30013, file)
print(robot)
robot.connect()
# for i in range(50):
#     print(robot.joint_positions)
#     time.sleep(0.1)
robot.move_to_configuration_linear([0.2,0.2,0.2,0,0,0])
for i in range(50):
    print(robot.joint_positions)
    print(robot.robot_connected)
    print(robot.robot_enabled)
    print(robot.robot_power)
    print(robot.digital_inputs)
    print(robot.digital_outputs)
    print(robot._tool_position)

    time.sleep(0.1)

