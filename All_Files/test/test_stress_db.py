import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import unittest
from unittest.mock import patch, MagicMock
from All_Files.model.stress_db import Stress_db


class TestStressDb(unittest.TestCase):

    def setUp(self):
        self.stress_db = Stress_db()
        self.mock_auth = MagicMock()
        self.mock_database = MagicMock()
        self.stress_db.db.auth = self.mock_auth
        self.stress_db.db.database = self.mock_database

    def test_stress_test(self):
        questions = self.stress_db.stress_test()
        self.assertIsInstance(questions, list)
        self.assertGreater(len(questions), 0)

    def test_result(self):
        self.assertEqual(self.stress_db.result(22), "Low")
        self.assertEqual(self.stress_db.result(15), "Moderate")
        self.assertEqual(self.stress_db.result(5), "High")

    def test_exercises(self):
        exercises = self.stress_db.exercises()
        self.assertIsInstance(exercises, dict)
        self.assertIn("Low", exercises)
        self.assertIn("Moderate", exercises)
        self.assertIn("High", exercises)

    def test_tips(self):
        tips = self.stress_db.tips()
        self.assertIsInstance(tips, dict)
        self.assertIn("Low", tips)

    def test_quotes(self):
        quotes = self.stress_db.quotes()
        self.assertIsInstance(quotes, dict)
        self.assertIn("Low", quotes)

    @patch("model.stress_db.datetime")
    def test_save_data(self, mock_datetime):
        mock_datetime.now.return_value.strftime.return_value = "2025-03-04 12:00:00"

        self.mock_auth.get_account_info.return_value = {"users": [{"localId": "123"}]}
        id_token = "fake_token"
        result = "Moderate"

        self.stress_db.save_data(id_token, result)
        self.mock_database.child().child().child().push.assert_called_once()


if __name__ == "__main__":
    unittest.main()
