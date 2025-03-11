import sys
import os
import unittest
from unittest.mock import MagicMock, patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from All_Files.controller.AccountLogic import AccountCreation, AccountDetails
from All_Files.model.write_db import Write_db
from All_Files.model.read_db import Read_db


class TestAccountCreation(unittest.TestCase):

    def setUp(self):
        """Set up mock instances for Write_db."""
        with patch("All_Files.model.write_db.Write_db") as mock_write_db:
            self.mock_write_db_instance = mock_write_db.return_value
            self.account = AccountCreation()
            self.account.db_handler = self.mock_write_db_instance

    def test_create_account_success(self):
        """Test account creation with valid inputs."""
        self.mock_write_db_instance.create_account.return_value = (True, "Account created successfully.")

        result, message = self.account.create_account("Test User", "test@example.com", "Password1!", "Password1!")
        self.assertTrue(result)
        self.assertEqual(message, "Account created successfully.")
        self.mock_write_db_instance.create_account.assert_called_once()

    def test_create_account_failure(self):
        """Test account creation failure due to weak password."""
        self.mock_write_db_instance.create_account.return_value = (False, "Invalid Password!")

        result, message = self.account.create_account("Test User", "test@example.com", "weakpass", "weakpass")
        self.assertFalse(result)
        self.assertEqual(message, "Invalid Password!")

    def test_login_success(self):
        """Test successful login."""
        self.mock_write_db_instance.login.return_value = (True, "", {"idToken": "token"})

        result, message, user = self.account.login("test@example.com", "Password1!")
        self.assertTrue(result)
        self.assertEqual(message, "")
        self.assertIsNotNone(user)

    def test_login_failure(self):
        """Test login failure."""
        self.mock_write_db_instance.login.return_value = (False, "Invalid credentials!", None)

        result, message, user = self.account.login("test@example.com", "wrongpassword")
        self.assertFalse(result)
        self.assertEqual(message, "Invalid credentials!")
        self.assertIsNone(user)

    def test_change_password_success(self):
        """Test successful password change."""
        self.mock_write_db_instance.change_password.return_value = (True, "Password changed successfully.")

        result, message = self.account.change_password("fake_uid", "fake_token", "NewPassword1!", "NewPassword1!")
        self.assertTrue(result)
        self.assertEqual(message, "Password changed successfully.")
        self.mock_write_db_instance.change_password.assert_called_once()

    def test_log_out(self):
        """Test user logout."""
        self.mock_write_db_instance.log_out.return_value = True

        result = self.account.log_out()
        self.assertTrue(result)
        self.mock_write_db_instance.log_out.assert_called_once()

    def test_delete_account_success(self):
        """Test successful account deletion."""
        self.mock_write_db_instance.delete_account.return_value = (True, "Account deleted successfully.")

        result, message = self.account.delete_account("fake_uid", "fake_token")
        self.assertTrue(result)
        self.assertEqual(message, "Account deleted successfully.")
        self.mock_write_db_instance.delete_account.assert_called_once()


class TestAccountDetails(unittest.TestCase):

    def setUp(self):
        """Set up mock instances for Read_db."""
        with patch("All_Files.model.read_db.Read_db") as mock_read_db:
            self.mock_read_db_instance = mock_read_db.return_value
            self.account_details = AccountDetails("fake_uid", "fake_token")
            self.account_details.read_db = self.mock_read_db_instance

    def test_read_user_details(self):
        """Test reading user details."""
        self.mock_read_db_instance.read_user_details.return_value = ("Test User", "hashedpassword", "test@example.com")

        result = self.account_details.read_user_details()
        self.assertEqual(result, ("Test User", "hashedpassword", "test@example.com"))
        self.mock_read_db_instance.read_user_details.assert_called_once()

    def test_read_journal(self):
        """Test reading journal entries."""
        mock_journal = {"2024-01-01": "Journal entry"}
        self.mock_read_db_instance.read_journal.return_value = mock_journal

        result = self.account_details.read_journal()
        self.assertEqual(result, mock_journal)
        self.mock_read_db_instance.read_journal.assert_called_once()

    def test_read_stress_level(self):
        """Test reading stress level history."""
        mock_stress = {"2024-01-01": "High"}
        self.mock_read_db_instance.read_stress_level.return_value = mock_stress

        result = self.account_details.read_stress_level()
        self.assertEqual(result, mock_stress)
        self.mock_read_db_instance.read_stress_level.assert_called_once()

    def test_read_mood_level(self):
        """Test reading mood level history."""
        mock_mood = {"2024-01-01": "Happy"}
        self.mock_read_db_instance.read_mood_level.return_value = mock_mood

        result = self.account_details.read_mood_level()
        self.assertEqual(result, mock_mood)
        self.mock_read_db_instance.read_mood_level.assert_called_once()

    def test_get_mood_stress_dates(self):
        """Test getting mood and stress tracking dates."""
        mock_dates = ["2024-01-01", "2024-01-02"]
        self.mock_read_db_instance.get_mood_stress_dates.return_value = mock_dates

        result = self.account_details.get_mood_stress_dates()
        self.assertEqual(result, mock_dates)
        self.mock_read_db_instance.get_mood_stress_dates.assert_called_once()

    def test_get_journal_dates(self):
        """Test getting journal entry dates."""
        mock_dates = ["2024-01-01", "2024-01-02"]
        self.mock_read_db_instance.get_journal_dates.return_value = mock_dates

        result = self.account_details.get_journal_dates()
        self.assertEqual(result, mock_dates)
        self.mock_read_db_instance.get_journal_dates.assert_called_once()

    def test_get_mood_dates(self):
        """Test getting mood tracking dates."""
        mock_dates = ["2024-01-01", "2024-01-02"]
        self.mock_read_db_instance.get_mood_dates.return_value = mock_dates

        result = self.account_details.get_mood_dates()
        self.assertEqual(result, mock_dates)
        self.mock_read_db_instance.get_mood_dates.assert_called_once()

    def test_get_stress_dates(self):
        """Test getting stress tracking dates."""
        mock_dates = ["2024-01-01", "2024-01-02"]
        self.mock_read_db_instance.get_stress_dates.return_value = mock_dates

        result = self.account_details.get_stress_dates()
        self.assertEqual(result, mock_dates)
        self.mock_read_db_instance.get_stress_dates.assert_called_once()


if __name__ == "__main__":
    unittest.main()
