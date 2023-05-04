import json
import os
import socket

def save_program():
    program = input("Enter program in URScript: ")

    # Save program to file
    with open("program.urp", "w") as f:
        f.write(program)

    # Get robot IP address
    with open("robot_info.json", "r") as f:
        robot_info = json.load(f)
    robot_ip = robot_info["ip"]

    # Send program to robot
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((robot_ip, 30002))
    with open("program.urp", "rb") as f:
        program_data = f.read()
    sock.send(program_data)
    sock.close()

    print("Program saved and sent to robot.")
