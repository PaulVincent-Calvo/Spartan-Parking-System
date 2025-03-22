from user import User
from staff import Staff

class ParkingLot:
    def __init__(self, slotId: int, isForStaff: bool = False):
        self.__slotId = slotId
        self.__isOccupied = False
        self.__isForStaff = isForStaff
        self.__reservedBy = None

    def reserve(self, user: User): # user reserving slot in parking lot
        if self.__isOccupied:
            print(f"Slot {self.__slotId} is already occupied.")
            return False
        if self.__isForStaff and not isinstance(user, Staff):  # only Staff can reserve staff-only slots
            print(f"Slot {self.__slotId} is for staff only.")
            return False
        
        self.__isOccupied = True
        self.__reservedBy = user
        user.reserve_parking(self.__slotId)
        print(f"Slot {self.__slotId} reserved by {user.name}.")
        return True

    def release(self):
        if not self.__isOccupied:
            print(f"Slot {self.__slotId} is already free.")
            return False
        print(f"Slot {self.__slotId} released from {self.__reservedBy.name}.")
        self.__isOccupied = False
        self.__reservedBy = None
        return True
    

