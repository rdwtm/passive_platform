from urx import Robot

# ustawienie adresu IP robota
robot = Robot("192.168.0.152")

# prędkość ruchu końcówki robota (w mm/s)
vel = 0.1

# ruch liniowy o 100mm wzdłuż osi X
robot.movej([1, -1.57, 1, -1.57, 0, 0], vel=vel, wait=True)

# ruch liniowy o 100mm wzdłuż osi Y
robot.movej([0, -1.57, 1, -1.57, 0, 0], vel=vel, wait=True)

# zakończenie połączenia z robotem
robot.close()
