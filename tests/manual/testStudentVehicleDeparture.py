import os
import sys

# Add the project root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from classes.student import Student
from classes.vehicle import Vehicle
from classes.parkingLot import ParkingLot

parking_slots = [
    ParkingLot(slotId=1, isForStaff=False),
    ParkingLot(slotId=2, isForStaff=False),
]

student1 = Student("Alice", 1, "alice@student.com", "Password123", "21-12345", "BS Computer Science")
car1 = Vehicle(student1, "CAR12345", "Car")
car1.register_vehicle()

student2 = Student("Bob", 2, "bob@student.com", "Password123", "21-54321", "BS Information Technology")
motorcycle1 = Vehicle(student2, "MC54321", "Motorcycle")
motorcycle1.register_vehicle()

student3 = Student("David", 3, "david@student.com", "Password123", "21-98765", "BS Computer Science")
motorcycle2 = Vehicle(student3, "MC12345", "Motorcycle")
motorcycle2.register_vehicle()

# preconditions: vehicles should already be parked in the parking slotss
parking_slots[0].reserve(student1, car1)
car1.park_vehicle()

parking_slots[1].reserve(student2, motorcycle1)
motorcycle1.park_vehicle()

parking_slots[1].reserve(student3, motorcycle2)  
motorcycle2.park_vehicle()

# test cases 009 - 012
test_cases = [
    (student1, car1, parking_slots[0], True),  # Student 1 departs their car that is already parked from the parking slot - pass
    (student1, car1, parking_slots[0], False),  # Student 1 tries to depart their car that is not parked - fail
    (student2, motorcycle1, parking_slots[1], True),  # Students 2 and 3 depart their motorcycle that is parked from the parking slot - pass
    (student3, motorcycle2, parking_slots[1], True),
    (student2, motorcycle1, parking_slots[1], False),  # Student 2 tries to depart their motorcycle that is not parked - fail
]

def test_vehicle_departure(test_cases):
    os.system('cls' if os.name == 'nt' else 'clear')
    for user, vehicle, slot, expected_result in test_cases:
        description = f"User {user.get_user_id()} tries to depart {vehicle.get_license_plate()} from slot {slot.get_slot_id()}"
        print(f"\n{description}")
        
        result = slot.release(user, vehicle)
        if result == expected_result:
            if result:
                vehicle.unpark_vehicle()
                print(f"Success: {vehicle.get_license_plate()} departed from slot {slot.get_slot_id()}.")
            else:
                print(f"Success: {vehicle.get_license_plate()} could not depart from slot {slot.get_slot_id()}.")
        else:
            print(f"Fail: Unexpected result for {vehicle.get_license_plate()} in slot {slot.get_slot_id()}.")

test_vehicle_departure(test_cases)