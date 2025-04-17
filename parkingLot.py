from user import User
from staff import Staff
from vehicle import Vehicle

class ParkingLot:
    def __init__(self, slotId: int, isForStaff: bool = False):
        self.__slotId = slotId
        self.__isOccupied = False
        self.__isForStaff = isForStaff
        self.__reservedBy = None
        self.__spaceAvailable = 1.0  

    def get_slot_id(self):
        return self.__slotId

    def is_occupied(self):
        return self.__spaceAvailable <= 0

    def is_for_staff(self):
        return self.__isForStaff

    def reserve(self, user: User, vehicle: Vehicle):
        if self.is_occupied():
            print(f"Slot {self.__slotId} is fully occupied.")
            return False

        if self.__isForStaff and not isinstance(user, Staff):
            print(f"Slot {self.__slotId} is reserved for staff only.")
            return False

        if self.__spaceAvailable >= vehicle.get_space_taken():
            if self.__spaceAvailable < 1.0 and vehicle.get_space_taken() == 1.0:
                print(f"Cannot park a car in slot {self.__slotId} because it already has a motorcycle.")
                return False

            self.__spaceAvailable -= vehicle.get_space_taken()
            self.__reservedBy = user  # Ensure the user is correctly set
            print(f"Slot {self.__slotId} reserved by {user.name} for vehicle {vehicle.get_license_plate()}.")
            return True
        else:
            print(f"Not enough space in slot {self.__slotId} for vehicle {vehicle.get_license_plate()}.")
            return False

    def release(self, user: User, vehicle: Vehicle):
        if self.__reservedBy != user:
            print(f"Error: Slot {self.__slotId} is not reserved by {user.name}.")
            return False

        if self.__spaceAvailable + vehicle.get_space_taken() > 1.0:
            print(f"Error: Vehicle {vehicle.get_license_plate()} is not parked in slot {self.__slotId}.")
            return False

        self.__spaceAvailable += vehicle.get_space_taken()
        if self.__spaceAvailable == 1.0:  # Reset reservedBy if the slot is fully empty
            self.__reservedBy = None
        print(f"Vehicle {vehicle.get_license_plate()} has departed from slot {self.__slotId}.")
        return True
