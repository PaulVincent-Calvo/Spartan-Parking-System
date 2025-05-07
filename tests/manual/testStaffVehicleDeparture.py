import os
import sys

# Add the project root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from classes.staff import Staff
from classes.vehicle import Vehicle
from classes.parkingLot import ParkingLot

parking_slots = [
    ParkingLot(slotId=1, isForStaff=False),
    ParkingLot(slotId=2, isForStaff=True),
]

staff1 = Staff("Alice", 1, "alice@staff.com", "Password123", "CA-12345", "College of Engineering, Architecturem, and Fine Arts")
car1 = Vehicle(staff1, "CAR12345", "Car")
car1.register_vehicle()

staff2 = Staff("Bob", 2, "bob@staff.com", "Password123", "CI-54321", "College of Informatics and Computing Sciences")
motorcycle1 = Vehicle(staff2, "MC54321", "Motorcycle")
motorcycle1.register_vehicle()

staff3 = Staff("David", 3, "david@staff.com", "Password123", "21-98765", "College of Engineering Technology")
motorcycle2 = Vehicle(staff3, "MC12345", "Motorcycle")
motorcycle2.register_vehicle()

# preconditions: vehicles should already be parked in the parking slots
parking_slots[0].reserve(staff1, car1)
car1.park_vehicle()

parking_slots[1].reserve(staff2, motorcycle1)
motorcycle1.park_vehicle()

parking_slots[1].reserve(staff3, motorcycle2)
motorcycle2.park_vehicle()

# test cases 013 - 016
test_cases = [
    (staff1, car1, parking_slots[0], True),  # staff 1 departs their car that is already parked - pass
    (staff1, car1, parking_slots[0], False),  # staff 1 tries to depart their car that is not parked - fail
    (staff2, motorcycle1, parking_slots[1], True),  # staff 2 departs their motorcycle - pass
    (staff3, motorcycle2, parking_slots[1], True),  # staff 3 departs their motorcycle - pass
    (staff2, motorcycle1, parking_slots[1], False),  # staff 2 tries to depart their motorcycle that is not parked - fail
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