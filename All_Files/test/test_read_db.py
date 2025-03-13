import sys
import os
import unittest
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from All_Files.model.read_db import Read_db


class TestReadDb(unittest.TestCase):

    def setUp(self):
        self.uid = "fake_uid"
        self.id_token = "fake_token"
        self.db = Read_db(self.uid, self.id_token)
        self.db.write.database = MagicMock()

    def test_read_user_details(self):
        mock_data = {"Name": "John Doe", "Email": "john@example.com"}
        self.db.write.database.child.return_value.child.return_value.child.return_value.get.side_effect = [
            MagicMock(val=MagicMock(return_value=mock_data["Name"])),
            MagicMock(val=MagicMock(return_value=mock_data["Email"]))
        ]

        name, email = self.db.read_user_details()
        self.assertEqual(name, "John Doe")
        self.assertEqual(email, "john@example.com")

    def test_read_journal(self):
        mock_entries = [
            MagicMock(val=MagicMock(return_value={"Created_at": "2025-03-10 12:00", "Entry": "Feeling great!"})),
            MagicMock(val=MagicMock(return_value={"Created_at": "2025-03-11 14:30", "Entry": "Had a busy day."}))
        ]
        self.db.write.database.child.return_value.child.return_value.child.return_value.get.return_value.each.return_value = mock_entries

        result = self.db.read_journal()
        expected = {
            "2025-03-10": [("12:00", "Feeling great!")],
            "2025-03-11": [("14:30", "Had a busy day.")]
        }
        self.assertEqual(result, expected)

    def test_read_stress_level(self):
        mock_entries = [
            MagicMock(val=MagicMock(return_value={"Created_at": "2025-03-10 10:00", "Stress level": "High"})),
            MagicMock(val=MagicMock(return_value={"Created_at": "2025-03-11 11:00", "Stress level": "Medium"}))
        ]
        self.db.write.database.child.return_value.child.return_value.child.return_value.get.return_value.each.return_value = mock_entries

        result = self.db.read_stress_level()
        expected = {
            "2025-03-10": "High",
            "2025-03-11": "Medium"
        }
        self.assertEqual(result, expected)

    def test_read_mood_level(self):
        mock_entries = [
            MagicMock(val=MagicMock(return_value={
                "Created_at": "2025-03-10 09:00",
                "Mood description": "Happy",
                "Mood influenced by": "Good weather",
                "Mood rating": "8"
            })),
            MagicMock(val=MagicMock(return_value={
                "Created_at": "2025-03-11 13:00",
                "Mood description": "Tired",
                "Mood influenced by": "Work stress",
                "Mood rating": "5"
            }))
        ]
        self.db.write.database.child.return_value.child.return_value.child.return_value.get.return_value.each.return_value = mock_entries

        result = self.db.read_mood_level()
        expected = {
            "2025-03-10": ["Happy", "Good weather", "8"],
            "2025-03-11": ["Tired", "Work stress", "5"]
        }
        self.assertEqual(result, expected)

    def test_get_journal_dates(self):
        with patch.object(self.db, "read_journal", return_value={
            "2025-03-10": [("12:00", "Feeling great!")],
            "2025-03-11": [("14:30", "Had a busy day.")]
        }):
            result = self.db.get_journal_dates()
            expected = ["2025-03-10", "2025-03-11"]
            self.assertEqual(result, expected)

    def test_get_mood_dates(self):
        with patch.object(self.db, "read_mood_level", return_value={
            "2025-03-10": ["Happy", "Good weather", "8"],
            "2025-03-11": ["Tired", "Work stress", "5"]
        }):
            result = self.db.get_mood_dates()
            expected = ["2025-03-10", "2025-03-11"]
            self.assertEqual(result, expected)

    def test_get_stress_dates(self):
        with patch.object(self.db, "read_stress_level", return_value={
            "2025-03-10": "High",
            "2025-03-11": "Medium"
        }):
            result = self.db.get_stress_dates()
            expected = ["2025-03-10", "2025-03-11"]
            self.assertEqual(result, expected)

    def test_get_mood_stress_dates(self):
        with patch.object(self.db, "read_mood_level", return_value={"2025-03-10": ["Happy", "Good weather", "8"]}), \
             patch.object(self.db, "read_stress_level", return_value={"2025-03-11": "Medium"}):
            result = self.db.get_mood_stress_dates()
            expected = ["2025-03-10", "2025-03-11"]
            self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()
