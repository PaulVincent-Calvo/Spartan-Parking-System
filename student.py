from user import User

class Student(User):  # student inheriting from user
    def __init__(self, name: str, user_id: int, email: str, password: str, sr_code: str, course: str):
        super().__init__(name, user_id, email, password)
        self.__srCode = sr_code 
        self.course = course 