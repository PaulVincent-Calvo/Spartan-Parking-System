import os
import sys

# Add the project root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from classes.student import Student
from classes.vehicle import Vehicle
from classes.parkingLot import ParkingLot

parking_slots = [
    ParkingLot(slotId = 1, isForStaff = False), 
    ParkingLot(slotId = 2, isForStaff = False), 
    ParkingLot(slotId = 3, isForStaff = True)
]

# accounts
student1 = Student("Alice", 1, "alice@student.com", "Password123", "21-12345", "BS Computer Science")
car1 = Vehicle(student1, "CAR12345", "Car")
car1.register_vehicle()

student2 = Student("Bob", 2, "bob@student.com", "Password123", "21-54321", "BS Information Technology")
car2 = Vehicle(student2, "CAR54321", "Car")
car2.register_vehicle()

student3 = Student("Charlie", 3, "charlie@student.com", "Password123", "21-67890", "BS Architecture")
car3 = Vehicle(student3, "CAR6789", "Car")
car3.register_vehicle()

# precondition for test case 3: a car is already parked and will be parked again 
parking_slots[1].reserve(student3, car3)
car3.park_vehicle()

# test cases
test_cases = {
    (student1, car1, parking_slots[2]): False, # student 1 parks their car in a staff parking slot - fail
    (student1, car1, parking_slots[0]): True, # student 1 parks their car in an empty parking slot - pass
    (student2, car2, parking_slots[0]): False,  # student 2 parks their car in the same slot as Student 1 - fail
    (student3, car3, parking_slots[1]): False,  # student 3 tries to park their car that is already parked - fail
}

# Function to test car parking
def test_car_parking():
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

test_car_parking()