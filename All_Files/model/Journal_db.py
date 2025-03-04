from model.write_db import Write_db
from datetime import datetime

class Journal_db:
    """
    A class to manage journal-related operations, such as saving journal entries to a database.
    It acts as an interface to interact with the `Write_db` class.

    Attributes:
        db (Write_db): An instance of the `Write_db` class to interact with the database.
    """

    def __init__(self):
        """
        Initializes the Journal_db class by creating an instance of the `Write_db` class.
        """

        self.db = Write_db()
        
        
    def save(self, id_token, journal):
        """
        Saves the user's journal entry to the database.

        Args:
            id_token (str): The ID token associated with the user's session.
            journal (str): The journal entry to be saved.

        Returns:
            Exception: If an error occurs during the save operation, the exception is returned.
        """

        # Saving data to Firebase
        user_id = self.db.auth.get_account_info(id_token)['users'][0]['localId']
        journal_data = {"Entry": journal,
                        "Created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        try:
            self.db.database.child("Users").child(user_id).child("Journal").push(journal_data, id_token)
        except Exception as err:
            return err
        
        
        
    def fetch_journal_history(self, id_token):
        """
        Fetches the user's journal history from Firebase.

        Args:
            id_token (str): The Firebase authentication token of the user.

        Returns:
            list: A list of dictionaries containing journal entries.
        """

        try:
            user_id = self.db.auth.get_account_info(id_token)['users'][0]['localId']
            journal_data = self.db.database.child("Users").child(user_id).child("Journal").get(id_token).val()

            print(f"Journal data retrieved: {journal_data}")  # Debugging output
            if journal_data:
                return sorted(
                    [
                        {"Created_at": entry["Created_at"], "Entry": entry["Entry"]}
                        for entry in journal_data.values()
                    ],
                    key=lambda x: x["Created_at"],
                    reverse=True
                )
            else:
                return []  # Return an empty list if no data is found
        except Exception as e:
            print(f"Error fetching journal history: {e}")
            return 