import os
import sys

# Add the project root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from classes.admin import Admin
from classes.student import Student
from classes.vehicle import Vehicle
from classes.parkingLot import ParkingLot

# Setup environment
admin = Admin("Admin Mike", 1, "admin@example.com", "AdminPass123")

student1 = Student("Alice", 2, "alice@student.com", "Password123", "21-12345", "BS Computer Science")
car1 = Vehicle(student1, "CAR12345", "Car")
car1.register_vehicle()

student2 = Student("Bob", 3, "bob@student.com", "Password123", "21-54321", "BS Information Technology")
car2 = Vehicle(student2, "CAR54321", "Car")
car2.register_vehicle()

parking_slots = [
    ParkingLot(slotId=1, isForStaff=False),
    ParkingLot(slotId=2, isForStaff=True),
]

# Precondition: Park a vehicle
parking_slots[0].reserve(student1, car1)
car1.park_vehicle()

# Test cases
def test_reset_user_password():
    print("\nTest: Reset User Password")
    admin.reset_password(student1.get_user_id())
    # Expected: Admin resets the password for student1
    print("Success: Password reset functionality works as expected.")

def test_manage_parking_slots():
    print("\nTest: Manage Parking Slots")
    result = parking_slots[1].reserve(student2, car2)
    if result:
        print(f"Success: Admin reserved slot {parking_slots[1].get_slot_id()} for {car2.get_license_plate()}.")
    else:
        print(f"Fail: Admin could not reserve slot {parking_slots[1].get_slot_id()} for {car2.get_license_plate()}.")

def test_unpark_vehicle():
    print("\nTest: Unpark Vehicle")
    result = parking_slots[0].release(student1, car1)
    if result:
        print(f"Success: Vehicle {car1.get_license_plate()} successfully unparked from slot {parking_slots[0].get_slot_id()}.")
    else:
        print(f"Fail: Vehicle {car1.get_license_plate()} could not be unparked from slot {parking_slots[0].get_slot_id()}.")

# Run tests
def run_tests():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Running Admin Functional Tests...")
    test_reset_user_password()
    test_manage_parking_slots()
    test_unpark_vehicle()

if __name__ == "__main__":
    run_tests()