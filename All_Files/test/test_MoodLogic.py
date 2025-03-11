import sys
import os
import unittest
from unittest.mock import MagicMock, patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from All_Files.controller.MoodLogic import Mood


class TestMood(unittest.TestCase):

    def setUp(self):
        """Set up a mock instance of Mood_db for each test."""
        with patch("model.mood_db.Mood_db") as mock_mood_db:
            self.mock_mood_db_instance = mock_mood_db.return_value
            self.mood = Mood()
            self.mood.mood_db = self.mock_mood_db_instance

    def test_quotes(self):
        mock_quotes = {"Very Happy": [("Mock Author 1", "Mock Quote 1"), ("Mock Author 2", "Mock Quote 2")]}
        self.mock_mood_db_instance.quotes.return_value = mock_quotes

        result = self.mood.quotes()

        self.assertEqual(result, mock_quotes)
        self.mock_mood_db_instance.quotes.assert_called_once()

    def test_tips(self):
        mock_tips = {"School": ["Mock Tip 1", "Mock Tip 2"], "Work": ["Mock Tip 3", "Mock Tip 4"]}
        self.mock_mood_db_instance.tips.return_value = mock_tips

        result = self.mood.tips()

        self.assertEqual(result, mock_tips)
        self.mock_mood_db_instance.tips.assert_called_once()

    def test_score(self):
        """Ensure mood_score is correctly passed to the database method."""
        self.mood.mood_score("5", "Happy", "Weather")
        self.mock_mood_db_instance.mood_score.assert_called_once_with("5", "Happy", "Weather")

    def test_question(self):
        mock_question = ["Mock Question 1?", "Mock Question 2?", "Mock Question 3?"]
        self.mock_mood_db_instance.mood_question.return_value = mock_question

        result = self.mood.mood_question()

        self.assertEqual(result, mock_question)
        self.mock_mood_db_instance.mood_question.assert_called_once()

    def test_options(self):
        mock_options = {
            "0": ["Mock Option 1", "Mock Option 2", "Mock Option 3", "Mock Option 4", "Mock Option 5"],
            "1": ["Mock Option 6", "Mock Option 7", "Mock Option 8", "Mock Option 9", "Mock Option 10"],
        }
        self.mock_mood_db_instance.options.return_value = mock_options

        result = self.mood.options()

        self.assertEqual(result, mock_options)
        self.mock_mood_db_instance.options.assert_called_once()

    def test_messages(self):
        mock_messages = {"Very Happy": ["Mock Message 1"], "Neutral": ["Mock Message 2"]}
        self.mock_mood_db_instance.supportive_messages.return_value = mock_messages

        result = self.mood.supportive_messages()

        self.assertEqual(result, mock_messages)
        self.mock_mood_db_instance.supportive_messages.assert_called_once()

    def test_save_data(self):
        """Test both success and failure cases of save_data."""
        cases = [
            ("fake_token", "Your results have been saved"),
            ("fake_token", "Error: Some fields are missing!")
        ]

        for token, expected_result in cases:
            self.mock_mood_db_instance.save_data.return_value = expected_result
            result = self.mood.save_data(token)

            self.assertEqual(result, expected_result)
            self.mock_mood_db_instance.save_data.assert_called_once_with(token)
            self.mock_mood_db_instance.save_data.reset_mock()


if __name__ == '__main__':
    unittest.main()
