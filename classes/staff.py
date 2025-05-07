import re
from .user import User

class Staff(User):
    def __init__(self, name: str, user_id: int, email: str, password: str, staff_code: str, department: str):

        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
            raise ValueError("Invalid email format")

        if len(password) < 10 or not any(c.isupper() for c in password) or not any(c.isdigit() for c in password):
            raise ValueError("Password must be at least 10 characters long, contain an uppercase letter, and include a number")

        if not re.match(r'^\d{2}-\d{5}$', staff_code):
            raise ValueError("Invalid staff code format. Expected format: 'xx-xxxxx'")

        super().__init__(name, user_id, email, password)
        self.__staffCode = staff_code
        self.__department = department

    def accessStaffParking(self):
        print(f"Staff {self.name} with code {self.__staffCode} has accessed staff parking.")

    def get_staff_code(self):  # Add this method
        return self.__staffCode