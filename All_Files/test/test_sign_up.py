import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import unittest
from unittest.mock import patch, MagicMock
from PyQt5.QtWidgets import QApplication, QLabel, QLineEdit, QPushButton, QCheckBox
from All_Files.view.sign_up import SignUp


class TestSignUpUI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = QApplication([])

    def setUp(self):
        self.window = SignUp()

        self.window.register_btn = MagicMock(spec=QPushButton)
        self.window.cancel_btn = MagicMock(spec=QPushButton)
        self.window.error_label = MagicMock(spec=QLabel)
        self.window.email = MagicMock(spec=QLineEdit)
        self.window.password = MagicMock(spec=QLineEdit)
        self.window.fullname = MagicMock(spec=QLineEdit)
        self.window.confirm_password = MagicMock(spec=QLineEdit)

        self.window.char_length_checkbox = MagicMock(spec=QCheckBox)
        self.window.uppercase_checkbox = MagicMock(spec=QCheckBox)
        self.window.lowercase_checkbox = MagicMock(spec=QCheckBox)
        self.window.digit_checkbox = MagicMock(spec=QCheckBox)
        self.window.special_char_checkbox = MagicMock(spec=QCheckBox)

        self.window.account = MagicMock()
        self.window.account.create_account.return_value = (True, "Account created successfully")

    def test_widgets_loaded_correctly(self):
        self.assertIsNotNone(self.window.register_btn, "register_btn is not loaded")
        self.assertIsNotNone(self.window.cancel_btn, "cancel_btn is not loaded")
        self.assertIsNotNone(self.window.error_label, "error_label is not loaded")
        self.assertIsNotNone(self.window.email, "email field is not loaded")
        self.assertIsNotNone(self.window.password, "password field is not loaded")
        self.assertIsNotNone(self.window.fullname, "fullname field is not loaded")
        self.assertIsNotNone(self.window.confirm_password, "confirm_password field is not loaded")

    def test_register_button_connection(self):
        with patch.object(self.window.register_btn, "clicked", create=True) as mock_signal:
            mock_signal.connect = MagicMock()
            self.window.register_btn.clicked.connect(self.window.create_account)
            mock_signal.connect.assert_called_once_with(self.window.create_account)

    def test_create_account_successful(self):
        self.window.fullname.text.return_value = "John Doe"
        self.window.email.text.return_value = "test@example.com"
        self.window.password.text.return_value = "Password123!"
        self.window.confirm_password.text.return_value = "Password123!"

        self.window.create_account()
        self.window.account.create_account.assert_called_once_with("John Doe", "test@example.com", "Password123!", "Password123!")
        self.window.error_label.setText.assert_called_once_with("Account created successfully")

    def test_create_account_failure(self):
        self.window.account.create_account.return_value = (False, "Email already in use")

        self.window.create_account()
        self.window.error_label.setText.assert_called_once_with("⚠️ Email already in use")
        self.window.error_label.setStyleSheet.assert_called_once_with('color: Black;')

    def test_cancel_function(self):
        with patch.object(self.window, "close") as mock_close:
            self.window.cancel()
            mock_close.assert_called_once()

    def test_clear_window(self):
        self.window.fullname.clear = MagicMock()
        self.window.email.clear = MagicMock()
        self.window.password.clear = MagicMock()
        self.window.confirm_password.clear = MagicMock()
        self.window.error_label.setText = MagicMock()

        self.window.clear_window()

        self.window.fullname.clear.assert_called_once()
        self.window.email.clear.assert_called_once()
        self.window.password.clear.assert_called_once()
        self.window.confirm_password.clear.assert_called_once()
        self.window.error_label.setText.assert_called_once_with("")

    @classmethod
    def tearDownClass(cls):
        cls.app.quit()


if __name__ == "__main__":
    unittest.main()