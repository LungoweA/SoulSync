import sys
import os
from model.write_db import Write_db
from model.read_db import Read_db


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

    def change_password(self, uid, id_token, new_password, confirm_password):
        """
        Changes the password for the user with the given UID.

        This method validates the new password and confirm password inputs, then calls the 
        `change_password` method from the database handler to perform the password update.

        Args:
            uid (str): The unique user ID.
            id_token (str): The authentication token for the user.
            new_password (str): The new password to be set.
            confirm_password (str): The confirmation of the new password.

        Returns:
            tuple: A tuple containing:
                - A boolean indicating whether the password change was successful (True if successful, False if not).
                - A message providing feedback about the password change process. The message can be a success or error message.
        """
        
        return self.db_handler.change_password(uid, id_token, new_password, confirm_password)
    
    
    def log_out(self):
        """
        Logs out the current user by clearing the user's authentication token.

        This method calls the `log_out` method from the database handler to perform the logout operation.

        Returns:
            bool: `True` if the logout was successful, `False` if there was an error.
        """
        
        return self.db_handler.log_out()
    
    
    def delete_account(self, uid, id_token):
        """
        Deletes the user's account permanently from the database.

        This method calls the `delete_account` method from the database handler to delete the user's
        data from the database and remove the user from the authentication system.

        Args:
            uid (str): The unique user ID of the account to be deleted.
            id_token (str): The authentication token for the user to authorize the account deletion.

        Returns:
            tuple: A tuple containing:
                - A boolean indicating whether the account deletion was successful (True if successful, False if not).
                - A message providing feedback about the account deletion process. The message can be a success or error message.
        """
    
        return self.db_handler.delete_account(uid, id_token)
    
    
    
    
class AccountDetails:
    """
    This class provides access to user details, journal entries, mood levels, and stress levels 
    from the database, encapsulating the methods from the Read_db class.

    Attributes:
        uid (str): The unique user ID for the account.
        id_token (str): The authentication token for the user.
        read_db (Read_db): An instance of the Read_db class used to fetch data from the database.

    Methods:
        read_user_details():
            Fetches the user's basic details (name, password, and email) from the database.
        
        read_journal():
            Retrieves the user's journal entries from the database.
        
        read_stress_level():
            Retrieves the user's stress level history from the database.
        
        read_mood_level():
            Retrieves the user's mood level history from the database.
        
        get_mood_stress_dates():
            Retrieves all unique dates from the user's mood and stress history, sorted.
        
        get_journal_dates():
            Retrieves all dates from the user's journal entries, sorted.
    """
    
    def __init__(self, uid, id_token):
        """
        Initializes the AccountDetails class with the user ID and authentication token.

        Args:
            uid (str): The unique user ID.
            id_token (str): The authentication token for the user.
        """
        
        self.uid = uid
        self.id_token = id_token
        self.read_db = Read_db(self.uid, self.id_token)
        
        
    def read_user_details(self):
        """
        Fetches the user's details (name, password, and email) from the database.

        Returns:
            tuple: A tuple containing the user's name, password, and email.
        """
        
        return self.read_db.read_user_details()
        
        
    def read_journal(self):
        """
        Retrieves the user's journal entries from the database.

        Returns:
            dict: A dictionary containing journal entries with date as the key.
                If no entries are found, returns a message indicating no journal entries are available.
        """
        
        return self.read_db.read_journal()
        
        
    def read_stress_level(self):
        """
        Retrieves the user's stress level history from the database.

        Returns:
            dict: A dictionary containing stress levels with date as the key.
                If no entries are found, returns an error message.
        """
        
        return self.read_db.read_stress_level()
            
    def read_mood_level(self):
        """
        Retrieves the user's mood level history from the database.

        Returns:
            dict: A dictionary containing mood levels with date as the key.
                If no entries are found, returns an error message.
        """
        
        return self.read_db.read_mood_level()
    
    def get_mood_stress_dates(self):
        """
        Retrieves all unique dates from the user's mood and stress history, sorted.

        Returns:
            list: A sorted list of dates that appear in both the user's mood and stress history.
        """
        
        return self.read_db.get_mood_stress_dates()
    
    
    def get_journal_dates(self):
        """
        Retrieves all dates from the user's journal entries, sorted.

        Returns:
            list: A sorted list of dates from the user's journal entries.
        """
        
        return self.read_db.get_journal_dates()

