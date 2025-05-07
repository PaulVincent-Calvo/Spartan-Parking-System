from .user import User

class Admin(User):   # admin inheriting from user
    def __init__(self, name: str, user_id: int, email: str, password: str):
        super().__init__(name, user_id, email, password)
        self.__isAdmin = True  

    def reset_password(self, user, new_password: str):
        old_password = user._User__password  
        if len(new_password) >= 10 and any(c.isupper() for c in new_password) and any(c.isdigit() for c in new_password):
            user._User__password = new_password
            print(f"Admin {self.name} has successfully reset the password for User ID {user.get_user_id()}.")
            print(f"Old Password: {old_password}")
            print(f"New Password: {new_password}")
        else:
            print("Failed: New password does not meet the required criteria (10 characters, at least one uppercase letter, and one number).")

    def view_dashboard(self):
        print(f"Admin {self.name} is viewing the dashboard.")

    def manage_parking_slot(self, action: str, slot_number: str):
        print(f"Admin {self.name} has {action} parking slot {slot_number}.")
