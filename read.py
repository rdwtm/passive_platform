import socket
import struct

# adres IP i port robota
HOST = '192.168.0.152'
PORT = 30003

# komenda do pobrania aktualnej pozycji
# command = "def get_current_position():\n  return get_actual_tcp_pose()\n"
command = "movel([0, -1.57, 0, 0, 0, 0], a=0.1, v=0.1)"

# utworzenie połączenia z robotem
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

while True:
    msg = s.recv(1140)
    msg_size = struct.unpack('>i', msg[0:4])[0]
    print(f"rozmiar: {msg_size}")
    q_target = struct.unpack('>d', msg[12:20])[0]
    actual = struct.unpack('>dddddd', msg[252:300])[:]
    print(f"target: {q_target}")
    print(f"actual: {actual}")