class User:
    def __init__(self, name: str, user_id: int, email: str, password: str):
        self.name = name            
        self.__userID = user_id     
        self.__email = email        
        self.__password = password  

    def login(self, email: str, password: str):
        if email == self.__email and password == self.__password:
            print(f"{self.name} logged in successfully.")
        else:
            print("Invalid email or password.")

    def logout(self):
        print(f"{self.name} has logged out.")

    def register_vehicle(self, vehicle_plate: str):
        print(f"Vehicle with plate {vehicle_plate} registered for {self.name}.")

    def reserve_parking(self, parking_spot: str):
        print(f"{self.name} reserved parking spot {parking_spot}.")



