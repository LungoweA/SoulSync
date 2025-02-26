import sys
import os
import pyrebase
import json
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
        config = {
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
        self.firebase = pyrebase.initialize_app(config)
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
                    'Password': password,
                    'Created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
                            
            self.database.child('Users').child(user_id).set(user_data, id_token)
                            
            return True, 'Account Created'
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

