import sys
import os
import pyrebase
import requests
from datetime import datetime

# Add the parent directory to the system path to allow module imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


class Write_db:
    """
    A class to handle Firebase authentication and database interactions, including user account creation,
    login, and password validation.
    """

    def __init__(self):
        """
        Initializes the Firebase application with the provided configuration.
        Sets up authentication and database references.
        """

        # Firebase configuration
        self.config = {
                    "apiKey": "AIzaSyDfRV2B-BNHDGxNC5aRNWH2441NkPE5xZs",
                    "authDomain": "soul-sync-a4b50.firebaseapp.com",
                    "databaseURL": "https://soul-sync-a4b50-default-rtdb.firebaseio.com",
                    "projectId": "soul-sync-a4b50",
                    "storageBucket": "soul-sync-a4b50.firebasestorage.app",
                    "messagingSenderId": "365391145029",
                    "appId": "1:365391145029:web:d5b3e7bfbc4e74a7b55b2c",
                    "measurementId": "G-N3ZX4ZTR50"
                }

        # Intializing firebase
        self.firebase = pyrebase.initialize_app(self.config)
        self.auth = self.firebase.auth()

        self.database = self.firebase.database()

    def create_account(self, name, email, password, confirm_password):
        """
        Creates a new user account and stores user details in the Firebase Realtime Database.
        Args:
            name (str): Full name of the user.
            email (str): User's email address.
            password (str): User's password.
            confirm_password (str): Confirmation of the user's password.
        Returns:
            tuple: (bool, str) - True with success message if account is created,
            False with error message otherwise.
        """

        if not self.validate_password(password):
            return False, "Invalid Password!"

        if password != confirm_password:
            return False, "Passwords don't match, please try again!"

        if self.validate_email(email):
            return False, "Email is not allowed!"

        try:
            user = self.auth.create_user_with_email_and_password(email, password)
            user_id = user['localId']
            id_token = user['idToken']
            user_data = {
                    'Name': name,
                    'Email': email,
                    'Created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

            self.database.child('Users').child(user_id).set(user_data, id_token)

            return True, 'Your account has been created.'
        except:
            return False, 'Account already exists!'

    def validate_password(self, password):
        """
        Validates the strength of the password based on the following criteria:
        - At least 7 characters long
        - Contains at least one uppercase letter
        - Contains at least one digit
        - Contains at least one lowercase letter
        - Contains at least one special character
        Args:
            password (str): The password to validate.
        Returns:
            bool: True if password meets all criteria, False otherwise.
        """

        correct_length = False
        is_upper = False
        is_digit = False
        is_lower = False
        is_not_alphanum = False

        if len(password) >= 7:
            correct_length = True
            for char in password:
                if char.isupper():
                    is_upper = True
                if char.isdigit():
                    is_digit = True
                if char.islower():
                    is_lower = True
                if (not char.isalnum()):
                    is_not_alphanum = True

        return correct_length and is_upper and is_digit and is_lower and is_not_alphanum

    def validate_email(self, email):
        """
        Validates an email address by checking if it contains any forbidden characters.

        Args:
            email (str): The email address to be validated.

        Returns:
            bool: Returns True if the email contains any forbidden characters, False otherwise.

        The forbidden characters are: ':', ';', '"', '<', '>', and '/'.
        """

        forbidden_characters = [':', ';', '"', '<', '>', '/']
        for char in email:
            if char in forbidden_characters:
                return True

    def login(self, email, password):
        """
        Logs in a user by verifying credentials with Firebase Authentication.
        Args:
            email (str): The user's email address.
            password (str): The user's password.
        Returns:
            tuple: (bool, str) - True if login is successful, False with error message otherwise.
        """

        try:
            user = self.auth.sign_in_with_email_and_password(email, password)

            return True, '', user
        except:
            return False, 'Invalid email or Incorrect password!', None

    def log_out(self):
        """
        Logs out the current user by setting the `current_user` attribute to `None`.

        Returns:
            bool: Returns `True` if the logout process is successful, otherwise returns `False`.

        This function attempts to log out the user by clearing the `current_user` attribute
        of the authentication system. If successful, it returns `True`. If an error occurs
        during the logout process, it catches the exception and returns `False`.
        """

        try:
            self.auth.current_user = None
            return True
        except Exception as e:
            return False

    def change_password(self, uid, id_token, new_password, confirm_password):
        """
        Changes the password for a user, ensuring validation and consistency between the new password and confirmation password.

        Args:
            uid (str): The unique user ID of the user whose password is being changed.
            id_token (str): The Firebase ID token to authenticate the request.
            new_password (str): The new password entered by the user.
            confirm_password (str): The password confirmation entered by the user.

        Returns:
            tuple: A tuple containing a boolean and a message:
                - bool: `True` if the password change was successful, `False` otherwise.
                - str: A message indicating the result of the password change attempt (e.g., success or error message).

        Raises:
            Exception: If there is an error during the password change request.
        """

        if new_password == "" or confirm_password == "":
            return False, "All fields must be filled!"

        if new_password != confirm_password:
            return False, "Passwords don't match, please try again!"

        if not self.validate_password(new_password):
                return False, 'Invalid Password!'

        try:

            url = f"https://identitytoolkit.googleapis.com/v1/accounts:update?key={self.config['apiKey']}"
            payload = {
                "idToken": id_token,
                "password": new_password,
                "returnSecureToken": True
            }

            requests.post(url, json=payload)
            self.database.child('Users').child(uid).update({'Password': new_password}, id_token)
            return True, 'Password Changed Successfully'
        except Exception:
            return False, 'Unknown Error Occurred'

    def delete_account(self, uid, id_token):
        """
        Deletes a user account from the database and Firebase Authentication system.

        Args:
            uid (str): The unique user ID of the account to be deleted.
            id_token (str): The Firebase ID token used to authenticate the request.

        Returns:
            tuple: A tuple containing a boolean and a message:
                - bool: `True` if the account deletion was successful, `False` otherwise.
                - str: A message indicating the result of the account deletion attempt (e.g., success or error message).

        Raises:
            Exception: If there is an error while attempting to delete the account.
        """

        try:
            self.database.child('Users').child(uid).remove(id_token)
            self.auth.delete_user_account(id_token)
            return True, 'Your account has been permanently deleted.'
        except Exception as e:
            return False, 'Unknown error occured!'
