from models import database


def create_clients(clients, *, db):
    for client in clients:
        person = database.Client(document=client[0], first_name=client[1], last_name=client[2], patronymic=client[3],
                                 birthday=client[4])
        db.add(person)
        db.commit()


def create_pets(pets, *, db):
    for pet in pets:
        animal = database.Pet(client_id=pet[0], name=pet[1], birthday=pet[2])
        db.add(animal)
        db.commit()
