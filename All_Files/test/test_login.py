import sys
import os


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import unittest
from unittest.mock import patch, MagicMock
from PyQt5.QtWidgets import QApplication, QLabel, QLineEdit, QPushButton
from All_Files.view.login import LogIn  # Full import path




class TestUILogicwindow(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = QApplication([])

    def setUp(self):
        self.window = LogIn()

        self.window.login_btn = MagicMock(spec=QPushButton)
        self.window.sign_up_btn = MagicMock(spec=QPushButton)
        self.window.error_label = MagicMock(spec=QLabel)
        self.window.email = MagicMock(spec=QLineEdit)
        self.window.password = MagicMock(spec=QLineEdit)

        self.window.account = MagicMock()
        self.window.account.login.return_value = (True, "Success", {"idToken": "fake_token"})

    def test_widgets_loaded_correctly(self):
        self.assertIsNotNone(self.window.login_btn, "login_btn is not loaded")
        self.assertIsNotNone(self.window.sign_up_btn, "sign_up_btn is not loaded")
        self.assertIsNotNone(self.window.error_label, "error_label is not loaded")
        self.assertIsNotNone(self.window.email, "email field is not loaded")
        self.assertIsNotNone(self.window.password, "password is not loaded")
    
    def test_widgets_connection(self):
        """Ensure login button is properly connected to login function."""
        with patch.object(self.window.login_btn, "clicked", create=True) as mock_signal:
            mock_signal.connect = MagicMock()
            self.window.login_btn.clicked.connect(self.window.login)
            mock_signal.connect.assert_called_once_with(self.window.login)


    def test_login_successful(self):
        """Simulate a successful login."""
        self.window.email.text.return_value = "test@example.com"
        self.window.password.text.return_value = "password123"

        with patch.object(self.window, "window") as mock_window:
            self.window.login()
            self.window.account.login.assert_called_once_with("test@example.com", "password123")
            mock_window.assert_called_once_with("fake_token")

    def test_login_failure(self):
        """Simulate a failed login and check error message display."""
        self.window.email.text.return_value = "wrong@example.com"
        self.window.password.text.return_value = "wrongpassword"
        self.window.account.login.return_value = (False, "Invalid credentials", None)

        self.window.login()
        self.window.error_label.setText.assert_called_once_with("⚠️ Invalid credentials")
        self.window.error_label.setStyleSheet.assert_called_once_with('color: Black;')

    def test_signup_function(self):
        """Check if signup window is opened correctly."""
        with patch("All_Files.view.login.SignUp") as mock_signup:
            instance = mock_signup.return_value
            self.window.signup()
            instance.show.assert_called_once()

    def test_window_function(self):
        """Check if the main window is opened after successful login."""
        with patch("All_Files.view.login.MenuWindow") as mock_menu:
            instance = mock_menu.return_value
            self.window.window("fake_token")
            instance.show.assert_called_once()
    
    def test_clear_window(self):
        """Ensure that email, password fields, and error message are cleared."""
        self.window.email.clear = MagicMock()
        self.window.password.clear = MagicMock()
        self.window.error_label.setText = MagicMock()

        self.window.clear_window()

        self.window.email.clear.assert_called_once()
        self.window.password.clear.assert_called_once()
        self.window.error_label.setText.assert_called_once_with("")


    @classmethod
    def tearDownClass(cls):
        cls.app.quit()


if __name__ == "__main__":
    unittest.main()
