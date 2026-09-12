class PetOwner: 
    def __init__(self, owner_id, name, contact_number):
        self.owner_id = owner_id
        self.name = name
        self.contact_number = contact_number
        self.pets = []

    def add_pet(self, pet):
        self.pets.append(pet)

    def __str__(self):
        return f"Owner[{self.owner_id}]: {self.name} (Contact: {self.contact_number})"

class Pet: 
    def __init__(self, pet_id, name, owner):
        self.pet_id = pet_id
        self.name = name
        self.owner = owner
        self.species = "Generic"

    def __str__(self):
        return f"{self.species}[{self.pet_id}]: {self.name} - Owned by {self.owner.name}"

## classes for each pets

class Dog(Pet):
    def __init__(self, pet_id, name, owner):
        super().__init__(pet_id, name, owner)
        self.species = "Dog"

class Cat(Pet):
    def __init__(self, pet_id, name, owner):
        super().__init__(pet_id, name, owner)
        self.species = "Cat"

class Bird(Pet):
    def __init__(self, pet_id, name, owner):
        super().__init__(pet_id, name, owner)
        self.species = "Bird"

class Rabbit(Pet):
    def __init__(self, pet_id, name, owner):
        super().__init__(pet_id, name, owner)
        self.species = "Rabbit"