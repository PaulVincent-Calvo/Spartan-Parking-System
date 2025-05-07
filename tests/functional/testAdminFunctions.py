import os
import sys

# Add the project root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from classes.admin import Admin
from classes.student import Student
from classes.vehicle import Vehicle
from classes.parkingLot import ParkingLot

parking_slots = [
    ParkingLot(slotId=1, isForStaff=False),
    ParkingLot(slotId=2, isForStaff=True),
    ParkingLot(slotId=3, isForStaff=False),  
    ParkingLot(slotId=4, isForStaff=False),  
]

admin = Admin("Admin Mike", 1, "admin@sps.com", "AdminPass123")

student1 = Student("Alice", 2, "alice@student.com", "Password123", "21-12345", "BS Computer Science")
car1 = Vehicle(student1, "CAR12345", "Car")
car1.register_vehicle()

student2 = Student("Bob", 3, "bob@student.com", "Password123", "21-54321", "BS Information Technology")
motorcycle1 = Vehicle(student2, "MC54321", "Motorcycle")
motorcycle1.register_vehicle()

student3 = Student("Charlie", 4, "charlie@student.com", "Password123", "21-67890", "BS Mathematics")
motorcycle2 = Vehicle(student3, "MC67890", "Motorcycle")
motorcycle2.register_vehicle()

student4 = Student("David", 5, "david@student.com", "Password123", "21-98765", "BS Physics")
car2 = Vehicle(student4, "CAR98765", "Car")
car2.register_vehicle()

student5 = Student("Eve", 6, "eve@student.com", "Password123", "21-54322", "BS Chemistry")
motorcycle3 = Vehicle(student5, "MC54322", "Motorcycle")
motorcycle3.register_vehicle()

# test cases
def test_reset_password():
    print("\nFunctional Test: Reset Password")
    print(f"Before reset: {student1._User__password}")
    admin.reset_password(student1, "NewPassword123")
    print(f"After reset: {student1._User__password}")
    if student1._User__password == "NewPassword123":
        print("Success: Password reset successfully.")
    else:
        print("Fail: Password reset failed.")

    print("\nNegative Case: Invalid Password Format")
    admin.reset_password(student1, "short")
    if student1._User__password == "short":
        print("Fail: Password should not have been reset.")
    else:
        print("Success: Invalid password was rejected.")

def test_admin_dashboard():
    print("\nFunctional Test: Admin Dashboard")
    parking_slots[0].reserve(student1, car1)
    parking_slots[0].park(student1, car1)

    parking_slots[1].reserve(student2, motorcycle1)
    parking_slots[1].park(student2, motorcycle1)

    parking_slots[2].reserve(student4, car2)  
    parking_slots[3].reserve(student5, motorcycle3) 

    print("\nParking Slot Status:")
    for slot in parking_slots:
        if slot.is_occupied():
            print(f"Slot {slot.get_slot_id()}:")
            reservations = slot.get_reservations()
            if reservations:
                print("  Reservations:")
                for user, vehicles in reservations.items():
                    for vehicle in vehicles:
                        print(f"    - {user.name} ({vehicle.get_license_plate()}, {vehicle.get_vehicle_type()})")
            parked_vehicles = slot.get_parked_vehicles()
            if parked_vehicles:
                print("  Parked Vehicles:")
                for user, vehicles in parked_vehicles.items():
                    for vehicle in vehicles:
                        print(f"    - {user.name} ({vehicle.get_license_plate()}, {vehicle.get_vehicle_type()})")
        else:
            print(f"Slot {slot.get_slot_id()}: Unoccupied")

def test_manual_parking():
    print("\nFunctional Test: Manual Parking")
    print("\nManually Parking a Vehicle:")
    
    parking_slots[0].release(student1, car1)

    if parking_slots[0].reserve(student1, car1):
        if parking_slots[0].park(student1, car1):
            print(f"Success: Vehicle {car1.get_license_plate()} parked in slot {parking_slots[0].get_slot_id()}.")
        else:
            print(f"Fail: Could not park vehicle {car1.get_license_plate()} in slot {parking_slots[0].get_slot_id()}.")
    else:
        print(f"Fail: Could not reserve slot {parking_slots[0].get_slot_id()} for vehicle {car1.get_license_plate()}.")

    print("\nNegative Case: Park in Staff-Only Slot")
    if parking_slots[1].reserve(student1, car1):
        print("Fail: Non-staff user should not be able to reserve a staff-only slot.")
    else:
        print("Success: Reservation rejected for non-staff user in staff-only slot.")

def test_manual_unparking():
    print("\nFunctional Test: Manual Unparking")
    print("\nManually Unparking a Vehicle:")
    if parking_slots[0].release(student1, car1):
        car1.unpark_vehicle()
        print(f"Success: Vehicle {car1.get_license_plate()} departed from slot {parking_slots[0].get_slot_id()}.")
    else:
        print(f"Fail: Could not unpark vehicle {car1.get_license_plate()} from slot {parking_slots[0].get_slot_id()}.")

    print("\nNegative Case: Unpark a Vehicle Not in Slot")
    if parking_slots[1].release(student1, car1):
        print("Fail: Vehicle should not have been unparked from a slot it is not parked in.")
    else:
        print("Success: Unparking rejected for vehicle not in the slot.")

# Run tests
def run_tests():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Running Admin Functional Tests...")
    test_admin_dashboard()    
    test_reset_password()
    test_manual_parking()
    test_manual_unparking()

if __name__ == "__main__":
    run_tests()