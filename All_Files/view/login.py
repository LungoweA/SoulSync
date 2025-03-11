import sys
import os
from PyQt5 import uic
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QCheckBox, QPushButton, QLineEdit, QLabel, QGroupBox, QMessageBox

# Add the parent directory to the system path to allow module imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from view.menu import MenuWindow
from controller.AccountLogic import AccountCreation
from view.sign_up import SignUp


class LogIn(QMainWindow):
    """
    The LogIn class handles user authentication through the login UI.
    
    Attributes:
        account (AccountCreation): Handles authentication logic.
        login_btn (QPushButton): Button for logging in.
        sign_up_btn (QPushButton): Button for navigating to sign-up.
        error_label (QLabel): Displays login error messages.
        email (QLineEdit): Input field for user email.
        password (QLineEdit): Input field for user password.
    """
    
    def __init__(self, parent=None):
        """Initializes the LogIn window and sets up UI elements and event handlers."""
        
        super(LogIn, self).__init__(parent)
        uic.loadUi(os.path.join(os.path.dirname(__file__), "UI files", "login.ui"), self)
        
        self.account = AccountCreation()
        
        self.login_btn = self.findChild(QPushButton, "login_btn")
        self.sign_up_btn = self.findChild(QPushButton, "sign_up_btn")
        self.error_label = self.findChild(QLabel, "error_label")
        
        self.email = self.findChild(QLineEdit, 'email')
        self.password = self.findChild(QLineEdit, 'password')
        self.show_password_checkbox = self.findChild(QCheckBox, 'show_password_checkbox')
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        
        self.group_box = self.findChild(QGroupBox, 'groupBox')
        
        self.group_box.hide()
        self.show_password_checkbox.toggled.connect(self.show_password)
        self.login_btn.clicked.connect(self.login)
        
        self.sign_up_btn.mousePressEvent = self.signup
        self.show()
        
    def login(self):
        """Attempts to authenticate the user with provided credentials."""
        
        success, message, user = self.account.login(self.email.text(), self.password.text())
        
        if success:
            self.id_token = user["idToken"]
            self.uid = user["localId"]

            self.window(self.uid, self.id_token)
        else:
            self.group_box.show()
            self.group_box.setStyleSheet(
                "background-color: #FFB3B3;"
                "border: 2px solid #FF4D4D;"
                "border-radius: 8px;"
                "padding: 10px;"
                "font-weight: bold;"
                "color: #990000;"
            )
            self.error_label.setStyleSheet('color: Black;')
            self.error_label.setText(f"⚠️  {message}")
            
    
    
    def show_password(self):
        """
        Toggles the visibility of the password entered in the password field based on the state 
        of the 'show_password_checkbox'.

        If the checkbox is checked, the password will be visible in plain text.
        If the checkbox is unchecked, the password will be hidden (displayed as asterisks).

        Parameters:
        None
        """
        
        checked = self.show_password_checkbox.isChecked()
        if checked:
            self.password.setEchoMode(QtWidgets.QLineEdit.Normal)
        else:
            self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        
    
    def clear_window(self):
        """Clears all input fields and error messages."""
        
        self.email.clear()
        self.password.clear()
        self.error_label.setText("")
        self.group_box.hide()
        
    def signup(self, event=None):
        """Opens the sign-up window and closes the login window."""
        
        self.sign_up = SignUp()
        self.sign_up.signal.connect(self.show)
        self.clear_window()
        self.close()
        self.sign_up.show()
        
    def window(self, uid, id_token):
        """Opens the main application window upon successful login."""
        
        self.home = MenuWindow(uid, id_token)  # Opening Menu window after log in
        self.clear_window()
        self.close()
        self.home.show()
