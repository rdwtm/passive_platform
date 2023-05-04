import json
import socket
import time

# adres IP i port robota
HOST = '192.168.0.152'
PORT = 30003

# komenda do pobrania aktualnej pozycji
# command = "def get_current_position():\n  return get_actual_tcp_pose()\n"
command = "movej([1, -1.57, 0, 1, 0, 0], a=0.1, v=0.1)\n"

# utworzenie połączenia z robotem
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
time.sleep(1)
print(s.getsockname())
print(s.getpeername())

# wysłanie komendy do robota
s.send(command.encode())

# odczytanie odpowiedzi od robota
# response = s.recv(1140)

# zamknięcie połączenia
s.close()
# print(repr(response))
# # print(response.decode().splitlines()[-2])

