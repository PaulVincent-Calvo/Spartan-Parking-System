from user import User
from admin import Admin
from staff import Staff
from student import Student
from vehicle import Vehicle
from parkingLot import ParkingLot

def main():
    user1 = User("John Doe", 101, "john@example.com", "password123")
    admin1 = Admin("Admin Mike", 1, "admin@example.com", "adminpass")
    staff1 = Staff("Staff_Alice", 201, "alice@staff.com", "staffpass", "STF123", "IT")
    student1 = Student("Student_Bob", 301, "bob@student.com", "studentpass", "SR2025", "CS")

    parking_slots = [ParkingLot(i, isForStaff=(i % 2 == 0)) for i in range(1, 6)]
