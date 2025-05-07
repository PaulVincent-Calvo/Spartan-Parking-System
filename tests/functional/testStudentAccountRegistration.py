import sys
import os
import unittest
from unittest.mock import patch, MagicMock
import io

# Add the parent directory to the path to import the functions
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import registration-related functions
from main import (
    register_user,
    is_valid_email,
    is_valid_password,
    is_valid_sr_code,
    register_vehicle,
    users,
    next_user_id
)
from classes.student import Student
from classes.vehicle import Vehicle


class TestStudentRegistration(unittest.TestCase):
    """Functional tests for student registration process"""
    
    def setUp(self):
        """Set up test environment before each test"""
        # Save original values
        self.original_users = users.copy()
        self.original_next_user_id = next_user_id
    
    def tearDown(self):
        """Clean up after each test"""
        # Restore original values
        global users, next_user_id
        users = self.original_users.copy()
        next_user_id = self.original_next_user_id
    
    @patch('builtins.input')
    @patch('main.clear_screen')
    @patch('main.register_vehicle')
    def test_TC001_student_registration_with_valid_credentials(self, mock_register_vehicle, mock_clear, mock_input):
        """
        Test Case ID: TC001
        Test Case Title: Student Registration with Valid Credentials
        Test Description: Validates the successful registration of a new student with valid credentials and proper database integration.
        """
        # Test Data
        test_name = "John Doe"
        test_email = "john.doe@student.com"
        test_password = "Password123"
        test_sr_code = "21-12345"
        test_course = "BS Computer Science"
        
        # Mock the register_vehicle function to return a fake vehicle
        mock_vehicle = MagicMock()
        mock_register_vehicle.return_value = mock_vehicle
        
        # Set up the input sequence for a student registration
        mock_input.side_effect = [
            "1",              # User type - Student
            test_name,        # Name
            test_email,       # Email
            test_password,    # Password
            test_sr_code,     # SR Code
            "1",              # Course - BS Computer Science
        ]
        
        # Execute test steps
        user = register_user()
        
        # Verify expected results
        self.assertIsInstance(user, Student)
        self.assertEqual(user.name, test_name)
        self.assertEqual(user._User__email, test_email)
        self.assertEqual(user._User__password, test_password)
        self.assertEqual(user._Student__srCode, test_sr_code)
        self.assertEqual(user._Student__course, test_course)
        
        # Verify user was added to the users dictionary
        self.assertIn(user._User__userID, users)
        self.assertEqual(users[user._User__userID], user)
        
        # Verify register_vehicle was called with the user
        mock_register_vehicle.assert_called_once_with(user)
    
    @patch('builtins.input')
    @patch('main.clear_screen')
    @patch('main.register_vehicle')
    def test_TC002_student_registration_with_invalid_email(self, mock_register_vehicle, mock_clear, mock_input):
        """
        Test Case ID: TC002
        Test Case Title: Student Registration with Invalid Email
        Test Description: Validates system handling when a student attempts to register with an invalid email format.
        """
        # Test Data
        test_name = "Jane Smith"
        test_invalid_email = "invalid-email"
        test_valid_email = "jane.smith@student.com"
        test_password = "Password123"
        test_sr_code = "21-54321"
        
        # Set up the input sequence with invalid then valid email
        mock_input.side_effect = [
            "1",              # User type - Student
            test_name,        # Name
            test_invalid_email, # Invalid email
            test_valid_email, # Valid email (retry)
            test_password,    # Password
            test_sr_code,     # SR Code
            "1",              # Course - BS Computer Science
        ]
        
        # Mock the register_vehicle function to return a fake vehicle
        mock_vehicle = MagicMock()
        mock_register_vehicle.return_value = mock_vehicle
        
        # Get initial count of users
        initial_user_count = len(users)
        
        # Execute test steps
        with patch('sys.stdout', new=io.StringIO()) as fake_output:
            user = register_user()
            output = fake_output.getvalue()
        
        # Verify expected results
        self.assertIn("Invalid email format", output)
        self.assertIsInstance(user, Student)
        self.assertEqual(user._User__email, test_valid_email)
        self.assertEqual(len(users), initial_user_count + 1)
    
    @patch('builtins.input')
    @patch('main.clear_screen')
    @patch('main.register_vehicle')
    def test_TC003_student_registration_with_invalid_password(self, mock_register_vehicle, mock_clear, mock_input):
        """
        Test Case ID: TC003
        Test Case Title: Student Registration with Invalid Password
        Test Description: Validates system handling when a student attempts to register with a password that doesn't meet complexity requirements.
        """
        # Test Data
        test_name = "Alex Johnson"
        test_email = "alex@student.com"
        test_invalid_password = "short"
        test_valid_password = "StrongPass123"
        test_sr_code = "22-12345"
        
        # Set up the input sequence with invalid then valid password
        mock_input.side_effect = [
            "1",                # User type - Student
            test_name,          # Name
            test_email,         # Email
            test_invalid_password, # Invalid password
            test_valid_password,   # Valid password (retry)
            test_sr_code,       # SR Code
            "2",                # Course - BS Information Technology
        ]
        
        # Mock the register_vehicle function to return a fake vehicle
        mock_vehicle = MagicMock()
        mock_register_vehicle.return_value = mock_vehicle
        
        # Execute test steps
        with patch('sys.stdout', new=io.StringIO()) as fake_output:
            user = register_user()
            output = fake_output.getvalue()
        
        # Verify expected results
        self.assertIn("Password must be at least 10 characters long", output)
        self.assertIsInstance(user, Student)
        self.assertEqual(user._User__password, test_valid_password)
        self.assertEqual(user._Student__course, "BS Information Technology")
    
    @patch('builtins.input')
    @patch('main.clear_screen')
    @patch('main.register_vehicle')
    def test_TC004_student_registration_with_invalid_sr_code(self, mock_register_vehicle, mock_clear, mock_input):
        """
        Test Case ID: TC004
        Test Case Title: Student Registration with Invalid SR Code
        Test Description: Validates system handling when a student attempts to register with an invalid SR code format.
        """
        # Test Data
        test_name = "Michael Brown"
        test_email = "michael@student.com"
        test_password = "Michael123"
        test_invalid_sr_code = "123456"
        test_valid_sr_code = "22-54321"
        
        # Set up the input sequence with invalid then valid SR code
        mock_input.side_effect = [
            "1",                 # User type - Student
            test_name,           # Name
            test_email,          # Email
            test_password,       # Password
            test_invalid_sr_code, # Invalid SR code
            test_valid_sr_code,   # Valid SR code (retry)
            "1",                 # Course - BS Computer Science
        ]
        
        # Mock the register_vehicle function to return a fake vehicle
        mock_vehicle = MagicMock()
        mock_register_vehicle.return_value = mock_vehicle
        
        # Execute test steps
        with patch('sys.stdout', new=io.StringIO()) as fake_output:
            user = register_user()
            output = fake_output.getvalue()
        
        # Verify expected results
        self.assertIn("Invalid SR Code format", output)
        self.assertIsInstance(user, Student)
        self.assertEqual(user._Student__srCode, test_valid_sr_code)
    
    @patch('builtins.input')
    @patch('main.clear_screen')
    @patch('main.register_vehicle')
    def test_TC005_student_registration_with_vehicle(self, mock_register_vehicle, mock_clear, mock_input):
        """
        Test Case ID: TC005
        Test Case Title: Student Registration with Vehicle
        Test Description: Validates the successful registration of a student with a vehicle.
        """
        # Test Data
        test_name = "Sarah Wilson"
        test_email = "sarah@student.com"
        test_password = "Password123"
        test_sr_code = "21-98765"
        
        # Create a mock vehicle to be returned
        mock_vehicle = MagicMock()
        mock_vehicle.get_license_plate.return_value = "ABC123"
        mock_vehicle.get_vehicle_type.return_value = "Car"
        mock_register_vehicle.return_value = mock_vehicle
        
        # Set up the input sequence
        mock_input.side_effect = [
            "1",              # User type - Student
            test_name,        # Name
            test_email,       # Email
            test_password,    # Password
            test_sr_code,     # SR Code
            "1",              # Course - BS Computer Science
        ]
        
        # Execute test steps
        user = register_user()
        
        # Verify expected results
        self.assertIsInstance(user, Student)
        mock_register_vehicle.assert_called_once_with(user)
        
        # Verify vehicle was associated with the user
        # Note: In the actual system, register_vehicle would add the vehicle to user.vehicles
        # Here we just verify that the register_vehicle function was called


if __name__ == '__main__':
    unittest.main()
