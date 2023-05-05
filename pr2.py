# from urx import Robot

# # ustawienie adresu IP robota
# robot = Robot("192.168.0.152")

# # prędkość ruchu końcówki robota (w mm/s)
# vel = 0.1

# # ruch liniowy o 100mm wzdłuż osi X
# robot.movej([1, -1.57, 1, -1.57, 0, 0], vel=vel, wait=True)

# # ruch liniowy o 100mm wzdłuż osi Y
# robot.movej([0, -1.57, 1, -1.57, 0, 0], vel=vel, wait=True)

# # zakończenie połączenia z robotem
# robot.close()

# err = (5.7044874205769425e-05, 1.0061057092993289, 6.096499105631703e-05, 0.00010894102411462825, 3.40422508543492e-07, 3.864880131614762e-05)
# if err < (0.001, 0.001, 0.001, 0.001, 0.001, 0.001):
#     print("True")
# else:
#     print("False")

