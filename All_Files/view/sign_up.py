import sys
import os
from PyQt5 import uic
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (QMainWindow, QApplication, QPushButton, QLineEdit, QCheckBox, QLabel)
from PyQt5.QtCore import *
from All_Files.controller.AccountLogic import AccountCreation




sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


class SignUp(QMainWindow):
    """
    SignUp class handles user registration in a PyQt5 application.
    It manages user input validation, password strength checking, and account creation.
    """
    
    signal = pyqtSignal()
    
    def __init__(self, parent=None):
        """
        Initializes the SignUp window, loads the UI, and connects UI elements to functions.
        """
        
        super(SignUp, self).__init__(parent)
        uic.loadUi(os.path.join(os.path.dirname(__file__), "UI files", "signup.ui"), self)
        
        self.account = AccountCreation()
        
        self.email = self.findChild(QLineEdit, 'email')
        self.password = self.findChild(QLineEdit, 'password')
        self.fullname = self.findChild(QLineEdit, 'fullname')
        self.confirm_password = self.findChild(QLineEdit, 'confirm_password_btn')
        
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.confirm_password.setEchoMode(QtWidgets.QLineEdit.Password)
        
        self.char_length_checkbox = self.findChild(QCheckBox, 'char_length_checkbox')
        self.uppercase_checkbox = self.findChild(QCheckBox, 'uppercase_checkbox')
        self.lowercase_checkbox = self.findChild(QCheckBox, 'lowercase_checkbox')
        self.digit_checkbox = self.findChild(QCheckBox, 'digit_checkbox')
        self.special_char_checkbox = self.findChild(QCheckBox, 'special_char_checkbox')
        
        self.show_password_checkbox = self.findChild(QCheckBox, 'show_password_checkbox')
        
        self.error_label = self.findChild(QLabel, "error_label")
        self.register_btn = self.findChild(QPushButton, "register_btn")
        self.cancel_btn = self.findChild(QPushButton, "cancel_btn")
        
        self.show_password_checkbox.toggled.connect(self.show_password)
        
        self.password.textChanged.connect(self.tick_checkbox)
        
        self.register_btn.clicked.connect(self.create_account)
        
        self.cancel_btn.clicked.connect(self.cancel)
        
        self.show()
        
    def create_account(self):
        """
        Attempts to create a new user account using the provided input.
        Displays an error message if the account creation fails.
        """
        
        success, message = self.account.create_account(self.fullname.text(), self.email.text(),
                                                        self.password.text(), self.confirm_password.text())
        
        if success:
            self.error_label.setStyleSheet('color: Black;'
                                            'font-family: MS Gothic')
            self.error_label.setText(message)
            
        else:
            self.error_label.setStyleSheet('color: red;')
            self.error_label.setText(message)
            
    def show_password(self):
        checked = self.show_password_checkbox.isChecked()
        if checked:
            self.password.setEchoMode(QtWidgets.QLineEdit.Normal)
            self.confirm_password.setEchoMode(QtWidgets.QLineEdit.Normal)
        else:
            self.password.setEchoMode(QtWidgets.QLineEdit.Password)
            self.confirm_password.setEchoMode(QtWidgets.QLineEdit.Password)
        
    def tick_checkbox(self):
        """
        Checks the strength of the entered password and updates the corresponding checkboxes.
        """
        
        self.char_length_checkbox.setChecked(False)
        self.uppercase_checkbox.setChecked(False)
        self.digit_checkbox.setChecked(False)
        self.lowercase_checkbox.setChecked(False)
        self.special_char_checkbox.setChecked(False)
        
        if len(self.password.text()) >= 7:
            self.char_length_checkbox.setChecked(True)
        for char in self.password.text():
            if char.isupper():
                self.uppercase_checkbox.setChecked(True)
            if char.isdigit():
                self.digit_checkbox.setChecked(True)
            if char.islower():
                self.lowercase_checkbox.setChecked(True)
            if (not char.isalnum()):
                self.special_char_checkbox.setChecked(True)
               
    def cancel(self):
        """
        Clears input fields, emits a signal, and closes the window.
        """
        
        self.clear_window()
        self.signal.emit()
        self.close()
        
    def clear_window(self):
        """
        Clears all input fields and error messages in the signup form.
        """
        
        self.fullname.clear()
        self.email.clear()
        self.password.clear()
        self.confirm_password.clear()
        self.error_label.setText("")