import os
import re
from classes.user import User
from classes.admin import Admin
from classes.staff import Staff
from classes.student import Student
from classes.vehicle import Vehicle
from classes.parkingLot import ParkingLot

next_user_id = 2  
users = {}  # Initialize users dictionary

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
    print(user.name + ", please register your vehicle.")
    
    while True:
        license_plate = input("Vehicle License Plate (6-8 alphanumeric characters, no spaces): ").strip()
        if license_plate and is_valid_license_plate(license_plate):
            break
        print("Invalid license plate format. Please enter 6-8 alphanumeric characters (e.g., ABC1234).")
    
    print("Select your vehicle type:")
    print("1. Car")
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
                continue
            print(f"Slot {slot.get_slot_id()} {'(Staff Only)' if slot.is_for_staff() else ''} - Space Available: {slot._ParkingLot__spaceAvailable}")

    user_vehicles = [vehicle for vehicle in user.get_vehicles() if not vehicle.is_parked()]
    if not user_vehicles:
        print("You have no unparked vehicles available to park. Please register or unpark a vehicle first.")
        return

    print("\nYour Unparked Registered Vehicles:")
    for idx, vehicle in enumerate(user_vehicles, start=1):
        print(f"{idx}. {vehicle.get_license_plate()} ({vehicle.get_vehicle_type()})")

    while True:
        try:
            vehicle_choice = input("\nSelect a vehicle to park (enter the number): ").strip()
            if not vehicle_choice.isdigit() or int(vehicle_choice) < 1 or int(vehicle_choice) > len(user_vehicles):
                print("Invalid choice. Please select a valid vehicle number.")
                continue
            selected_vehicle = user_vehicles[int(vehicle_choice) - 1]
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
                    selected_vehicle.park_vehicle()  # Mark the vehicle as parked
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

    # Filter vehicles that are registered and parked
    user_vehicles = [vehicle for vehicle in user.get_vehicles() if vehicle.is_parked()]
    if not user_vehicles:
        print("You have no parked vehicles available to depart. Please park a vehicle first.")
        return

    print("\nYour Parked Registered Vehicles:")
    for idx, vehicle in enumerate(user_vehicles, start=1):
        print(f"{idx}. {vehicle.get_license_plate()} ({vehicle.get_vehicle_type()})")

    while True:
        try:
            vehicle_choice = input("\nSelect a vehicle to depart (enter the number): ").strip()
            if not vehicle_choice.isdigit() or int(vehicle_choice) < 1 or int(vehicle_choice) > len(user_vehicles):
                print("Invalid choice. Please select a valid vehicle number.")
                continue
            selected_vehicle = user_vehicles[int(vehicle_choice) - 1]
            break
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    for slot in parking_slots:
        if slot.release(user, selected_vehicle):
            selected_vehicle.unpark_vehicle()  # Mark the vehicle as unparked
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
            clear_screen()
            print("\n==============================")
            print("      User Registration")
            print("==============================")
            break

        clear_screen()
        print("\n==============================")
        print("      User Registration")
        print("==============================")
        print("Select User Type:")
        print("1. Student")
        print("2. Staff")
        print("Invalid choice. Please select 1 or 2.")
    
    name = input("Name: ").strip()
    while not name:
        print("Name cannot be empty. Please enter your name.")
        name = input("Enter your name: ").strip()
    
    while True:
        email = input("Email: ").strip()
        if email and is_valid_email(email):
            break
        print("Invalid email format. Please enter a valid email address.")
    
    while True:
        password = input("Password (10 characters long with at least one uppercase letter and one number): ").strip()
        if password and is_valid_password(password):
            break
        print("Password must be at least 10 characters long, contain at least one uppercase letter, and include a number.")
    
    user_id = next_user_id 
    next_user_id += 1  
    
    if choice == "1":
        while True:
            sr_code = input("SR Code (xx-xxxxx): ").strip()
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
            staff_code = input("Staff code: ").strip()
            if staff_code and is_valid_staff_code(staff_code):
                break
            print("Invalid staff code format. Please use the format '21-12355'.")
        
        print("Select your department:")
        print("1. College of Engineering, Architecture, and Fine Arts")
        print("2. College of Informatics and Computing Sciences")
        print("3. College of Engineering Technology")
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
            else:
                print("Invalid choice. Please select 1, 2, or 3.")
        
        user = Staff(name, user_id, email, password, staff_code, department)
    else:
        print("Invalid choice. Please try again.")
        return None

    register_vehicle(user)

    return user

def admin_dashboard(admin):
    while True:
        clear_screen()
        print("\n==============================")
        print("        Admin Dashboard")
        print("==============================")
        print(f"Welcome, {admin.name}!")
        
        # Display the status of every parking slot
        print("\nParking Slot Status:")
        for slot in parking_slots:
            if slot.is_occupied():
                print(f"Slot {slot.get_slot_id()}:")
                
                # Display reserved vehicles
                reservations = slot.get_reservations()
                if reservations:
                    print("  Reservations:")
                    for user, vehicles in reservations.items():
                        for vehicle in vehicles:
                            print(f"    - {user.name} ({vehicle.get_license_plate()}, {vehicle.get_vehicle_type()})")
                
                # Display parked vehicles
                parked_vehicles = slot.get_parked_vehicles()
                if parked_vehicles:
                    print("  Parked Vehicles:")
                    for user, vehicles in parked_vehicles.items():
                        for vehicle in vehicles:
                            print(f"    - {user.name} ({vehicle.get_license_plate()}, {vehicle.get_vehicle_type()})")
            else:
                print(f"Slot {slot.get_slot_id()}: Unoccupied")
        
        # Admin options
        print("\nWhat would you like to do?")
        print("1. Manage Parking Slots")
        print("2. Reset User Password")
        print("3. Exit to Main Menu")
        choice = input("Enter your choice: ").strip()
        
        if choice == "1":
            manage_parking_slots(admin)
        elif choice == "2":
            reset_user_password(admin)
        elif choice == "3":
            print("Exiting Admin Dashboard... Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

def manage_parking_slots(admin):
    while True:
        clear_screen()
        print("\n==============================")
        print("     Manage Parking Slots")
        print("==============================")
        
        # Display parking slots
        print("Parking Slot Status:")
        for slot in parking_slots:
            if slot.is_occupied():
                print(f"Slot {slot.get_slot_id()}:")
                
                # Display reserved vehicles
                reservations = slot.get_reservations()
                if reservations:
                    print("  Reservations:")
                    for user, vehicles in reservations.items():
                        for vehicle in vehicles:
                            print(f"    - {user.name} ({vehicle.get_license_plate()}, {vehicle.get_vehicle_type()})")
                
                # Display parked vehicles
                parked_vehicles = slot.get_parked_vehicles()
                if parked_vehicles:
                    print("  Parked Vehicles:")
                    for user, vehicles in parked_vehicles.items():
                        for vehicle in vehicles:
                            print(f"    - {user.name} ({vehicle.get_license_plate()}, {vehicle.get_vehicle_type()})")
            else:
                print(f"Slot {slot.get_slot_id()}: Unoccupied")
        
        print("\nWhat would you like to do?")
        print("1. Manually Park a Vehicle")
        print("2. Unpark a Vehicle")
        print("3. Return to Admin Dashboard")
        choice = input("Enter your choice: ").strip()
        
        if choice == "1":
            manually_park_vehicle(admin)
        elif choice == "2":
            unpark_vehicle(admin)
        elif choice == "3":
            break
        else:
            print("Invalid choice. Please try again.")

def manually_park_vehicle(admin):
    clear_screen()
    print("\n==============================")
    print("     Manually Park a Vehicle")
    print("==============================")
    
    # Display all slots
    print("Parking Slot Status:")
    for slot in parking_slots:
        if slot.is_occupied():
            print(f"Slot {slot.get_slot_id()}: Occupied")
        else:
            print(f"Slot {slot.get_slot_id()}: Unoccupied")
    
    while True:
        try:
            slot_id = int(input("Enter the slot ID to park the vehicle in: ").strip())
            selected_slot = next((slot for slot in parking_slots if slot.get_slot_id() == slot_id), None)
            if selected_slot:
                break
            else:
                print("Invalid slot ID. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a numeric slot ID.")
    
    print("\nRegistered Users:")
    for user_id, user in users.items():
        print(f"User ID: {user_id}, Name: {user.name}")
    
    while True:
        try:
            user_id = int(input("Enter the User ID to park the vehicle for: ").strip())
            selected_user = users.get(user_id)
            if selected_user:
                break
            else:
                print("Invalid User ID. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a numeric User ID.")
    
    user_vehicles = [vehicle for vehicle in selected_user.get_vehicles() if not vehicle.is_parked()]
    if not user_vehicles:
        print(f"User {selected_user.name} has no unparked vehicles.")
        input("Press Enter to return to the previous menu...")
        return
    
    print("\nUser's Unparked Vehicles:")
    for idx, vehicle in enumerate(user_vehicles, start=1):
        print(f"{idx}. {vehicle.get_license_plate()} ({vehicle.get_vehicle_type()})")
    
    while True:
        try:
            vehicle_choice = int(input("Select a vehicle to park (enter the number): ").strip())
            if 1 <= vehicle_choice <= len(user_vehicles):
                selected_vehicle = user_vehicles[vehicle_choice - 1]
                break
            else:
                print("Invalid choice. Please select a valid vehicle number.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")
    
    # Reserve the slot and park the vehicle
    if selected_slot.reserve(selected_user, selected_vehicle):
        if selected_slot.park(selected_user, selected_vehicle):  # Call the park method
            print(f"Success: Vehicle {selected_vehicle.get_license_plate()} parked in slot {selected_slot.get_slot_id()}.")
        else:
            print(f"Failed: Could not park vehicle {selected_vehicle.get_license_plate()} in slot {selected_slot.get_slot_id()}.")
    else:
        print(f"Failed: Could not reserve slot {selected_slot.get_slot_id()} for vehicle {selected_vehicle.get_license_plate()}.")
    
    input("Press Enter to return to the previous menu...")

def unpark_vehicle(admin):
    clear_screen()
    print("\n==============================")
    print("        Unpark a Vehicle")
    print("==============================")
    
    # Display occupied slots
    occupied_slots = [slot for slot in parking_slots if slot.is_occupied()]
    if not occupied_slots:
        print("No vehicles are currently parked.")
        input("Press Enter to return to the previous menu...")
        return
    
    print("Occupied Slots:")
    for slot in occupied_slots:
        vehicle = slot.get_reserved_vehicle()
        print(f"Slot {slot.get_slot_id()}: {vehicle.get_license_plate()} ({vehicle.get_vehicle_type()})")
    
    # Select a slot to unpark
    while True:
        try:
            slot_id = int(input("Enter the slot ID to unpark the vehicle from: ").strip())
            selected_slot = next((slot for slot in occupied_slots if slot.get_slot_id() == slot_id), None)
            if selected_slot:
                break
            else:
                print("Invalid slot ID. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a numeric slot ID.")
    
    if selected_slot.release(selected_slot.get_reserved_user(), selected_slot.get_reserved_vehicle()):
        selected_slot.get_reserved_vehicle().unpark_vehicle()
        print(f"Vehicle successfully unparked from slot {selected_slot.get_slot_id()}.")
    else:
        print(f"Failed to unpark vehicle from slot {selected_slot.get_slot_id()}.")
    
    input("Press Enter to return to the previous menu...")

def reset_user_password(admin):
    clear_screen()
    print("\n==============================")
    print("      Reset User Password")
    print("==============================")
    
    print("Registered Users:")
    for user_id, user in users.items():
        print(f"User ID: {user_id}, Name: {user.name}")
    
    while True:
        try:
            user_id = int(input("Enter the User ID to reset the password for: ").strip())
            selected_user = users.get(user_id)
            if selected_user:
                break
            else:
                print("Invalid User ID. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a numeric User ID.")
    
    while True:
        new_password = input("Enter the new password (at least 10 characters, 1 uppercase letter, and 1 number): ").strip()
        if is_valid_password(new_password):
            admin.reset_password(selected_user, new_password) 
            break
        else:
            print("Invalid password. Please ensure it meets the criteria (at least 10 characters, 1 uppercase letter, and 1 number).")
    
    input("Press Enter to return to the previous menu...")

def main_system(user):
    while True:
        clear_screen()
        print("\n==============================")
        print("   Spartan Parking System")
        print("==============================")
        print(f"Welcome, {user.name}!")

        user_vehicles = user.get_vehicles()
        if user_vehicles:
            print("Your Registered Vehicles:")
            for idx, vehicle in enumerate(user_vehicles, start=1):
                print(f"{idx}. {vehicle.get_license_plate()} ({vehicle.get_vehicle_type()})")

        print("\nWhat would you like to do?")
        print("1. Park a vehicle")
        print("2. Depart your vehicle")
        print("3. Register another vehicle")
        print("4. Exit the system")
        user_choice = input("Enter your choice: ")

        if user_choice == "1":
            park_vehicle(user)
        elif user_choice == "2":
            depart_vehicle(user)
        elif user_choice == "3":
            register_vehicle(user)
        elif user_choice == "4":
            print("Logging out... Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

def main():
    global next_user_id, users  # Declare users as global
    admin1 = Admin("Admin Mike", 1, "admin@example.com", "AdminPass123")
    users = {1: admin1}  # Dictionary to store users by their user ID

    student1 = Student("Alice", next_user_id, "alice@student.com", "Password123", "21-12345", "BS Computer Science")
    next_user_id += 1
    vehicle1 = Vehicle(student1, "MC12345", "Motorcycle")
    vehicle1.register_vehicle()
    users[student1._User__userID] = student1

    student2 = Student("Bob", next_user_id, "bob@student.com", "Password123", "21-54321", "BS Information Technology")
    next_user_id += 1
    vehicle2 = Vehicle(student2, "MC54321", "Motorcycle")
    vehicle2.register_vehicle()
    users[student2._User__userID] = student2

    student3 = Student("Charlie", next_user_id, "charlie@student.com", "Password123", "21-67890", "BS Computer Science")
    next_user_id += 1
    vehicle3 = Vehicle(student3, "CAR6789", "Car")
    vehicle3.register_vehicle()
    users[student3._User__userID] = student3

    student4 = Student("John", next_user_id, "john@student.com", "Password123", "21-12378", "BS Computer Science")
    next_user_id += 1
    vehicle4 = Vehicle(student4, "CAR012", "Car")
    vehicle4.register_vehicle()
    users[student4._User__userID] = student4

    for user_id, user in users.items():
        print(f"User ID: {user_id}, Name: {user.name}")
        vehicles = user.get_vehicles()
        if vehicles:
            print("  Registered Vehicles:")
            for vehicle in vehicles:
                print(f"    - {vehicle.get_license_plate()} ({vehicle.get_vehicle_type()})")
        else:
            print("  No registered vehicles.")
            
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
                if isinstance(found_user, Admin):
                    admin_dashboard(found_user)
                else:
                    main_system(found_user)
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
