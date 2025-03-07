import sys
import os
import unittest
from unittest.mock import MagicMock, patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from All_Files.controller.JournalLogic import Diary


class TestJournal(unittest.TestCase):

    @patch("model.Journal_db.Journal_db")
    def setUp(self, mock_journal_db):

        self.mock_journal_db_instance = mock_journal_db.return_value

        self.mood = Diary()
        self.mood.Journal_db = self.mock_journal_db_instance

    def test_save_success(self):
        self.mock_journal_db_instance.save.return_value = True

        result = self.mood.save("fake_token", "This is my journal entry")

        self.mock_journal_db_instance.save.assert_called_once_with("fake_token", "This is my journal entry")
        self.assertTrue(result)

    def test_save_failure(self):

        self.mock_journal_db_instance.save.return_value = False

        result = self.mood.save("fake_token", "This is another entry")

        self.mock_journal_db_instance.save.assert_called_once_with("fake_token", "This is another entry")

        self.assertFalse(result)

    def test_save_exception(self):

        self.mock_journal_db_instance.save.side_effect = Exception("Database error")

        with self.assertRaises(Exception):
            self.mood.save("fake_token", "Entry causing error")

        self.mock_journal_db_instance.save.assert_called_once_with("fake_token", "Entry causing error")

    def test_fetch_journal_success(self):
        mock_entries = [
            {"Created_at": "2025-03-06 10:00:00", "Entry": "First journal entry"},
            {"Created_at": "2025-03-07 12:00:00", "Entry": "Second journal entry"}
        ]

        self.mock_journal_db_instance.fetch_journal_history.return_value = mock_entries

        result = self.mood.fetch_journal_history("fake_token")

        self.mock_journal_db_instance.fetch_journal_history.assert_called_once_with("fake_token")
        self.assertEqual(result, mock_entries)

    def test_fetch_journal_empty(self):
        self.mock_journal_db_instance.fetch_journal_history.return_value = []

        result = self.mood.fetch_journal_history("fake_token")

        self.mock_journal_db_instance.fetch_journal_history.assert_called_once_with("fake_token")
        self.assertEqual(result, [])

    def test_fetch_journal_exception(self):
        self.mock_journal_db_instance.fetch_journal_history.side_effect = Exception("Database error")

        with self.assertRaises(Exception):
            self.mood.fetch_journal_history("fake_token")

        self.mock_journal_db_instance.fetch_journal_history.assert_called_once_with("fake_token")

        
if __name__ == '__main__':
    unittest.main()
