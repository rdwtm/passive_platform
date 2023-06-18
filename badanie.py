from main import connect_to_robot, home, move_to_cart_pos
import time 
import timeit
global robot
robot = None

connect_to_robot()
home()
# for i in range(5):
#     for i in range(1, 8, 1):
#         # Divide i by 10 to get the float value
#         float_value = i / 10.0
#         move_to_cart_pos(float_value)
#     for i in reversed(range(0, 7, 1)):
#         # Divide i by 10 to get the float value
#         float_value = i / 10.0
#         move_to_cart_pos(float_value)
lista = []
for i in range(1, 7, 1):
        float_value = i / 10.0
        start_time = time.time()
        move_to_cart_pos(float_value)
        end_time = time.time()
        execution_time1 = end_time - start_time
        start_time1 = time.time()
        move_to_cart_pos(0)
        end_time1 = time.time()
        execution_time2 = end_time1 - start_time1
        lista.append([execution_time1, execution_time2, float_value])

for el in lista:
    print(f"dla pozycji :{el[2]} czas do przodu: {el[0]}, czas do tyłu {el[1]}")