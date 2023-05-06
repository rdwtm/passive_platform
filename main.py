from connect import *
from utils import *
from base import *
from uchwyt import *
from set_positions import *
from commands import *
import os
import socket
import inspect
import programs
# robot = connect()
# if not robot.connected:
#     print("connect failure")

# bazowanie(robot)

# print("zbazowany")
# uchwyt(robot)
# uchwyt_przesuw(robot, 0.1)
# save_position(robot, "settings.json")
# save_position(robot)
# klocek = get_positions(name="klocek")
# nad_klockiem = add_or_subtract_tuples(klocek,  (0.0, 0.0, 0.1, 0.0, 0.0, 0.0),'+')
# robot.move_to_pose(nad_klockiem, v=0.2)
# robot.move_to_pose_linear(klocek, v=0.2)
# time.sleep(3)
# robot.move_to_pose(nad_klockiem, v=0.2)


# uchwyt_przesuw(robot, 0.1)

# print(robot.cart_trans)
# klocek = add_or_subtract_tuples(klocek,  (0.0, robot.cart_trans, 0.0, 0.0, 0.0, 0.0),'+')
# nad_klockiem = add_or_subtract_tuples(klocek,  (0.0, 0.0, 0.1, 0.0, 0.0, 0.0),'+')
# robot.move_to_pose(nad_klockiem, v=0.2)
# time.sleep(1)
# robot.move_to_pose_linear(klocek, v=0.2)
# time.sleep(1)
# robot.move_to_pose(nad_klockiem, v=0.2)
# time.sleep(1)



# Import necessary libraries
import time

# Define the functions
def connect_to_robot():
    global robot 
    os.system('clear')
    print("Connecting to the robot...")
    robot = connect()
    if not robot.connected:
        print("connect failure")
    print("Connection established.")

def home():
    os.system('clear')
    if not robot.connected:
        print("Please connect to the robot first.")
    else:
        print("Homing the robot...")
        bazowanie(robot)
        print("Robot has been homed.")
        robot.is_on_base

def move_to_position():
    os.system('clear')
    # if not robot.is_on_base:
    #     print("Please home the robot first.")
    # else:
    #     position = input("Enter the desired position: ")
    #     print("Moving robot to position", position)
    #     move_pos_lin(robot, position)
    #     print("Robot has reached position", position)
    robot.open_grip()

def save_pos():
    os.system('clear')
    # if not robot.is_on_base:
    # #     print("Please home the robot first.")
    # else:
    save_position(robot)
    

def run_program():
    os.system('clear')
    if not robot.is_on_base:
        print("Please home the robot first.")
    else:
        print("Running the program...")
        # uzyskaj listę nazw funkcji w module
        # functions_list = [name for name, obj in inspect.getmembers(programs) if inspect.isfunction(obj)]
        functions_list = [name for name, obj in inspect.getmembers(programs) if inspect.isfunction(obj) and obj.__module__ == programs.__name__]

        # wyświetl listę funkcji
        print("Available functions:")
        for i, function_name in enumerate(functions_list):
            print(f"{i+1}. {function_name}")

        # poproś użytkownika o wybór funkcji i jej parametrów
        choice = int(input("Enter the number of the function you want to use: "))
        function_name = functions_list[choice - 1]
        # function_args = input("Enter the function arguments separated by commas. Speed olny yet: ").split(",")

        # uzyskaj funkcję po nazwie
        function = getattr(programs, function_name)

        # wywołaj funkcję z odpowiednimi parametrami
        result = function(robot)

        # wyświetl wynik
        print(result)


        time.sleep(2)
        print("Program has finished.")

def move_to_cart_pos():
    os.system('clear')
    if not robot.is_on_base:
        print("Please home the robot first.")
    else:
        pos = float(input("Enter the desired cart position [m]: "))
        print("Moving robot to cart position", pos)
        uchwyt_przesuw(robot, pos)
        time.sleep(2)
        print("Robot has reached configuration", pos)

def move_gripper():
    inp = int(input('1 to close, 2 to open'))
    if inp == 1:
        robot.close_grip()
    if inp == 2:
        robot.open_grip() 

# Define the main function
def main():
    global robot
    robot = None
    while True:
        print("\nRobot Control Panel")
        print("--------------------")
        print("1. Connect to robot")
        print("2. Home")
        print("3. Move to position")
        print("4. Save position")
        print("5. Move to cart position")
        print("6. Run program")
        print("7. Move gripper")
        print("8. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            connect_to_robot()
            connected = True
        elif choice == "2":
            home()
        elif choice == "3":
            move_to_position()
        elif choice == "4":
            save_pos()
        elif choice == "5":
            move_to_cart_pos()
        elif choice == "6":
            run_program()
        elif choice == "7":
            move_gripper()
        elif choice == "8":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

# Call the main function
if __name__ == '__main__':
    main()
