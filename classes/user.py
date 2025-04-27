class User:
    def __init__(self, name: str, user_id: int, email: str, password: str):
        self.name = name            
        self.__userID = user_id     
        self.__email = email        
        self.__password = password  
        self.__vehicles = []  

    def get_user_id(self):  # Add this method
        return self.__userID
    
    def get_vehicles(self):
        return self.__vehicles
    
    def login(self, email: str, password: str):
        if email == self.__email and password == self.__password:
            print(f"{self.name} logged in successfully.")
        else:
            print("Invalid email or password.")

    def logout(self):
        print(f"{self.name} has logged out.")

    def register_vehicle(self, vehicle):
        # Check if a vehicle with the same license plate is already registered
        if any(v.get_license_plate() == vehicle.get_license_plate() for v in self.__vehicles):
            print(f"Error: Vehicle with plate {vehicle.get_license_plate()} is already registered for {self.name}.")
            return False
        self.__vehicles.append(vehicle)  # Store the Vehicle object
        print(f"Vehicle with plate {vehicle.get_license_plate()} registered for {self.name}.")
        return True

    def reserve_parking(self, parking_spot: str):
        print(f"{self.name} reserved parking spot {parking_spot}.")



