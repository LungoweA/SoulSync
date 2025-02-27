import sys
import os
from model.write_db import Write_db
import firebase_admin
from firebase_admin import auth, credentials


SERVICE_ACCOUNT_PATH = os.path.abspath(os.path.join("model", r"User db", "firebase_config.json"))

# Initialize Firebase if it's not already initialized
if not firebase_admin._apps:
    cred = credentials.Certificate(SERVICE_ACCOUNT_PATH)
    firebase_admin.initialize_app(cred)

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

        return self.db_handler.login(email, password)

    def reset_password(self):
        pass

    def log_out(self, id_token):
        """
        Logs out the user by revoking their session.
        Args:
            id_token (str): The Firebase authentication token of the user.
        Returns:
            bool: True if logout is successful, False otherwise.
        """
        try:
            decoded_token = auth.verify_id_token(id_token)
            uid = decoded_token["uid"]
            auth.revoke_refresh_tokens(uid)
            print("User logged out sucessfully")
            return True
        except Exception as e:
            print("error logging out:", e)
            return False

    def delete_account(self):
        pass
