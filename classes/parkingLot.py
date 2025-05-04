from .user import User
from .staff import Staff
from .vehicle import Vehicle

class ParkingLot:
    def __init__(self, slotId: int, isForStaff: bool = False):
        self.__slotId = slotId
        self.__isForStaff = isForStaff
        self.__spaceAvailable = 1.0
        self.__reservations = {}  # key = User, value = list of Vehicles

    def get_slot_id(self):
        return self.__slotId

    def is_occupied(self):
        return self.__spaceAvailable <= 0

    def is_for_staff(self):
        return self.__isForStaff

    def reserve(self, user: User, vehicle: Vehicle):
        if vehicle.is_parked():
            print(f"Vehicle {vehicle.get_license_plate()} is already parked and cannot be parked again.")
            return False

        if self.__spaceAvailable < vehicle.get_space_taken():
            print(f"Not enough space in slot {self.__slotId} for vehicle {vehicle.get_license_plate()}.")
            return False

        if self.__isForStaff and not isinstance(user, Staff):
            print(f"Slot {self.__slotId} is reserved for staff only.")
            return False

        if any(v.get_vehicle_type() == "Car" for vehicles in self.__reservations.values() for v in vehicles):
            print(f"Slot {self.__slotId} already has a car parked and cannot accommodate another vehicle.")
            return False

        self.__spaceAvailable -= vehicle.get_space_taken()
        self.__reservations.setdefault(user, []).append(vehicle)
        print(f"Slot {self.__slotId} reserved by {user.name} for vehicle {vehicle.get_license_plate()}.")
        return True

    def release(self, user: User, vehicle: Vehicle):
        if self.__spaceAvailable + vehicle.get_space_taken() > 1.0:
            print(f"Vehicle {vehicle.get_license_plate()} is not parked in slot {self.__slotId}.")
            return False
        
        if user not in self.__reservations or vehicle not in self.__reservations[user]:
            print(f" Slot {self.__slotId} is not reserved for {user.name}'s {vehicle.get_license_plate()}.")
            return False
        
        self.__spaceAvailable += vehicle.get_space_taken()
        self.__reservations[user].remove(vehicle)
        
        if not self.__reservations[user]:
            del self.__reservations[user]

        print(f"Vehicle {vehicle.get_license_plate()} has departed from slot {self.__slotId}.")
        return True
