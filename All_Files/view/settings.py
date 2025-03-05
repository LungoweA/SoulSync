from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QPushButton, QLineEdit, QStackedWidget
import os
from controller.AccountLogic import AccountCreation  # Import authentication logic
from PyQt5.QtWidgets import QCheckBox, QLabel, QMessageBox


class SettingsWindow(QMainWindow):
    def __init__(self, id_token):
        super().__init__()
        self.id_token = id_token  # Store user session token
        uic.loadUi(os.path.join(os.path.dirname(__file__), "UI files", "settings.ui"), self)
        self.account_logic = AccountCreation()

        self.new_password_btn = self.findChild(QPushButton, "new_password_btn")
        self.delete_account_btn_2 = self.findChild(QPushButton, "delete_account_btn_2")
        self.back_menu_btn = self.findChild(QPushButton, "back_menu_btn")
        self.confirm_change_btn = self.findChild(QPushButton, "confirm_change_btn")
        self.cancel_password_btn = self.findChild(QPushButton, "cancel_password_btn")
        self.delete_account_btn = self.findChild(QPushButton, "delete_account_btn")
        self.cancel_delete_btn = self.findChild(QPushButton, "cancel_delete_btn")
        self.char_length_checkbox = self.findChild(QCheckBox, "char_length_checkbox")
        self.uppercase_checkbox = self.findChild(QCheckBox, "uppercase_checkbox")
        self.lowercase_checkbox = self.findChild(QCheckBox, "lowercase_checkbox")
        self.digit_checkbox = self.findChild(QCheckBox, "digit_checkbox")
        self.special_char_checkbox = self.findChild(QCheckBox, "special_char_checkbox")

        self.current_password = self.findChild(QLineEdit, "current_password")
        self.new_password = self.findChild(QLineEdit, "new_password")
        self.confirm_password_btn = self.findChild(QLineEdit, "confirm_password_btn")
        self.new_password.textChanged.connect(self.check_password_strength)

        self.stackedWidget = self.findChild(QStackedWidget, "stackedWidget")
        self.stackedWidget.setCurrentIndex(0)

        self.new_password_btn.clicked.connect(self.show_change_password)
        self.delete_account_btn_2.clicked.connect(self.show_delete_account)

        self.confirm_change_btn.clicked.connect(self.change_password)
        self.cancel_password_btn.clicked.connect(self.show_main_menu)
        self.delete_account_btn.clicked.connect(self.confirm_delete_account)
        self.cancel_delete_btn.clicked.connect(self.show_main_menu)
        self.back_menu_btn.clicked.connect(self.go_back_to_menu)

        self.error_label = self.findChild(QLabel, "error_label")
        if self.error_label:
            self.error_label.hide()  # Hide initially
            self.error_label.setText("")  # Ensure it's empty
            self.error_label.setStyleSheet("color: red;")  # Default to red text for errors
            self.error_label.setSizePolicy(self.error_label.sizePolicy().Minimum, self.error_label.sizePolicy().Minimum)  # Prevent extra spacing
        else:
            print("Error: Could not find 'error_label' in the UI file.")

    def show_main_menu(self):
        """ Switch to Page 1 (Main Settings Menu) """
        self.stackedWidget.setCurrentIndex(0)

    def show_change_password(self):
        """ Switch to Page 2 (Change Password) """
        self.stackedWidget.setCurrentIndex(1)

    def show_delete_account(self):
        """ Switch to Page 3 (Delete Account) """
        self.stackedWidget.setCurrentIndex(2)

    def change_password(self):
        """ Call Firebase function to change password with validation """
        old_password = self.current_password.text().strip()
        new_password = self.new_password.text().strip()
        confirm_password = self.confirm_password_btn.text().strip()

        # Find error label
        self.error_label = self.findChild(QLabel, "error_label")

        # Reset error label before validation
        if self.error_label:
            self.error_label.hide()
            self.error_label.setText("")  # Clear previous error messages

        # Check if fields are empty
        if not old_password or not new_password or not confirm_password:
            if self.error_label:
                self.error_label.setText("❌ All fields must be filled!")
                self.error_label.show()
            return

        # Check if new passwords match
        if new_password != confirm_password:
            if self.error_label:
                self.error_label.setText("❌ New password and confirm password do not match!")
                self.error_label.show()
            return

        # Call AccountLogic to handle password validation and change
        account_logic = AccountCreation()
        success, message = account_logic.change_password(self.id_token, old_password, new_password)

        if success:
            print("✅ Password changed successfully!")
            self.new_password.clear()
            self.confirm_password_btn.clear()
            self.current_password.clear()
            if self.error_label:
                self.error_label.setStyleSheet("color: green;")
                self.error_label.setText("✅ Password changed successfully!")
                self.error_label.show()
        else:
            if self.error_label:
                self.error_label.setStyleSheet("color: red;")  # Set error color for visibility
                self.error_label.setText(f"❌ {message}")
                self.error_label.show()

    def check_password_strength(self):
        """ Updates the checkboxes based on password strength by calling AccountLogic.py """
        password = self.new_password.text()

        # Get password strength checks from AccountLogic
        account_logic = AccountCreation()
        strength = account_logic.check_password_strength(password)

        # Find the password strength checkboxes
        checkboxes = {
            "char_length_checkbox": self.char_length_checkbox,
            "uppercase_checkbox": self.uppercase_checkbox,
            "lowercase_checkbox": self.lowercase_checkbox,
            "digit_checkbox": self.digit_checkbox,
            "special_char_checkbox": self.special_char_checkbox
        }

        # Check if all checkboxes exist before updating
        if not all(checkboxes.values()):
            print("❌ ERROR: One or more checkboxes were not found in the UI.")
            return

        # Update checkboxes based on strength criteria
        self.char_length_checkbox.setChecked(strength["char_length"])
        self.uppercase_checkbox.setChecked(strength["uppercase"])
        self.lowercase_checkbox.setChecked(strength["lowercase"])
        self.digit_checkbox.setChecked(strength["digit"])
        self.special_char_checkbox.setChecked(strength["special_char"])

    def confirm_delete_account(self):
        """Ask the user for confirmation before deleting the account."""
        reply = QMessageBox.question(
            self, "Delete Account",
            "Are you sure you want to delete your account?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            self.delete_account()

    def delete_account(self):
        """Deletes account and redirects to login screen."""
        success, message = self.account_logic.delete_account(self.id_token)

        if success:
            QMessageBox.information(self, "Account Deleted", message)

            # ✅ Instead of logging out, switch directly to the login screen
            self.switch_to_login()
        else:
            QMessageBox.warning(self, "Error", f"❌ Failed to delete account!\n{message}")

    def log_out_user(self):
        """Logs out user and redirects to the login screen."""
        print("✅ Redirecting user to login screen...")

        # Import LoginWindow inside function to avoid circular import
        try:
            from view.login import LoginWindow
            self.login_window = LoginWindow()
            self.login_window.show()
            self.close()
        except ImportError as e:
            print(f"❌ Error importing LoginWindow: {e}")

    def switch_to_login(self):
        """Force close settings window and open the login window."""
        print("✅ Redirecting user to login screen...")

        # Import inside function to avoid circular import issues
        from view.login import LogIn

        self.login_window = LogIn()
        self.login_window.show()
        self.close()

    def show_message(self, message, success=False):
        """
        Displays a styled message.
        - If success=True -> Green background (success)
        - If success=False -> Red background (error)
        """
        if self.error_label:
            if success:
                # Green background for success
                self.error_label.setStyleSheet(
                    "background-color: #B3FFB3; border: 2px solid #4DCC4D; "
                    "border-radius: 8px; padding: 10px; font-weight: bold; color: black;"
                )
            else:
                # Red background for error
                self.error_label.setStyleSheet(
                    "background-color: #FFB3B3; border: 2px solid #FF4D4D; "
                    "border-radius: 8px; padding: 10px; font-weight: bold; color: #990000;"
                )

            self.error_label.setText(message)
            self.error_label.show()

            # Auto-hide after 3 seconds
            from PyQt5.QtCore import QTimer
            QTimer.singleShot(3000, lambda: self.error_label.hide())

    def go_back_to_menu(self):
        from view.menu import MenuWindow
        self.menu_window = MenuWindow(self.id_token)
        self.menu_window.show()
        self.close()
