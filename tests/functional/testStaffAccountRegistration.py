import os
import sys
import re

# Add the project root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from classes.admin import Admin
from classes.staff import Staff
from classes.student import Student
from classes.vehicle import Vehicle
from classes.parkingLot import ParkingLot

# Setup test environment
parking_slots = [
    ParkingLot(slotId=1, isForStaff=False),
    ParkingLot(slotId=2, isForStaff=True),
    ParkingLot(slotId=3, isForStaff=False),
    ParkingLot(slotId=4, isForStaff=True),
]

admin = Admin("Admin Sarah", 1, "admin@sps.com", "AdminPass123")

def setup_test_users():
    """Create test users and return them"""
    # Create staff members for testing
    staff1 = Staff("Dr. Johnson", 2, "johnson@staff.com", "StaffPass123", "21-54321", "College of Engineering")
    car1 = Vehicle(staff1, "STAFF123", "Car")
    car1.register_vehicle()

    staff2 = Staff("Prof. Williams", 3, "williams@staff.com", "StaffPass456", "21-98765", "College of Science")
    motorcycle1 = Vehicle(staff2, "STAFF456", "Motorcycle")
    motorcycle1.register_vehicle()

    # Create a student for negative testing
    student1 = Student("Alice", 4, "alice@student.com", "Password123", "21-12345", "BS Computer Science")
    student_car = Vehicle(student1, "STU12345", "Car")
    student_car.register_vehicle()
    
    return staff1, staff2, student1

# Test cases
def test_valid_staff_registration_and_vehicle_registration():
    print("\nTest Case 1: Valid Staff Registration and Vehicle Registration")
    try:
        # Valid staff registration
        staff = Staff("Dr. Smith", 10, "smith@university.edu", "ValidPass123", "AB-12342", "College of Engineering")
        print(f"SUCCESS: Staff created: {staff.name}, {staff.get_user_id()}, {staff.get_staff_code()}")

        # Valid vehicle registration
        vehicle = Vehicle(staff, "STAFF123", "Car")
        vehicle.register_vehicle()
        if vehicle in staff.get_vehicles():
            print(f"SUCCESS: Vehicle {vehicle.get_license_plate()} registered for {staff.name}.")
        else:
            print("FAIL: Vehicle registration failed - not in staff's vehicles")
    except Exception as e:
        print(f"FAIL: Valid registration failed: {str(e)}")


def test_edge_case_staff_registration_and_vehicle_registration():
    print("\nTest Case 2: Edge Case - Staff Registration and Vehicle Registration")
    try:
        # Edge case: Minimum valid staff code
        staff = Staff("Dr. Chen", 12, "chen@university.edu", "ValidPass123", "00-00000", "College of Arts")
        print(f"SUCCESS: Staff created with minimum valid staff code: {staff.name}, {staff.get_user_id()}, {staff.get_staff_code()}")

        # Edge case: Maximum length license plate
        max_plate = "A" * 8  # Assuming 8 is the max length
        vehicle = Vehicle(staff, max_plate, "Motorcycle")
        vehicle.register_vehicle()
        if vehicle in staff.get_vehicles():
            print(f"SUCCESS: Vehicle with max length plate {max_plate} registered for {staff.name}.")
        else:
            print("FAIL: Max length plate registration failed silently")
    except Exception as e:
        print(f"FAIL: Edge case registration failed: {str(e)}")


def test_invalid_account_registration():
    print("\nTest Case 3: Invalid Account Registration")
    try:
        # Invalid email format
        staff = Staff("Dr. Brown", 14, "brown@invalid", "ValidPass123", "22-12345", "College of Science")
        print("FAIL: invalid email format rejected")
    except ValueError as e:
        print(f"SUCCESS: invalid email rejected - {str(e)}")

    try:
        # Short password
        staff = Staff("Dr. Taylor", 15, "taylor@university.edu", "short", "22-54321", "College of Medicine")
        print("FAIL: short password rejected")
    except ValueError as e:
        print(f"SUCCESS: short password rejected - {str(e)}")

    try:
        # Invalid staff code format
        staff = Staff("Dr. Adams", 17, "adams@university.edu", "ValidPass123", "invalid", "College of Business")
        print("FAIL: invalid staff code format rejected")
    except ValueError as e:
        print(f"SUCCESS: invalid staff code rejected - {str(e)}")

# Run tests
def run_tests():
    os.system('cls' if os.name == 'nt' else 'clear')
    test_valid_staff_registration_and_vehicle_registration()
    test_edge_case_staff_registration_and_vehicle_registration()
    test_invalid_account_registration()
    print("\n=== All Tests Completed ===")

if __name__ == "__main__":
    run_tests()