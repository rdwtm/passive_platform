def save_position():
    # pobranie listy pozycji z pliku JSON
    if not os.path.exists('positions.json'):
        positions = []
    else:
        with open('positions.json', 'r') as file:
            positions = json.load(file)

    while True:
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
        else:
            # jeśli pozycja nie istnieje lub użytkownik zdecydował się nadpisać istniejącą pozycję, przejdź dalej
            choice = input("Do you want to add another position? (y/n)")
            if choice.lower() == "n":
                break

        # pobranie aktualnej pozycji robota
        tcp_pose = get_tcp_pose()

        # utworzenie słownika z pozycją robota
        position = {'name': name, 'tcp_pose': tcp_pose}

        # dodanie nowej pozycji do listy
        positions.append(position)

    # zapisanie pozycji do pliku JSON
    with open('positions.json', 'w') as file:
        json.dump(positions, file, indent=4)

    print(f"Pozycja '{name}' została zapisana do pliku 'positions.json'.")
