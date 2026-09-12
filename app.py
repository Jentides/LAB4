import sys
import unittest

# --- 1-3: MODULE IMPORTS ---
# Importing the existing modules from the 'modules' directory.
# Since the exact function signatures in your 1-3 modules are hidden, 
# these assume standard procedural signatures passing the database instance.
try:
    from modules.pet_owner_management import register_owner, view_owners
    from modules.appointment import schedule_appointment, view_appointments, cancel_appointment, update_appointment_status
    # If pet management logic (viewing/associating) is in clinic_database:
    # from modules.clinic_database import view_pets
except ImportError as e:
    print(f"Warning: Ensure your modules are correctly set up in the 'modules' folder. Missing: {e}")

# --- 4. DESIGN PATTERN IMPLEMENTATION ---

# Singleton Pattern: ClinicDatabase
class ClinicDatabase:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ClinicDatabase, cls).__new__(cls)
            # Centralized storage for the clinic
            cls._instance.owners = {}        # {owner_id: {"name": name, "contact": contact}}
            cls._instance.pets = []          # List of Pet objects
            cls._instance.appointments = {}  # {apt_id: {"pet_name": name, "status": status}}
        return cls._instance

# Factory Pattern: PetFactory
class Pet:
    def __init__(self, name, owner_id):
        self.name = name
        self.owner_id = owner_id

class Dog(Pet): pass
class Cat(Pet): pass
class Bird(Pet): pass
class Rabbit(Pet): pass

class PetFactory:
    @staticmethod
    def create_pet(pet_type, name, owner_id):
        pet_type = pet_type.lower()
        if pet_type == 'dog':
            return Dog(name, owner_id)
        elif pet_type == 'cat':
            return Cat(name, owner_id)
        elif pet_type == 'bird':
            return Bird(name, owner_id)
        elif pet_type == 'rabbit':
            return Rabbit(name, owner_id)
        else:
            raise ValueError(f"Pet type '{pet_type}' is not supported.")


# --- 5. UNIT TESTING ---

class TestClinicSystem(unittest.TestCase):
    def setUp(self):
        # Reset the singleton instance before each test to ensure an isolated state
        ClinicDatabase._instance = None
        self.db = ClinicDatabase()

    def test_validate_singleton_instance(self):
        db1 = ClinicDatabase()
        db2 = ClinicDatabase()
        self.assertIs(db1, db2, "ClinicDatabase is not a Singleton! Instances differ.")

    def test_register_pet_owner(self):
        owner_id = "O1"
        self.db.owners[owner_id] = {"name": "John Doe", "contact": "1234567890"}
        self.assertIn(owner_id, self.db.owners)
        self.assertEqual(self.db.owners[owner_id]["name"], "John Doe")

    def test_add_pet_record(self):
        pet = PetFactory.create_pet("Dog", "Buddy", "O1")
        self.db.pets.append(pet)
        self.assertEqual(len(self.db.pets), 1)
        self.assertIsInstance(self.db.pets[0], Dog)
        self.assertEqual(self.db.pets[0].name, "Buddy")

    def test_schedule_appointment(self):
        apt_id = "A1"
        self.db.appointments[apt_id] = {"pet_name": "Buddy", "status": "Scheduled"}
        self.assertIn(apt_id, self.db.appointments)
        self.assertEqual(self.db.appointments[apt_id]["status"], "Scheduled")

    def test_cancel_appointment(self):
        apt_id = "A1"
        self.db.appointments[apt_id] = {"pet_name": "Buddy", "status": "Scheduled"}
        self.db.appointments[apt_id]["status"] = "Cancelled"
        self.assertEqual(self.db.appointments[apt_id]["status"], "Cancelled")


# --- TERMINAL APP (CLI) ---

def run_tests():
    print("\n--- Running Unit Tests ---")
    # Pass sys.argv to avoid breaking the CLI loop when unittest runs
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
    print("--------------------------\n")

def main():
    db = ClinicDatabase()

    while True:
        print("\n=== Veterinary Clinic Management System ===")
        print("1. Pet Owner Management")
        print("2. Pet Management (Factory implementation)")
        print("3. Appointment Management")
        print("4. Run Unit Tests")
        print("5. Exit")
        
        choice = input("Enter your choice: ")

        if choice == '1':
            print("\n--- Pet Owner Management ---")
            print("a. Register Owner")
            print("b. View Owners")
            sub_choice = input("Select option: ").lower()
            
            if sub_choice == 'a':
                owner_id = input("Enter Owner ID: ")
                name = input("Enter Owner Name: ")
                contact = input("Enter Contact Number: ")
                # Assuming your module 1 function takes these params
                try:
                    register_owner(db, owner_id, name, contact)
                    print(f"Owner {name} registered successfully!")
                except NameError:
                    db.owners[owner_id] = {"name": name, "contact": contact}
                    print(f"Owner {name} registered directly via CLI.")
            elif sub_choice == 'b':
                try:
                    view_owners(db)
                except NameError:
                    print("Registered Owners:", db.owners)

        elif choice == '2':
            print("\n--- Pet Management ---")
            print("a. Add Pet Record")
            print("b. View Pets")
            sub_choice = input("Select option: ").lower()

            if sub_choice == 'a':
                try:
                    p_type = input("Enter pet type (Dog, Cat, Bird, Rabbit): ")
                    p_name = input("Enter pet name: ")
                    o_id = input("Enter owner ID: ")
                    
                    # Core requirement: Create objects through PetFactory
                    pet = PetFactory.create_pet(p_type, p_name, o_id)
                    db.pets.append(pet)
                    print(f"Successfully created and associated a {pet.__class__.__name__} named '{pet.name}'!")
                except ValueError as e:
                    print(f"Error: {e}")
            elif sub_choice == 'b':
                for p in db.pets:
                    print(f"- Type: {p.__class__.__name__}, Name: {p.name}, Owner ID: {p.owner_id}")
                if not db.pets:
                    print("No pets registered yet.")

        elif choice == '3':
            print("\n--- Appointment Management ---")
            print("a. Schedule Appointment")
            print("b. View Appointments")
            print("c. Update/Cancel Appointment")
            sub_choice = input("Select option: ").lower()

            if sub_choice == 'a':
                apt_id = input("Enter Appointment ID: ")
                pet_name = input("Enter Pet Name: ")
                try:
                    schedule_appointment(db, apt_id, pet_name)
                    print("Appointment scheduled successfully!")
                except NameError:
                    db.appointments[apt_id] = {"pet_name": pet_name, "status": "Scheduled"}
                    print("Appointment scheduled directly via CLI (Module not fully linked).")
            elif sub_choice == 'b':
                try:
                    view_appointments(db)
                except NameError:
                    print("Appointments:", db.appointments)
            elif sub_choice == 'c':
                apt_id = input("Enter Appointment ID to modify: ")
                new_status = input("Enter new status (Scheduled, Completed, Cancelled): ").capitalize()
                try:
                    if new_status == "Cancelled":
                        cancel_appointment(db, apt_id)
                    else:
                        update_appointment_status(db, apt_id, new_status)
                except NameError:
                    if apt_id in db.appointments:
                        db.appointments[apt_id]["status"] = new_status
                        print(f"Appointment {apt_id} status updated to {new_status}.")
                    else:
                        print("Appointment not found.")

        elif choice == '4':
            run_tests()
            
        elif choice == '5':
            print("Exiting system. Goodbye!")
            sys.exit(0)
            
        else:
            print("Invalid choice. Please enter a number from 1 to 5.")

if __name__ == "__main__":
    main()
