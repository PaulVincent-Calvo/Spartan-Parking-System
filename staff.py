from user import User

class Staff(User):  # staff inheriting from user
    def __init__(self, name: str, user_id: int, email: str, password: str, staff_code: str, department: str):
        super().__init__(name, user_id, email, password)
        self.__staffCode = staff_code
        self.__department = department 

    def accessStaffParking(self):
        print(f"Staff {self.name} with code {self.__staffCode} has accessed staff parking.")