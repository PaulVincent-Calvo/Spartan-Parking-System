from .user import User

class Vehicle:
    def __init__(self, owner: User, licensePlate: str, vehicleType: str):
        self.__owner = owner  # composition - vehicle has an owner (User)
        self.__licensePlate = licensePlate
        self.__vehicleType = vehicleType
        self.__isRegistered = False
        self.__isParked = False
        self.__spaceTaken = 1 if vehicleType == "Car" else 0.5 

    def get_owner(self):
        return self.__owner

    def get_license_plate(self):
        return self.__licensePlate

    def get_vehicle_type(self):
        return self.__vehicleType

    def get_space_taken(self):
        return self.__spaceTaken

    def is_registered(self):
        return self.__isRegistered

    def is_parked(self):
        return self.__isParked

    def register_vehicle(self):
        if not self.__isRegistered:
            if self.__owner.register_vehicle(self):  
                self.__isRegistered = True
                print(f"Vehicle {self.__licensePlate} registered successfully.")
            else:
                print(f"Vehicle {self.__licensePlate} registration failed.")
        else:
            print(f"Vehicle {self.__licensePlate} is already registered.")

    def park_vehicle(self):
        if not self.__isParked:
            self.__isParked = True
            print(f"Vehicle {self.__licensePlate} is now parked.")
        else:
            print(f"Vehicle {self.__licensePlate} is already parked.")

    def unpark_vehicle(self):
        if self.__isParked:
            self.__isParked = False
            print(f"Vehicle {self.__licensePlate} is now unparked.")
        else:
            print(f"Vehicle {self.__licensePlate} is already unparked.")
