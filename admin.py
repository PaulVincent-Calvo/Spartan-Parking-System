from user import User

class Admin(User):   # admin inheriting from user
    def __init__(self, name: str, user_id: int, email: str, password: str):
        super().__init__(name, user_id, email, password)
        self.__isAdmin = True  

    def reset_password(self, user_id: int):
        print(f"Admin {self.name} has reset the password for User ID {user_id}.")

    def view_dashboard(self):
        print(f"Admin {self.name} is viewing the dashboard.")

    def manage_parking_slot(self, action: str, slot_number: str):
        print(f"Admin {self.name} has {action} parking slot {slot_number}.")
