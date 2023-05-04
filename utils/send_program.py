from ur_control import Robot

# Adres IP robota UR5
robot_host = "192.168.0.10"

# Nazwa programu, który ma zostać uruchomiony na robocie
program_name = "nazwa_programu.urp"

# Utworzenie obiektu reprezentującego robota
robot = Robot(robot_host)

# Uruchomienie programu na robocie
robot.send_program(program_name)

# Zamknięcie połączenia z robotem
robot.close()