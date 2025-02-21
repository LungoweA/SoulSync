import sys
import os
from All_Files.model.write_db import Write_db


# Add the parent directory to the system path to allow module imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


class AccountCreation:
    """
    A class to manage user account operations, including account creation, login, password reset, logout,
    and account deletion. It acts as an interface to interact with the database handler (Write_db).
    """
    
    def __init__(self):
        """
        Initializes the AccountCreation class and sets up the database handler instance.
        """
        
        self.db_handler = Write_db()
        
    def create_account(self, fullname, email, password, confirm_password):
        """
        Creates a new user account by storing user details in the database.
        Args:
            fullname (str): The full name of the user.
            email (str): The user's email address.
            password (str): The user's password.
            confirm_password (str): Confirmation of the user's password.
        Returns:
            tuple: (bool, str) where bool indicates success or failure, and str contains a message.
        """
    
        return self.db_handler.create_account(fullname, email, password, confirm_password)
    
    def login(self, email, password):
        """
        Authenticates a user by verifying their email and password.
        Args:
            email (str): The user's email address.
            password (str): The user's password.
        Returns:
            tuple: (bool, str) where bool indicates success or failure, and str contains a message.
        """
        success, message = self.db_handler.login(email, password)
        if success:
            user = self.db_handler.auth.sign_in_with_email_and_password(email, password)
            return True, message, user
        return False, message, None
        
        #return self.db_handler.login(email, password)
    
    def reset_password(self):
        pass
    
    def log_out(self):
        pass
    
    def delete_account(self):
        pass