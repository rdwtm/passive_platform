# import json
# import socket
# import time

# def send_play(sock):
#     play_cmd = "play\n"
#     sock.sendall(bytes(play_cmd, 'utf-8'))

# def set_freedrive(sock):
#     freedrive_on = "def myProg():\n  set_standard_analog_input_domain(0, 0)\n  set_tool_digital_out(0, False)\n  set_analog_outputdomain(0, 0)\n  set_freedrive(1)\n  loop = 1\n  while loop == 1:\n    sync()\n  end\nend\n"
#     sock.sendall(bytes(freedrive_on, 'utf-8'))

# # adres IP i port robota
# HOST = '192.168.0.152'
# PORT = 30003

# # komenda do pobrania aktualnej pozycji
# # command = "def get_current_position():\n  return get_actual_tcp_pose()\n"
# command = "movej([0, -1.57, 0, 1, 0, 0], a=0.1, v=0.1)\n"

# # utworzenie połączenia z robotem
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.connect((HOST, PORT))
# time.sleep(1)
# # print(s.getsockname())
# # print(s.getpeername())

# # wysłanie komendy do robota
# s.send(command.encode())
# # time.sleep(5)
# set_freedrive(s)
# send_play(s)
# print("freedrive!!!")

# time.sleep(20)

# # odczytanie odpowiedzi od robota
# # response = s.recv(1140)

# # zamknięcie połączenia
# s.close()
# # print(repr(response))
# # # print(response.decode().splitlines()[-2])

import socket
import struct

HOST = "192.168.0.152" # adres IP robota
PORT = 33333 # port używany przez interfejs użytkownika UR

# utworzenie socketu i połączenie z robotem
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

# wysłanie komendy do robota
# s.send("sec io_in ()\n".encode())

# odbiór danych zwrotnych od robota
data = s.recv(1)
print(data)
# interpretacja danych zwrotnych jako listy bitów
bits = struct.unpack(">III", data[0:12])[:]
print(bits)
# # wyświetlenie stanu wejść cyfrowych
# print("Stan wejść cyfrowych: ")
# print("Input 0: ", bool(bits & 1))
# print("Input 1: ", bool(bits & 2))
# print("Input 2: ", bool(bits & 4))
# print("Input 3: ", bool(bits & 8))

# zamknięcie połączenia
s.close()