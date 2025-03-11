import sys
import os
import unittest
from unittest.mock import MagicMock, patch
from datetime import datetime

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from All_Files.model.mood_db import Mood_db


class TestMoodDb(unittest.TestCase):

    def setUp(self):
        """Set up a mock instance of Write_db for each test."""
        with patch("model.write_db.Write_db") as mock_write_db:
            self.mock_write_db_instance = mock_write_db.return_value
            self.mood_db = Mood_db()
            self.mood_db.db = self.mock_write_db_instance

    def test_quotes(self):
        """Ensure quotes method returns the expected dictionary."""
        mock_quotes = {
            "Very Happy": [("Dalai Lama", "Happiness is not something ready-made.")],
            "Stressed": [("Wayne Dyer", "You cannot always control what goes on outside.")]
        }
        self.mood_db.quotes = MagicMock(return_value=mock_quotes)

        result = self.mood_db.quotes()

        self.assertEqual(result, mock_quotes)
        self.mood_db.quotes.assert_called_once()

    def test_mood_question(self):
        """Ensure mood_question method returns a list of questions."""
        expected_questions = ["How are you feeling today?", "What influenced your mood the most today?"]
        self.mood_db.mood_question = MagicMock(return_value=expected_questions)

        result = self.mood_db.mood_question()

        self.assertEqual(result, expected_questions)
        self.mood_db.mood_question.assert_called_once()

    def test_options(self):
        """Ensure options method returns a dictionary of options."""
        mock_options = {
            "0": ["Very Bad", "Bad", "Normal", "Good", "Very Good"],
            "1": ["Very Happy", "Neutral", "Stressed"]
        }
        self.mood_db.options = MagicMock(return_value=mock_options)

        result = self.mood_db.options()

        self.assertEqual(result, mock_options)
        self.mood_db.options.assert_called_once()

    def test_tips(self):
        """Ensure tips method returns a dictionary of tips based on influences."""
        mock_tips = {"School": ["Prioritize tasks", "Avoid procrastination"], "Work": ["Take Short Breaks"]}
        self.mood_db.tips = MagicMock(return_value=mock_tips)

        result = self.mood_db.tips()

        self.assertEqual(result, mock_tips)
        self.mood_db.tips.assert_called_once()

    def test_supportive_messages(self):
        """Ensure supportive_messages method returns a dictionary of messages."""
        mock_messages = {"Very Happy": "Enjoy your day!", "Stressed": "Take deep breaths and relax."}
        self.mood_db.supportive_messages = MagicMock(return_value=mock_messages)

        result = self.mood_db.supportive_messages()

        self.assertEqual(result, mock_messages)
        self.mood_db.supportive_messages.assert_called_once()

    def test_mood_score(self):
        """Ensure mood_score method correctly updates the user data dictionary."""
        self.mood_db.mood_score("5", "Happy", "Weather")

        self.assertEqual(self.mood_db.user_data["Mood rating"], "5")
        self.assertEqual(self.mood_db.user_data["Mood description"], "Happy")
        self.assertEqual(self.mood_db.user_data["Mood influenced by"], "Weather")

    def test_save_data(self):
        """Test both successful and failure cases of save_data method."""
        success_message = "Your results have been saved"
        error_message = "Error: Some fields are missing!"

        self.mock_write_db_instance.auth.get_account_info.return_value = {"users": [{"localId": "123"}]}
        self.mock_write_db_instance.database.child().child().child().push.return_value = None
        self.mood_db.user_data = {
            "Mood rating": "5",
            "Mood description": "Happy",
            "Mood influenced by": "Weather",
            "Created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        result = self.mood_db.save_data("fake_token")
        self.assertEqual(result, success_message)

        self.mood_db.user_data["Mood rating"] = None
        result = self.mood_db.save_data("fake_token")
        self.assertEqual(result, error_message)


if __name__ == '__main__':
    unittest.main()
