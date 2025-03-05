import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from model.Journal_db import Journal_db

class Diary:
    """
    A class to manage journal or diary-related operations, such as saving journal entries.
    It acts as an interface to interact with the `Journal_db` class.

    Attributes:
        journal_db (Journal_db): An instance of the `Journal_db` class to interact with the journal-related database.
    """

    def __init__(self):
        """
        Initializes the Diary class by creating an instance of the `Journal_db` class.
        """

        self.Journal_db = Journal_db()
        
    def save(self, id_token, journal):
        """
        Saves the user's journal entry to the database.

        Args:
            id_token (str): The ID token associated with the user's session.
            journal (str): The journal entry to be saved.

        Returns:
            bool: True if the journal entry was successfully saved, False otherwise.
        """

        return self.Journal_db.save(id_token, journal)

    def fetch_journal_history(self, id_token):
        """
        Fetches the user's journal history using the Journal_db class.

        Args:
            id_token (str): The Firebase authentication token of the user.

        Returns:
            list: A list of dictionaries containing journal entries.
        """
        return self.Journal_db.fetch_journal_history(id_token)
