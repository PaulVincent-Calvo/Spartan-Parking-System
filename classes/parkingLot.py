from .user import User
from .staff import Staff
from .vehicle import Vehicle

class ParkingLot:
    def __init__(self, slotId: int, isForStaff: bool = False):
        self.__slotId = slotId
        self.__isForStaff = isForStaff
        self.__spaceAvailable = 1.0
        self.__reservations = {}  # key = User, value = list of Vehicles
        self.__parkedVehicles = {}  # key = User, value = list of Vehicles

    def get_slot_id(self):
        return self.__slotId

    def is_occupied(self):
        return self.__spaceAvailable < 1.0 or bool(self.__parkedVehicles)

    def is_for_staff(self):
        return self.__isForStaff

    def get_reservations(self):
        return self.__reservations

    def get_parked_vehicles(self):
        return self.__parkedVehicles

    def reserve(self, user: User, vehicle: Vehicle):
        if vehicle.is_parked():
            print(f"Vehicle {vehicle.get_license_plate()} is already parked and cannot be reserved.")
            return False

        if self.__spaceAvailable < vehicle.get_space_taken():
            print(f"Not enough space in slot {self.__slotId} for vehicle {vehicle.get_license_plate()}.")
            return False

        if self.__isForStaff and not isinstance(user, Staff):
            print(f"Slot {self.__slotId} is reserved for staff only.")
            return False

        if any(v.get_vehicle_type() == "Car" for vehicles in self.__reservations.values() for v in vehicles):
            print(f"Slot {self.__slotId} already has a car reserved and cannot accommodate another vehicle.")
            return False

        self.__spaceAvailable -= vehicle.get_space_taken()
        self.__reservations.setdefault(user, []).append(vehicle)
        print(f"Slot {self.__slotId} reserved by {user.name} for vehicle {vehicle.get_license_plate()}.")
        return True

    def park(self, user: User, vehicle: Vehicle):
        if user not in self.__reservations or vehicle not in self.__reservations[user]:
            print(f"Vehicle {vehicle.get_license_plate()} is not reserved in slot {self.__slotId}.")
            return False

        if vehicle.is_parked():
            print(f"Vehicle {vehicle.get_license_plate()} is already parked.")
            return False

        # Remove the reservation for the vehicle
        self.__reservations[user].remove(vehicle)
        if not self.__reservations[user]:
            del self.__reservations[user]

        self.__parkedVehicles.setdefault(user, []).append(vehicle)
        vehicle.park_vehicle()
        print(f"Vehicle {vehicle.get_license_plate()} is now parked in slot {self.__slotId}.")
        return True

    def release(self, user: User, vehicle: Vehicle):
        if user not in self.__parkedVehicles or vehicle not in self.__parkedVehicles[user]:
            print(f"Vehicle {vehicle.get_license_plate()} is not parked in slot {self.__slotId}.")
            return False

        self.__parkedVehicles[user].remove(vehicle)
        if not self.__parkedVehicles[user]:
            del self.__parkedVehicles[user]

        self.__spaceAvailable += vehicle.get_space_taken()
        vehicle.unpark_vehicle()
        print(f"Vehicle {vehicle.get_license_plate()} has departed from slot {self.__slotId}.")
        return True
