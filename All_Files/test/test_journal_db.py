import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from All_Files.model.Journal_db import Journal_db



import unittest
from unittest.mock import MagicMock, patch
from datetime import datetime


class TestJournalDb(unittest.TestCase):

    def setUp(self):
        """Set up a test instance of Journal_db with mocked database and authentication."""
        self.journal_db = Journal_db()
        self.mock_auth = MagicMock()
        self.mock_database = MagicMock()

        self.journal_db.db.auth = self.mock_auth
        self.journal_db.db.database = self.mock_database

    def test_save(self):
        """Test saving a journal entry to the database."""
        id_token = "fake_token"
        journal_entry = "This is a test journal entry."

        # Mock Firebase authentication response
        self.mock_auth.get_account_info.return_value = {"users": [{"localId": "123"}]}

        # Call the save method
        self.journal_db.save(id_token, journal_entry)

        # Assert the correct database call is made
        self.mock_database.child().child().child().push.assert_called_once_with(
            {
                "Entry": journal_entry,
                "Created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            },
            id_token
        )

    def test_fetch_journal_history(self):
        """Test fetching the journal history from the database."""
        id_token = "fake_token"

        # Mock Firebase authentication response
        self.mock_auth.get_account_info.return_value = {"users": [{"localId": "123"}]}

        # Mock journal data stored in Firebase
        mock_journal_data = {
            "1": {"Entry": "First journal entry", "Created_at": "2025-03-01 10:00:00"},
            "2": {"Entry": "Second journal entry", "Created_at": "2025-03-02 14:00:00"},
        }
        self.mock_database.child().child().child().get.return_value.val.return_value = mock_journal_data

        # Call the fetch_journal_history method
        history = self.journal_db.fetch_journal_history(id_token)

        # Assert the returned list is sorted by Created_at in descending order
        self.assertEqual(len(history), 2)
        self.assertEqual(history[0]["Entry"], "Second journal entry")
        self.assertEqual(history[1]["Entry"], "First journal entry")

if __name__ == "__main__":
    unittest.main()
