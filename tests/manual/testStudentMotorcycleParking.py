import os
import sys

# Add the project sroot directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from classes.student import Student
from classes.vehicle import Vehicle
from classes.parkingLot import ParkingLot

parking_slots = [
    ParkingLot(slotId = 1, isForStaff = False), 
    ParkingLot(slotId = 2, isForStaff = True),
    ParkingLot(slotId = 3, isForStaff = False),
]

# accounts
student1 = Student("Alice", 1, "alice@student.com", "Password123", "21-12345", "BS Computer Science")
motorcycle1 = Vehicle(student1, "MC12345", "Motorcycle")
motorcycle1.register_vehicle()

student2 = Student("Bob", 2, "bob@student.com", "Password123", "21-54321", "BS Information Technology")
motorcycle2 = Vehicle(student2, "MC54321", "Motorcycle")
motorcycle2.register_vehicle()

student3 = Student("David", 3, "david@student.com", "Password123", "21-98765", "BS Mathematics")
car1 = Vehicle(student3, "CAR9876", "Car")
car1.register_vehicle()

student4 = Student("Charlie", 4, "charlie@student.com", "Password123", "21-67890", "BS Architecture")
motorcycle3 = Vehicle(student4, "MC67890", "Motorcycle")
motorcycle3.register_vehicle()

# precondition for test case 4: a single motorcycle is parked in a parking slot 
parking_slots[2].reserve(student4, motorcycle3)
motorcycle3.park_vehicle()

# test cases
test_cases = {
    (student1, motorcycle1, parking_slots[1]): False,  # Student 1 parks their motorcycle in an empty staff parking slot - fail
    (student1, motorcycle1, parking_slots[0]): True,  # Student 1 parks their motorcycle in an empty parking slot - pass
    (student2, motorcycle2, parking_slots[0]): True,  # Student 2 parks their motorcycle in the same slot as Student 1 - pass
    (student3, car1, parking_slots[2]): False,        # student 3 tries to park their car in the slot occupied by Student 4's motorcycle - fail
}

def test_motorcycle_parking():
    os.system('cls' if os.name == 'nt' else 'clear')
    for (user, vehicle, slot), expected_result in test_cases.items():
        user_id = user.get_user_id()
        description = f"Student {user_id} tries to park {vehicle.get_license_plate()} in slot {slot.get_slot_id()}"
        print(f"\n{description}")
        result = slot.reserve(user, vehicle)
        if result == expected_result:
            if result:
                vehicle.park_vehicle()
                print(f"Success: {vehicle.get_license_plate()} parked in slot {slot.get_slot_id()}")
            else:
                print(f"Success: {vehicle.get_license_plate()} could not park in slot {slot.get_slot_id()}")
        else:
            print(f"Fail: Unexpected result for {vehicle.get_license_plate()} in slot {slot.get_slot_id()}")

test_motorcycle_parking()