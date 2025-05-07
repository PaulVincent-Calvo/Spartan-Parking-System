import os
import io
from unittest.mock import patch


# Import the functions to test
from main import (
    park_vehicle,
    depart_vehicle,
    register_vehicle,
    clear_screen
)
from classes.staff import Staff
from classes.vehicle import Vehicle
from classes.parkingLot import ParkingLot


class TestStaffCarParking(unittest.TestCase):
    """Testing for Staff Car Parking functionality."""
    
    def setUp(self):
        """Set up test environment before each test."""
        self.original_stdout = sys.stdout
        
        # Create a staff member for testing
        self.staff = Staff(
            name="Test Staff",
            userID=100,
            email="staff@example.com",
            password="StaffPass123",
            staffCode="21-54321",
            department="College of Informatics and Computing Sciences"
        )
        
        # Create a car for the staff member
        self.car = Vehicle(self.staff, "CAR1234", "Car")
        self.car.register_vehicle()
        
        # Create test parking slots
        self.test_parking_slots = [
            ParkingLot(slotId=1, isForStaff=False),
            ParkingLot(slotId=2, isForStaff=True),  # Staff only slot
            ParkingLot(slotId=3, isForStaff=False),
            ParkingLot(slotId=4, isForStaff=True)   # Staff only slot
        ]
    
    def tearDown(self):
        """Clean up after each test."""
        sys.stdout = self.original_stdout
    
    @patch('main.parking_slots')
    @patch('builtins.input')
    def test_staff_car_parking_success(self, mock_input, mock_parking_slots):
        """
        TEST CASE: Staff Car Parking in Staff-Only Slot
        
        Test Description: Validates that a staff member can successfully park their car 
                         in a staff-only parking slot.
        """
        # Replace the parking slots with our test slots
        mock_parking_slots.__iter__.return_value = self.test_parking_slots
        
        # Set up mock inputs for parking a car
        mock_input.side_effect = [
            "1",  # Select the first vehicle
            "2"   # Select parking slot 2 (staff only)
        ]
        
        with patch('main.clear_screen'):
            # Redirect stdout to capture print statements
            captured_output = io.StringIO()
            sys.stdout = captured_output
            
            # Execute the parking action
            park_vehicle(self.staff)
            
            # Reset stdout
            sys.stdout = self.original_stdout
            
            # Verify the car is parked
            self.assertTrue(self.car.is_parked())
            
            # Verify the parking slot is occupied
            staff_slot = self.test_parking_slots[1]  # Slot ID 2
            self.assertTrue(staff_slot.is_occupied())
            
            # Check output messages
            output_text = captured_output.getvalue()
            self.assertIn(f"Vehicle {self.car.get_license_plate()} parked in slot 2", output_text)
    
    @patch('main.parking_slots')
    @patch('builtins.input')
    def test_staff_car_departure(self, mock_input, mock_parking_slots):
        """
        TEST CASE: Staff Car Departure from Parking Slot
        
        Test Description: Validates that a staff member can successfully retrieve their car 
                         from a parking slot.
        """
        # Replace the parking slots with our test slots
        mock_parking_slots.__iter__.return_value = self.test_parking_slots
        
        # Mark the car as parked and reserve slot 2
        self.car.park_vehicle()
        staff_slot = self.test_parking_slots[1]  # Slot ID 2
        staff_slot.reserve(self.staff, self.car)
        
        # Set up mock inputs for departing
        mock_input.side_effect = [
            "1"  # Select the first vehicle
        ]
        
        with patch('main.clear_screen'):
            # Redirect stdout to capture print statements
            captured_output = io.StringIO()
            sys.stdout = captured_output
            
            # Execute the departure action
            depart_vehicle(self.staff)
            
            # Reset stdout
            sys.stdout = self.original_stdout
            
            # Verify the car is no longer parked
            self.assertFalse(self.car.is_parked())
            
            # Verify the parking slot is no longer occupied
            self.assertFalse(staff_slot.is_occupied())
            
            # Check output messages
            output_text = captured_output.getvalue()
            self.assertIn(f"Vehicle {self.car.get_license_plate()} has departed successfully", output_text)
    
    @patch('main.parking_slots')
    @patch('builtins.input')
    def test_staff_car_parking_in_regular_slot(self, mock_input, mock_parking_slots):
        """
        TEST CASE: Staff Car Parking in Regular Slot
        
        Test Description: Validates that a staff member can also park their car 
                         in a regular (non-staff) parking slot.
        """
        # Replace the parking slots with our test slots
        mock_parking_slots.__iter__.return_value = self.test_parking_slots
        
        # Set up mock inputs for parking a car
        mock_input.side_effect = [
            "1",  # Select the first vehicle
            "1"   # Select parking slot 1 (regular slot)
        ]
        
        with patch('main.clear_screen'):
            # Redirect stdout to capture print statements
            captured_output = io.StringIO()
            sys.stdout = captured_output
            
            # Execute the parking action
            park_vehicle(self.staff)
            
            # Reset stdout
            sys.stdout = self.original_stdout
            
            # Verify the car is parked
            self.assertTrue(self.car.is_parked())
            
            # Verify the parking slot is occupied
            regular_slot = self.test_parking_slots[0]  # Slot ID 1
            self.assertTrue(regular_slot.is_occupied())
            
            # Check output messages
            output_text = captured_output.getvalue()
            self.assertIn(f"Vehicle {self.car.get_license_plate()} parked in slot 1", output_text)


if __name__ == "__main__":
    unittest.main()
