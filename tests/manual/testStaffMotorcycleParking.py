import os
import sys

# Add the project root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from classes.staff import Staff
from classes.vehicle import Vehicle
from classes.parkingLot import ParkingLot

# Setup: parking slots
parking_slots = [
    ParkingLot(slotId=1, isForStaff=True),
    ParkingLot(slotId=2, isForStaff=False),
    ParkingLot(slotId=3, isForStaff=True),
]

# Staff accounts and motorcycles
staff1 = Staff("Eve", 101, "eve@university.com", "Password123", "SC-00001", "IT Department")
motorcycle1 = Vehicle(staff1, "MC11111", "Motorcycle")
motorcycle1.register_vehicle()

staff2 = Staff("Frank", 102, "frank@university.com", "Password123", "SC-00002", "Admin")
motorcycle2 = Vehicle(staff2, "MC22222", "Motorcycle")
motorcycle2.register_vehicle()

staff3 = Staff("Grace", 103, "grace@university.com", "Password123", "SC-00003", "Library")
motorcycle3 = Vehicle(staff3, "MC33333", "Motorcycle")
motorcycle3.register_vehicle()

# Precondition: Staff1 has already parked their motorcycle in a staff-only slot
parking_slots[0].reserve(staff1, motorcycle1)
motorcycle1.park_vehicle()

# Test cases
test_cases = {
    (staff2, motorcycle2, parking_slots[0]): True,   # Staff2 joins Staff1 in same staff slot (0.5 + 0.5 = 1.0) - should pass
    (staff2, motorcycle2, parking_slots[1]): True,   # Staff2 parks in a public slot - allowed
    (staff3, motorcycle3, parking_slots[0]): False,  # Staff3 tries to park where two motorcycles already exist (1.0 space used)
    (staff3, motorcycle3, parking_slots[2]): True,   # Staff3 parks in an empty staff slot
}

def test_staff_motorcycle_parking():
    os.system('cls' if os.name == 'nt' else 'clear')
    for (user, vehicle, slot), expected_result in test_cases.items():
        user_id = user.get_user_id()
        description = f"Staff {user_id} tries to park {vehicle.get_license_plate()} in slot {slot.get_slot_id()}"
        print(f"\n{description}")
        result = slot.reserve(user, vehicle)

        if result == expected_result:
            if result:
                vehicle.park_vehicle()
                print(f"Success: {vehicle.get_license_plate()} parked in slot {slot.get_slot_id()}")
            else:
                print(f"Success: {vehicle.get_license_plate()} could not park in slot {slot.get_slot_id()}")
        else:
            print(f"Fail: Unexpected result for {vehicle.get_license_plate()} in slot {slot.get_slot_id()}")

if __name__ == "__main__":
    test_staff_motorcycle_parking()
