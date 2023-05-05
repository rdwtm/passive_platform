import os
import json
from utils import *

def save_position(robot, file = "positions.json"):
    # pobranie listy pozycji z pliku JSON
    if not os.path.exists(file):
        positions = []
    else:
        with open(file, 'r') as f:
            positions = json.load(f)

    
    # pobranie nazwy pozycji od użytkownika
    name = input('Podaj nazwę pozycji: ')

    # sprawdzenie, czy pozycja o podanej nazwie już istnieje
    for position in positions:
        if position['name'] == name:
            # jeśli pozycja istnieje, zapytaj użytkownika, czy chce ją nadpisać
            answer = input(f"Pozycja o nazwie '{name}' już istnieje. Czy chcesz ją nadpisać? (tak/nie): ")
            if answer.lower() != 'tak':
                # jeśli użytkownik nie chce nadpisać pozycji, przejdź do pobierania nowej nazwy pozycji
                break
            else:
                # jeśli użytkownik chce nadpisać pozycję, usuń istniejącą pozycję z listy
                positions.remove(position)
                break

    # pobranie aktualnej pozycji robota
    tcp_pose = check_position(robot)
    print(tcp_pose)
    # utworzenie słownika z pozycją robota
    position = {'name': name, 'tcp_pose': tcp_pose}
    print(position)
    # dodanie nowej pozycji do listy
    positions.append(position)
    print(positions)

    # zapisanie pozycji do pliku JSON
    with open(file, 'w') as f:
        json.dump(positions, f, indent=4)

    print(f"Pozycja '{name}' została zapisana do pliku {file}.")
    