import sys
import os
import unittest
from unittest.mock import MagicMock, patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from All_Files.controller.JournalLogic import Diary


class TestJournal(unittest.TestCase):

    def setUp(self):
        """Set up a mock instance of Journal_db for each test."""
        with patch("model.Journal_db.Journal_db") as mock_journal_db:
            self.mock_journal_db_instance = mock_journal_db.return_value
            self.mood = Diary()
            self.mood.Journal_db = self.mock_journal_db_instance

    def test_save_entry(self):
        """Test both success and failure cases of save method."""
        cases = [
            ("fake_token", "This is my journal entry", True, True),
            ("fake_token", "This is another entry", False, False),
        ]

        for token, entry, mock_return, expected_result in cases:
            self.mock_journal_db_instance.save.return_value = mock_return
            result = self.mood.save(token, entry)

            self.mock_journal_db_instance.save.assert_called_once_with(token, entry)
            self.assertEqual(result, expected_result)
            self.mock_journal_db_instance.save.reset_mock()

    def test_save_exception(self):
        """Ensure exception is raised when save fails due to a database error."""
        self.mock_journal_db_instance.save.side_effect = Exception("Database error")

        with self.assertRaises(Exception) as context:
            self.mood.save("fake_token", "Entry causing error")

        self.assertEqual(str(context.exception), "Database error")
        self.mock_journal_db_instance.save.assert_called_once_with("fake_token", "Entry causing error")


if __name__ == '__main__':
    unittest.main()
