from user import User
from admin import Admin
from staff import Staff
from student import Student
from vehicle import Vehicle
from parkingLot import ParkingLot

def main():
    student1 = Student("Student_Hetty", 301, "hetty@student.com", "studentpass", "SR2025", "CS")
    admin1 = Admin("Admin Mike", 1, "admin@example.com", "adminpass")
    staff1 = Staff("Staff_Alice", 201, "alice@staff.com", "staffpass", "STF123", "IT")
    student2 = Student("Student_Bob", 301, "bob@student.com", "studentpass", "SR2025", "CS")

    parking_slots = [ParkingLot(i, isForStaff=(i % 2 == 0)) for i in range(1, 6)]

    vehicle1 = Vehicle(student2, "ABC-123", "Sedan")
    vehicle2 = Vehicle(staff1, "XYZ-789", "SUV")
    vehicle1.register_vehicle()
    vehicle2.register_vehicle()
    
    print("\nAvailable parking slots:")
    for slot in parking_slots:
        print(f"Slot {slot.get_slot_id()}: {'Occupied' if slot.is_occupied() else 'Available'}")

    print("\nAttempting to reserve parking slots:")
    parking_slots[0].reserve(student2)
    parking_slots[1].reserve(staff1) 
    parking_slots[2].reserve(student1) 

    print("\nStaff Parking Access:")
    staff1.accessStaffParking()
    
    print("\nAdmin Actions:")
    admin1.view_dashboard()
    admin1.manage_parking_slot("added", "5")
    admin1.reset_password(301)

if __name__ == "__main__":
    main()
