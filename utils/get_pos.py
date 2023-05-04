import json
import socket

def get_current_position():
    # adres IP i port robota
    HOST = '192.168.1.100'
    PORT = 30003

    # komenda do pobrania aktualnej pozycji
    command = "def get_current_position():\n  return get_actual_tcp_pose()\n"

    # utworzenie połączenia z robotem
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))

    # wysłanie komendy do robota
    s.send(command.encode())

    # odczytanie odpowiedzi od robota
    response = s.recv(1024)

    # zamknięcie połączenia
    s.close()

    # przetworzenie odpowiedzi na pozycję w formacie JSON
    position = json.loads(response.decode().splitlines()[-2])

    return position