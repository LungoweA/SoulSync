from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QPushButton, QLineEdit, QStackedWidget
import os
from controller.AccountLogic import AccountCreation  # Import authentication logic
from PyQt5.QtWidgets import QCheckBox, QLabel, QMessageBox, QGroupBox


class SettingsWindow(QMainWindow):
    """
    A window for managing user account settings, including password changes and account deletion.

    This class handles interactions with the UI elements related to changing the password, 
    deleting the account, and navigating between settings and the main menu. It also validates 
    the password inputs and displays success or error messages.

    Attributes:
        account_logic (AccountCreation): Handles account-related operations like password change.
        uid (str): User ID for the current session.
        id_token (str): Authentication token for the user.
        new_password_btn (QPushButton): Button to initiate password change.
        delete_account_btn_2 (QPushButton): Button to initiate account deletion.
        back_menu_btn (QPushButton): Button to navigate back to the main menu.
        confirm_change_btn (QPushButton): Button to confirm the password change.
        cancel_password_btn (QPushButton): Button to cancel password change and return to main menu.
        delete_account_btn (QPushButton): Button to confirm account deletion.
        cancel_delete_btn (QPushButton): Button to cancel account deletion and return to main menu.
        char_length_checkbox (QCheckBox): Checkbox to validate password length.
        uppercase_checkbox (QCheckBox): Checkbox to validate the presence of uppercase letters.
        lowercase_checkbox (QCheckBox): Checkbox to validate the presence of lowercase letters.
        digit_checkbox (QCheckBox): Checkbox to validate the presence of digits.
        special_char_checkbox (QCheckBox): Checkbox to validate the presence of special characters.
        new_password (QLineEdit): Input field for the new password.
        confirm_password (QLineEdit): Input field for confirming the new password.
        error_label (QLabel): Label to display error or success messages.
        group_box (QGroupBox): Group box containing error/success message UI.
        stackedWidget (QStackedWidget): Widget used to navigate between different screens.
    """
    
    def __init__(self, uid, id_token):
        super().__init__()
        
        uic.loadUi(os.path.join(os.path.dirname(__file__), "UI files", "settings.ui"), self)
        
        self.account_logic = AccountCreation()
        self.id_token = id_token  # Store user session token
        self.uid = uid
        
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

        self.new_password = self.findChild(QLineEdit, "new_password")
        self.confirm_password = self.findChild(QLineEdit, "confirm_password")
        
        self.error_label = self.findChild(QLabel, "error_label")
        self.group_box = self.findChild(QGroupBox, "groupBox")
        
        self.stackedWidget = self.findChild(QStackedWidget, "stackedWidget")
        self.stackedWidget.setCurrentIndex(0)

        self.new_password_btn.clicked.connect(self.show_change_password)
        self.delete_account_btn_2.clicked.connect(self.show_delete_account)

        self.confirm_change_btn.clicked.connect(self.change_password)
        self.cancel_password_btn.clicked.connect(self.show_main_menu)
        self.delete_account_btn.clicked.connect(self.confirm_delete_account)
        self.cancel_delete_btn.clicked.connect(self.show_main_menu)
        self.back_menu_btn.clicked.connect(self.go_back_to_menu)
        
        self.new_password.textChanged.connect(self.tick_checkbox)
        
        self.group_box.hide()
        
        
    def show_main_menu(self):
        """ Switch to Page 1 (Main Settings Menu) """
        self.stackedWidget.setCurrentIndex(0)
        self.group_box.hide()
        self.error_label.clear()

    def show_change_password(self):
        """ Switch to Page 2 (Change Password) """
        self.stackedWidget.setCurrentIndex(1)

    def show_delete_account(self):
        """ Switch to Page 3 (Delete Account) """
        self.stackedWidget.setCurrentIndex(2)

    def change_password(self):
        """
        Attempts to change the user's password and updates the UI based on the result.

        Retrieves the new and confirmed passwords, validates them using `AccountCreation`, 
        and displays success or error messages with appropriate styling.
        """
        
        new_password = self.new_password.text()
        confirm_password = self.confirm_password.text()
        
        # Call AccountLogic to handle password validation and change
        account_logic = AccountCreation()
        success, message = account_logic.change_password(self.uid, self.id_token, new_password, confirm_password)

        if success:
            self.show_success_message(message)
        else:
            self.show_failure_message(message)
            
            
    def show_success_message(self, message):
        """
        Displays a success message with styled UI feedback.

        Shows `group_box` with green styling and updates `error_label` with the provided success message.
        Clears the password input fields.
        """
    
        self.group_box.show()
        self.group_box.setStyleSheet(
            """
            background-color: #B3FFB3;
            border: 2px solid #4DCC4D;
            border-radius: 8px;
            padding: 10px;
            font-weight: bold;
            """
        )
        self.error_label.setStyleSheet("color: black;")
        self.error_label.setText(f"✅ {message}")
        self.new_password.clear()
        self.confirm_password.clear()
        
        
    def show_failure_message(self, message):
        """
        Displays a failure message with styled UI feedback.

        Shows `group_box` with red styling and updates `error_label` with the provided error message.
        Clears the password input fields.
        """
    
        self.group_box.show()
        self.group_box.setStyleSheet(
            "background-color: #FFB3B3;"
            "border: 2px solid #FF4D4D;"
            "border-radius: 8px;"
            "padding: 10px;"
            "font-weight: bold;"
            "color: #990000;"
        )
        self.error_label.setStyleSheet("color: black;")  # Set error color for visibility
        self.error_label.setText(f"❌ {message}")
        self.new_password.clear()
        self.confirm_password.clear()
        
        
    def tick_checkbox(self):
        """
        Checks the strength of the entered password and updates the corresponding checkboxes.
        """
        
        self.char_length_checkbox.setChecked(False)
        self.uppercase_checkbox.setChecked(False)
        self.digit_checkbox.setChecked(False)
        self.lowercase_checkbox.setChecked(False)
        self.special_char_checkbox.setChecked(False)
        
        if len(self.new_password.text()) >= 7:
            self.char_length_checkbox.setChecked(True)
        for char in self.new_password.text():
            if char.isupper():
                self.uppercase_checkbox.setChecked(True)
            if char.isdigit():
                self.digit_checkbox.setChecked(True)
            if char.islower():
                self.lowercase_checkbox.setChecked(True)
            if (not char.isalnum()):
                self.special_char_checkbox.setChecked(True)

    
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
        
        success, message = self.account_logic.delete_account(self.uid, self.id_token)

        if success:
            QMessageBox.information(self, "Account Deleted", message)

            # Instead of logging out, switch directly to the login screen
            self.switch_to_login()
        else:
            QMessageBox.warning(self, "Error", f"❌ Failed to delete account!\n{message}")
        
        
    def switch_to_login(self):
        """Force close settings window and open the login window."""
        
        # Import inside function to avoid circular import issues
        from All_Files.view.login import LogIn
        self.login_window = LogIn()
        self.login_window.show()
        self.close()

    def go_back_to_menu(self):
        """Closes settings window and open the menu window."""
        
        from All_Files.view.menu import MenuWindow
        self.menu_window = MenuWindow(self.uid, self.id_token)
        self.menu_window.show()
        self.close()
