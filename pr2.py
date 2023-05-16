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

import math

# Funkcja wyznaczająca punkty przecięcia prostej z okręgiem
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

# Przykładowe wywołanie funkcji
line = (1, 0, 0)
center = (0.0, 0.0)
radius = 0.7

points = intersection_points(line, center, radius)
print(points)
