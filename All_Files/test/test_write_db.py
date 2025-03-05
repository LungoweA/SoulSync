import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import unittest
from unittest.mock import patch, MagicMock
from All_Files.model.write_db import Write_db



class TestWriteDb(unittest.TestCase):
    
    def setUp(self):
        self.db = Write_db()

    def test_create_account_success(self):
        # Mock Firebase authentication
        mock_auth = MagicMock()
        mock_auth.create_user_with_email_and_password.return_value = {
            'localId': '123', 
            'idToken': 'token'
        }
        self.db.auth = mock_auth  # Manually set the mock auth on the instance

        # Patch the instance's `database` attribute
        with patch.object(self.db, 'database', new_callable=MagicMock) as mock_database, \
            patch.object(self.db, 'validate_password', return_value=True), \
            patch.object(self.db, 'validate_email', return_value=False):

            # Call create_account
            result, message = self.db.create_account("Test User", "test@example.com", "Password1!", "Password1!")

            # Debugging output
            print("Create Account Result:", result)
            print("Message:", message)

            # Assertions
            self.assertTrue(result, "Expected account creation to succeed, but it failed.")
            self.assertEqual(message, 'Account Created')

            # Ensure data is written to Firebase mock
            mock_database.child.return_value.child.return_value.set.assert_called_once()




    def test_create_account_invalid_password(self):
        with patch.object(self.db, 'validate_password', return_value=False):
            result, message = self.db.create_account("Test User", "test@example.com", "pass", "pass")
            
            self.assertFalse(result)
            self.assertEqual(message, "Invalid Password!")

    def test_create_account_mismatched_passwords(self):
        with patch.object(self.db, 'validate_password', return_value=True):
            result, message = self.db.create_account("Test User", "test@example.com", "Password1!", "Password2!")
            
            self.assertFalse(result)
            self.assertEqual(message, "Passwords don't match, please try again!")

    def test_create_account_invalid_email(self):
        with patch.object(self.db, 'validate_password', return_value=True), \
             patch.object(self.db, 'validate_email', return_value=True):
            
            result, message = self.db.create_account("Test User", "invalid;email@example.com", "Password1!", "Password1!")
            
            self.assertFalse(result)
            self.assertEqual(message, "Email is not allowed!")

    def test_validate_password(self):
        valid_password = "Strong1!"
        invalid_password = "weak"
        self.assertTrue(self.db.validate_password(valid_password))
        self.assertFalse(self.db.validate_password(invalid_password))

    def test_validate_email(self):
        valid_email = "test@example.com"
        invalid_email = "test;example.com"
        self.assertFalse(self.db.validate_email(valid_email))
        self.assertTrue(self.db.validate_email(invalid_email))

    @patch.object(Write_db, 'auth', create=True)
    def test_login_success(self, mock_auth):
        mock_auth.sign_in_with_email_and_password.return_value = {'idToken': 'token'}
        result, message, user = self.db.login("test@example.com", "Password1!")
        self.assertTrue(result)
        self.assertEqual(message, '')
        self.assertIsNotNone(user)
    
    @patch.object(Write_db, 'auth', create=True)
    def test_login_failure(self, mock_auth):
        mock_auth.sign_in_with_email_and_password.side_effect = Exception()
        result, message, user = self.db.login("test@example.com", "wrongpassword")
        self.assertFalse(result)
        self.assertEqual(message, 'Invalid email or Incorrect password!')
        self.assertIsNone(user)

if __name__ == '__main__':
    unittest.main()
