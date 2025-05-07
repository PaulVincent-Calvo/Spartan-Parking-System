import unittest
import sys
import os
import io
from unittest.mock import patch

# Add the parent directory to path so we can import the main module
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Import the functions to test
from main import (
    is_valid_email,
    is_valid_password,
    is_valid_sr_code,
    register_user,
    clear_screen
)
from classes.student import Student
from classes.vehicle import Vehicle


class TestStudentAccountRegistration(unittest.TestCase):
    """Functional testing for Student Account Registration process."""
    
    def setUp(self):
        """Set up test environment before each test."""
        # Ensure we start with a clean environment
        self.original_stdout = sys.stdout
    
    def tearDown(self):
        """Clean up after each test."""
        sys.stdout = self.original_stdout
    
    def test_validation_functions(self):
        """Test the validation functions used in student registration."""
        # Email validation
        self.assertTrue(is_valid_email("student@example.com"))
        self.assertFalse(is_valid_email("invalid-email"))
        
        # Password validation
        self.assertTrue(is_valid_password("SecurePass123"))
        self.assertFalse(is_valid_password("short"))
        
        # SR Code validation
        self.assertTrue(is_valid_sr_code("21-12345"))
        self.assertFalse(is_valid_sr_code("invalid"))
    
    @patch('builtins.input')
    def test_student_registration_success(self, mock_input):
        """
        TEST CASE: Student Registration with Valid Credentials
        
        Test Description: Validates the successful registration of a new student user with 
                         valid credentials and proper vehicle registration.
        """
        # Set up mock inputs for student registration
        mock_input.side_effect = [
            "1",                  # Select student type
            "John Doe",           # Name
            "john.doe@email.com", # Email
            "Password123",        # Password (valid format)
            "21-12345",           # SR Code (valid format)
            "1",                  # Course: BS Computer Science
            "ABC1234",            # License plate
            "1"                   # Vehicle type: Car
        ]
        
        with patch('main.next_user_id', 100), patch('main.clear_screen'):
            # Redirect stdout to capture print statements
            captured_output = io.StringIO()
            sys.stdout = captured_output
            
            # Execute the registration
            user = register_user()
            
            # Reset stdout
            sys.stdout = self.original_stdout
            
            # Verify the student was created correctly
            self.assertIsNotNone(user)
            self.assertIsInstance(user, Student)
            self.assertEqual(user.name, "John Doe")
            self.assertEqual(user._User__email, "john.doe@email.com")
            self.assertEqual(user._User__password, "Password123")
            self.assertEqual(user._Student__srCode, "21-12345")
            self.assertEqual(user._Student__course, "BS Computer Science")
            
            # Verify the vehicle was registered
            vehicles = user.get_vehicles()
            self.assertEqual(len(vehicles), 1)
            self.assertEqual(vehicles[0].get_license_plate(), "ABC1234")
            self.assertEqual(vehicles[0].get_vehicle_type(), "Car")
            
            # Check output messages
            output_text = captured_output.getvalue()
            self.assertIn("Vehicle Registration", output_text)
    
    @patch('builtins.input')
    def test_student_registration_invalid_email_correction(self, mock_input):
        """
        TEST CASE: Student Registration with Initially Invalid Email
        
        Test Description: Validates that the system prompts for correction when an invalid 
                         email is entered and then proceeds with registration upon receiving valid input.
        """
        # First provide invalid email, then correct it
        mock_input.side_effect = [
            "1",                  # Select student type
            "Jane Smith",         # Name
            "invalid-email",      # Invalid Email
            "jane.smith@email.com", # Valid Email
            "Password123",        # Password
            "21-54321",           # SR Code
            "2",                  # Course: BS Information Technology
            "XYZ5678",            # License plate
            "2"                   # Vehicle type: Motorcycle
        ]
        
        with patch('main.next_user_id', 101), patch('main.clear_screen'):
            # Redirect stdout to capture print statements
            captured_output = io.StringIO()
            sys.stdout = captured_output
            
            # Execute the registration
            user = register_user()
            
            # Reset stdout
            sys.stdout = self.original_stdout
            
            # Verify the student was created with the corrected email
            self.assertIsNotNone(user)
            self.assertEqual(user._User__email, "jane.smith@email.com")
            self.assertEqual(user._Student__course, "BS Information Technology")
            
            # Check output messages
            output_text = captured_output.getvalue()
            self.assertIn("Invalid email format", output_text)
    
    @patch('builtins.input')
    def test_student_registration_invalid_password_correction(self, mock_input):
        """
        TEST CASE: Student Registration with Initially Invalid Password
        
        Test Description: Validates that the system prompts for correction when an invalid 
                         password is entered and then proceeds with registration upon receiving valid input.
        """
        # First provide invalid password, then correct it
        mock_input.side_effect = [
            "1",                  # Select student type
            "Alex Johnson",       # Name
            "alex@email.com",     # Email
            "short",              # Invalid Password
            "SecurePass123",      # Valid Password
            "21-98765",           # SR Code
            "1",                  # Course: BS Computer Science
            "DEF9012",            # License plate
            "1"                   # Vehicle type: Car
        ]
        
        with patch('main.next_user_id', 102), patch('main.clear_screen'):
            # Redirect stdout to capture print statements
            captured_output = io.StringIO()
            sys.stdout = captured_output
            
            # Execute the registration
            user = register_user()
            
            # Reset stdout
            sys.stdout = self.original_stdout
            
            # Verify the student was created with the corrected password
            self.assertIsNotNone(user)
            self.assertEqual(user._User__password, "SecurePass123")
            
            # Check output messages
            output_text = captured_output.getvalue()
            self.assertIn("Password must be at least 10 characters long", output_text)
    
    @patch('builtins.input')
    def test_student_registration_invalid_sr_code_correction(self, mock_input):
        """
        TEST CASE: Student Registration with Initially Invalid SR Code
        
        Test Description: Validates that the system prompts for correction when an invalid 
                         SR Code is entered and then proceeds with registration upon receiving valid input.
        """
        # First provide invalid SR Code, then correct it
        mock_input.side_effect = [
            "1",                  # Select student type
            "Chris Davis",        # Name
            "chris@email.com",    # Email
            "Password123",        # Password
            "invalid",            # Invalid SR Code
            "21-45678",           # Valid SR Code
            "2",                  # Course: BS Information Technology
            "GHI3456",            # License plate
            "2"                   # Vehicle type: Motorcycle
        ]
        
        with patch('main.next_user_id', 103), patch('main.clear_screen'):
            # Redirect stdout to capture print statements
            captured_output = io.StringIO()
            sys.stdout = captured_output
            
            # Execute the registration
            user = register_user()
            
            # Reset stdout
            sys.stdout = self.original_stdout
            
            # Verify the student was created with the corrected SR Code
            self.assertIsNotNone(user)
            self.assertEqual(user._Student__srCode, "21-45678")
            
            # Check output messages
            output_text = captured_output.getvalue()
            self.assertIn("Invalid SR Code format", output_text)


if __name__ == "__main__":
    unittest.main()
