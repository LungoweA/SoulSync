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


if __name__ == "__main__":
    unittest.main()
