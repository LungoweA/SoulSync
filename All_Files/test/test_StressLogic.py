import sys
import os
import unittest
from unittest.mock import MagicMock, patch
from datetime import datetime

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from All_Files.controller.StressLogic import Stress


class TestStress(unittest.TestCase):

    def setUp(self):
        """Set up a mock instance of Stress_db for each test."""
        with patch("model.stress_db.Stress_db") as mock_stress_db:
            self.mock_stress_db_instance = mock_stress_db.return_value
            self.stress = Stress()
            self.stress.stress_db = self.mock_stress_db_instance

    def test_stress_test(self):
        """Ensure stress_test method returns the expected questions."""
        mock_questions = ["Question 1", "Question 2", "Question 3"]
        self.mock_stress_db_instance.stress_test.return_value = mock_questions

        result = self.stress.stress_test()

        self.assertEqual(result, mock_questions)
        self.mock_stress_db_instance.stress_test.assert_called_once()

    def test_result(self):
        """Ensure result method correctly determines stress level."""
        cases = [
            (22, "Low"),
            (15, "Moderate"),
            (5, "High"),
        ]

        for sum_value, expected in cases:
            self.mock_stress_db_instance.result.return_value = expected
            result = self.stress.result(sum_value)
            self.assertEqual(result, expected)
            self.mock_stress_db_instance.result.assert_called_with(sum_value)

    def test_tips(self):
        """Ensure tips method returns a dictionary of stress tips."""
        mock_tips = {"Low": ["Tip 1", "Tip 2"], "High": ["Tip 3"]}
        self.mock_stress_db_instance.tips.return_value = mock_tips

        result = self.stress.tips()

        self.assertEqual(result, mock_tips)
        self.mock_stress_db_instance.tips.assert_called_once()

    def test_exercises(self):
        """Ensure exercises method returns a dictionary of stress exercises."""
        mock_exercises = {"Low": ["Exercise 1", "Exercise 2"], "Moderate": ["Exercise 3"]}
        self.mock_stress_db_instance.exercises.return_value = mock_exercises

        result = self.stress.exercises()

        self.assertEqual(result, mock_exercises)
        self.mock_stress_db_instance.exercises.assert_called_once()

    def test_quotes(self):
        """Ensure quotes method returns a dictionary of motivational quotes."""
        mock_quotes = {"Low": [("Author 1", "Quote 1")], "High": [("Author 2", "Quote 2")]}
        self.mock_stress_db_instance.quotes.return_value = mock_quotes

        result = self.stress.quotes()

        self.assertEqual(result, mock_quotes)
        self.mock_stress_db_instance.quotes.assert_called_once()

    def test_save_data(self):
        """Test both successful and unsuccessful save operations."""
        success_message = "Your results have been saved"
        error_message = "Error: Failed to save data"

        self.mock_stress_db_instance.save_data.return_value = success_message
        result = self.stress.save_data("fake_token", "Moderate")
        self.assertEqual(result, success_message)
        self.mock_stress_db_instance.save_data.assert_called_once_with("fake_token", "Moderate")

        self.mock_stress_db_instance.save_data.reset_mock()
        self.mock_stress_db_instance.save_data.return_value = error_message
        result = self.stress.save_data("fake_token", "High")
        self.assertEqual(result, error_message)
        self.mock_stress_db_instance.save_data.assert_called_once_with("fake_token", "High")

    def test_fetch_stress_history(self):
        """Test fetching stress history with normal, empty, and failure cases."""
        fake_id_token = "fake_token"
        expected_result = [
            {"Created_at": "2025-03-07 12:00:00", "Stress Level": "High"},
            {"Created_at": "2025-03-06 18:30:00", "Stress Level": "Low"},
        ]

        self.mock_stress_db_instance.fetch_stress_history.return_value = expected_result
        result = self.stress.fetch_stress_history(fake_id_token)
        self.assertEqual(result, expected_result)
        self.mock_stress_db_instance.fetch_stress_history.assert_called_once_with(fake_id_token)

        self.mock_stress_db_instance.fetch_stress_history.reset_mock()
        self.mock_stress_db_instance.fetch_stress_history.return_value = []
        result = self.stress.fetch_stress_history(fake_id_token)
        self.assertEqual(result, [])
        self.mock_stress_db_instance.fetch_stress_history.assert_called_once_with(fake_id_token)

        self.mock_stress_db_instance.fetch_stress_history.reset_mock()
        self.mock_stress_db_instance.fetch_stress_history.side_effect = Exception("Database error")

        with self.assertRaises(Exception) as context:
            self.stress.fetch_stress_history(fake_id_token)

        self.assertEqual(str(context.exception), "Database error")
        self.mock_stress_db_instance.fetch_stress_history.assert_called_once_with(fake_id_token)


if __name__ == '__main__':
    unittest.main()
