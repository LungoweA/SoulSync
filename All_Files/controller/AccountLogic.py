import sys
import os
from model.write_db import Write_db
import firebase_admin
from firebase_admin import auth, credentials, db
import json
import requests
from dotenv import load_dotenv


load_dotenv()

firebase_config = json.loads(os.getenv("FIREBASE_CONFIG", "{}"))

if not firebase_config:
    raise ValueError("❌ Firebase configuration is missing!")

FIREBASE_WEB_API_KEY = firebase_config.get("apiKey")
DATABASE_URL = firebase_config.get("databaseURL")

if not firebase_admin._apps:
    cred = credentials.Certificate(firebase_config)
    firebase_admin.initialize_app(cred, {"databaseURL": DATABASE_URL})

db = db.reference()

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

    def change_password(self, id_token, old_password, new_password):
        """
        Changes the user's password in Firebase Authentication after verifying the old password.
        Args:
            id_token (str): The Firebase authentication token of the user.
            old_password (str): The user's current password.
            new_password (str): The new password the user wants to set.
        Returns:
            tuple: (bool, str) where bool indicates success, and str contains a message.
        """
        try:
            # Verify the user's ID token
            user = auth.verify_id_token(id_token)
            uid = user["uid"]
            user_email = user["email"]  # Get user's email from token

            # Verify old password using Firebase Authentication REST API
            url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_WEB_API_KEY}"

            payload = {
                "email": user_email,
                "password": old_password,
                "returnSecureToken": True,
            }

            response = requests.post(url, json=payload)
            data = response.json()

            # If Firebase returns an error, the password is incorrect
            if "error" in data:
                error_message = data["error"]["message"]
                
                # **Debugging print statement**
                print(f"Firebase Error: {error_message}")

                # **Fix: Change generic "Credentials are incorrect" to a specific message**
                if error_message in ["INVALID_PASSWORD", "INVALID_LOGIN_CREDENTIALS"]:
                    return False, "❌ Current password is incorrect!"
                elif error_message == "EMAIL_NOT_FOUND":
                    return False, "❌ No user found with this email!"
                elif error_message == "USER_DISABLED":
                    return False, "❌ This account has been disabled!"
                else:
                    return False, f"❌ {error_message}"


            # **New Fix: Prevent changing to the same password AFTER verifying the old one**
            if old_password == new_password:
                return False, "❌ New password cannot be the same as the current password!"

            # Check password length
            if len(new_password) < 6:
                return False, "❌ Password must be at least 6 characters long!"

            # Check password strength (Uppercase, Lowercase, Number, Special Char)
            has_upper = any(char.isupper() for char in new_password)
            has_lower = any(char.islower() for char in new_password)
            has_digit = any(char.isdigit() for char in new_password)
            has_special = any(not char.isalnum() for char in new_password)

            if not (has_upper and has_lower and has_digit and has_special):
                return False, "❌ Password does not meet all the requirements!"

            # If old password is correct and new password is valid, update the password
            auth.update_user(uid, password=new_password)

            print("✅ Password changed successfully in Firebase!")
            return True, "✅ Password changed successfully!"
        except Exception as e:
            print(f"❌ Error changing password: {e}")
            return False, str(e)

    def check_password_strength(self, password):
        """
        Checks the strength of a given password based on the following criteria:
        - At least 7 characters long
        - Contains at least one uppercase letter
        - Contains at least one lowercase letter
        - Contains at least one digit
        - Contains at least one special character
        Args:
            password (str): The password to check.
        Returns:
            dict: A dictionary containing which strength criteria are met.
        """
        return {
            "char_length": len(password) >= 7,
            "uppercase": any(char.isupper() for char in password),
            "lowercase": any(char.islower() for char in password),
            "digit": any(char.isdigit() for char in password),
            "special_char": any(not char.isalnum() for char in password)
        }

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
            print("User logged out successfully")
            return True
        except Exception as e:
            print("error logging out:", e)
            return False

    def delete_account(self, id_token):
        """Deletes the user account from Firebase Authentication and Database."""
        try:
            user = auth.verify_id_token(id_token)
            uid = user["uid"]

            # ✅ Step 1: Ensure we're checking the correct path
            user_data_path = f"Users/{uid}"  # ✅ Match Firebase structure
            user_data = db.child(user_data_path).get()

            if isinstance(user_data, dict):  # ✅ Handle dictionary response
                print(f"✅ Found user data in Database: {user_data}")
                db.child(user_data_path).delete()  # ✅ Delete using correct method
                print(f"✅ Deleted user data from Firebase Database for UID: {uid}")
            else:
                print("⚠️ No user data found in Database! Skipping database deletion.")

            # ✅ Step 2: Ensure user exists before deleting from Authentication
            try:
                auth.get_user(uid)  # Will raise an error if user does not exist
            except firebase_admin.auth.UserNotFoundError:
                return False, "❌ User not found in Firebase Authentication!"

            # ✅ Step 3: Delete the user from Firebase Authentication
            auth.delete_user(uid)
            print(f"✅ Deleted user from Firebase Authentication: {uid}")

            return True, "✅ Account deleted successfully!"
        except firebase_admin.auth.UserNotFoundError:
            return False, "❌ User does not exist or has already been deleted!"
        except Exception as e:
            print(f"❌ Error deleting account: {e}")
            return False, f"❌ Error deleting account: {str(e)}"
