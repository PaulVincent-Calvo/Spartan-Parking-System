import os
import re
from user import User
from admin import Admin
from staff import Staff
from student import Student
from vehicle import Vehicle
from parkingLot import ParkingLot

next_user_id = 2  

parking_slots = [
    ParkingLot(slotId=1, isForStaff=False),
    ParkingLot(slotId=2, isForStaff=False),
    ParkingLot(slotId=3, isForStaff=True), 
    ParkingLot(slotId=4, isForStaff=False),
    ParkingLot(slotId=5, isForStaff=True)   
]

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def is_valid_email(email):
    return re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email) is not None

def is_valid_password(password):
    return (
        len(password) >= 10 and
        any(c.isupper() for c in password) and
        any(c.isdigit() for c in password)
    )

def is_valid_sr_code(sr_code):
    return re.match(r'^\d{2}-\d{5}$', sr_code) is not None

def is_valid_staff_code(staff_code):
    return re.match(r'^\d{2}-\d{5}$', staff_code) is not None

def is_valid_license_plate(license_plate):
    return re.match(r'^[A-Z0-9]{6,8}$', license_plate) is not None

def register_vehicle(user):
    clear_screen()
    print("\n==============================")
    print("     Vehicle Registration")
    print("==============================")
    while True:
        license_plate = input("Enter vehicle license plate (6-8 alphanumeric characters): ").strip()
        if license_plate and is_valid_license_plate(license_plate):
            break
        print("Invalid license plate format. Please enter 6-8 alphanumeric characters (e.g., ABC1234).")
    
    print("Select your vehicle type:")
    print("1. Car (any 4 Wheeler vehicle)")
    print("2. Motorcycle")
    while True:
        vehicle_type_choice = input("Enter choice (1 or 2): ").strip()
        if vehicle_type_choice == "1":
            vehicle_type = "Car"
            break
        elif vehicle_type_choice == "2":
            vehicle_type = "Motorcycle"
            break
        else:
            print("Invalid choice. Please select 1 or 2.")
    
    vehicle = Vehicle(user, license_plate, vehicle_type)
    vehicle.register_vehicle()
    return vehicle

def park_vehicle(user):
    clear_screen()
    print("\n==============================")
    print("       Parking a Vehicle")
    print("==============================")

    print("Available Parking Slots:")
    for slot in parking_slots:
        if not slot.is_occupied():
            if slot.is_for_staff() and not isinstance(user, Staff):
                continue  # Skip staff-only slots for non-staff users
            print(f"Slot {slot.get_slot_id()} {'(Staff Only)' if slot.is_for_staff() else ''} - Space Available: {slot._ParkingLot__spaceAvailable}")

    if not hasattr(user, 'vehicles') or not user.vehicles:
        print("You have no registered vehicles. Please register a vehicle first.")
        return

    print("\nYour Registered Vehicles:")
    for idx, vehicle in enumerate(user.vehicles, start=1):
        print(f"{idx}. {vehicle.get_license_plate()} ({vehicle.get_vehicle_type()})")

    while True:
        try:
            vehicle_choice = input("Select a vehicle to park (enter the number): ").strip()
            if not vehicle_choice.isdigit() or int(vehicle_choice) < 1 or int(vehicle_choice) > len(user.vehicles):
                print("Invalid choice. Please select a valid vehicle number.")
                continue
            selected_vehicle = user.vehicles[int(vehicle_choice) - 1]
            break
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    while True:
        try:
            slot_id = input("Enter the slot ID to park your vehicle: ").strip()
            if not slot_id.isdigit():
                print("Invalid input. Please enter a numeric slot ID.")
                continue
            slot_id = int(slot_id)
            selected_slot = next((slot for slot in parking_slots if slot.get_slot_id() == slot_id), None)
            if selected_slot:
                if selected_slot.is_for_staff() and not isinstance(user, Staff):
                    print("This slot is for staff only. Please choose another slot.")
                    continue

                if selected_slot.reserve(user, selected_vehicle):
                    print(f"Vehicle {selected_vehicle.get_license_plate()} parked in slot {slot_id}.")
                    break
                else:
                    print(f"Failed to park vehicle {selected_vehicle.get_license_plate()} in slot {slot_id}.")
            else:
                print("Invalid slot ID. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a valid slot ID.")

def depart_vehicle(user):
    clear_screen()
    print("\n==============================")
    print("       Depart a Vehicle")
    print("==============================")

    if not hasattr(user, 'vehicles') or not user.vehicles:
        print("You have no registered vehicles. Please register a vehicle first.")
        return

    print("\nYour Registered Vehicles:")
    for idx, vehicle in enumerate(user.vehicles, start=1):
        print(f"{idx}. {vehicle.get_license_plate()} ({vehicle.get_vehicle_type()})")

    while True:
        try:
            vehicle_choice = input("Select a vehicle to depart (enter the number): ").strip()
            if not vehicle_choice.isdigit() or int(vehicle_choice) < 1 or int(vehicle_choice) > len(user.vehicles):
                print("Invalid choice. Please select a valid vehicle number.")
                continue
            selected_vehicle = user.vehicles[int(vehicle_choice) - 1]
            break
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    for slot in parking_slots:
        if slot.release(user, selected_vehicle):
            print(f"Vehicle {selected_vehicle.get_license_plate()} has departed successfully.")
            return

    print(f"Error: Vehicle {selected_vehicle.get_license_plate()} is not parked in any slot.")

def register_user():
    global next_user_id

    clear_screen()
    print("\n==============================")
    print("      User Registration")
    print("==============================")
    print("Select User Type:")
    print("1. Student")
    print("2. Staff")
    while True:
        choice = input("Enter choice (1 or 2): ").strip()
        if choice in ["1", "2"]:
            break
        print("Invalid choice. Please select 1 or 2.")
    
    name = input("Enter your name: ").strip()
    while not name:
        print("Name cannot be empty. Please enter your name.")
        name = input("Enter your name: ").strip()
    
    while True:
        email = input("Enter email: ").strip()
        if email and is_valid_email(email):
            break
        print("Invalid email format. Please enter a valid email address.")
    
    while True:
        password = input("Enter password: ").strip()
        if password and is_valid_password(password):
            break
        print("Password must be at least 10 characters long, contain at least one uppercase letter, and include a number.")
    
    user_id = next_user_id 
    next_user_id += 1  
    
    if choice == "1":
        while True:
            sr_code = input("Enter student SR Code: ").strip()
            if sr_code and is_valid_sr_code(sr_code):
                break
            print("Invalid SR Code format. Please use the SR Code found in your ID (e.g., 21-12355).")
        
        print("Select your course:")
        print("1. BS Computer Science")
        print("2. BS Information Technology")
        while True:
            course_choice = input("Enter choice (1 or 2): ").strip()
            if course_choice == "1":
                course = "BS Computer Science"
                break
            elif course_choice == "2":
                course = "BS Information Technology"
                break
            else:
                print("Invalid choice. Please select 1 or 2.")
        
        user = Student(name, user_id, email, password, sr_code, course)
    elif choice == "2":
        while True:
            staff_code = input("Enter staff code: ").strip()
            if staff_code and is_valid_staff_code(staff_code):
                break
            print("Invalid staff code format. Please use the format '21-12355'.")
        
        print("Select your department:")
        print("1. College of Engineering, Architecture, and Fine Arts")
        print("2. College of Informatics and Computing Sciences")
        print("3. College of Engineering Technology")
        print("4. Essential Staff")
        while True:
            department_choice = input("Enter choice (1, 2, 3, or 4): ").strip()
            if department_choice == "1":
                department = "College of Engineering, Architecture, and Fine Arts"
                break
            elif department_choice == "2":
                department = "College of Informatics and Computing Sciences"
                break
            elif department_choice == "3":
                department = "College of Engineering Technology"
                break
            elif department_choice == "4":
                department = "Essential Staff"
                break
            else:
                print("Invalid choice. Please select 1, 2, 3, or 4.")
        
        user = Staff(name, user_id, email, password, staff_code, department)
    else:
        print("Invalid choice. Please try again.")
        return None

    register_vehicle(user)

    return user

def main():
    global next_user_id
    admin1 = Admin("Admin Mike", 1, "admin@example.com", "AdminPass123")
    users = {1: admin1}  # Dictionary to store users by their user ID

    # Adding three student users with their vehicles
    student1 = Student("Alice", next_user_id, "alice@example.com", "Password123", "21-12345", "BS Computer Science")
    next_user_id += 1
    vehicle1 = Vehicle(student1, "MC12345", "Motorcycle")
    vehicle1.register_vehicle()
    users[student1._User__userID] = student1

    student2 = Student("Bob", next_user_id, "bob@example.com", "Password123", "21-54321", "BS Information Technology")
    next_user_id += 1
    vehicle2 = Vehicle(student2, "MC54321", "Motorcycle")
    vehicle2.register_vehicle()
    users[student2._User__userID] = student2

    student3 = Student("Charlie", next_user_id, "charlie@example.com", "Password123", "21-67890", "BS Computer Science")
    next_user_id += 1
    vehicle3 = Vehicle(student3, "CAR6789", "Car")
    vehicle3.register_vehicle()
    users[student3._User__userID] = student3

    while True:
        clear_screen()
        print("\n==============================")
        print("    Spartan Parking System")
        print("==============================")
        print("1. Login")
        print("2. Register")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            clear_screen()
            print("\n==============================")
            print("             Login")
            print("==============================")
            email = input("Enter email: ")
            password = input("Enter password: ")
            
            found_user = None
            for user in users.values():
                if user._User__email == email and user._User__password == password:
                    found_user = user
                    break
            
            if found_user:
                while True:
                    clear_screen()
                    print("\n==============================")
                    print("   Spartan Parking System")
                    print("==============================")
                    print(f"Welcome, {found_user.name}!")
                    print("\nWhat would you like to do?")
                    print("1. Park a vehicle")
                    print("2. Register another vehicle")
                    print("3. Depart a vehicle")
                    print("4. Exit the system")
                    user_choice = input("Enter your choice: ")

                    if user_choice == "1":
                        park_vehicle(found_user)
                    elif user_choice == "2":
                        register_vehicle(found_user)
                    elif user_choice == "3":
                        depart_vehicle(found_user)
                    elif user_choice == "4":
                        print("Logging out... Goodbye!")
                        break
                    else:
                        print("Invalid choice. Please try again.")
            else:
                print("Invalid email or password.")        
    
        elif choice == "2":
            user = register_user()
            if user:
                users[user._User__userID] = user
                print(f"User {user.name} registered successfully with ID {user._User__userID}!")

        elif choice == "3":
            print("Exiting... Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
