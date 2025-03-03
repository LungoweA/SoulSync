import sys
import os

# Add the parent directory to the system path to allow module imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from model.mood_db import Mood_db

class Mood:
    """
    A class to interact with the Mood database and provide mood-related functionalities.

    This class acts as an interface to the `Mood_db` class, allowing the user to retrieve
    quotes, tips, mood scores, mood questions, options, supportive messages, and to save data.

    Attributes:
        mood_db (Mood_db): An instance of the `Mood_db` class to interact with the database.
    """

    def __init__(self):
        """
        Initializes the Mood class by creating an instance of the `Mood_db` class.
        """

        self.mood_db = Mood_db()

    
    def quotes(self):
        """
        Retrieves a list of quotes from the database.

        Returns:
            list: A list of quotes.
        """

        return self.mood_db.quotes()
    
    def tips(self):
        """
        Retrieves a list of tips from the database.

        Returns:
            list: A list of tips.
        """
        return self.mood_db.tips()
    
    def mood_score(self, rating, description, influence):
        """
        Calculates or retrieves the mood score based on the provided rating, description, and influence.

        Args:
            rating (int): The mood rating provided by the user.
            description (str): A description of the mood.
            influence (str): Factors influencing the mood.

        Returns:
            int: The calculated or retrieved mood score.
        """

        return self.mood_db.mood_score(rating, description, influence)
    
    def mood_question(self):
        """
        Retrieves a mood-related question from the database.

        Returns:
            str: A mood-related question.
        """

        return self.mood_db.mood_question()
    
    def options(self):
        """
        Retrieves a list of options from the database.

        Returns:
            list: A list of options.
        """

        return self.mood_db.options()
    
    def supportive_messages(self):
        """
        Retrieves a list of supportive messages from the database.

        Returns:
            list: A list of supportive messages.
        """

        return self.mood_db.supportive_messages()
    
    def save_data(self, id_token):
        """
        Saves the user's data to the database using the provided ID token.

        Args:
            id_token (str): The ID token associated with the user's session.

        Returns:
            bool: True if the data was successfully saved, False otherwise.
        """
        
        return self.mood_db.save_data(id_token)
    
    def fetch_mood_history(self, id_token):
        """
        Fetches the user's mood history from the database.

        Args:
        id_token (str): The Firebase authentication token of the user.

        Returns:
        list: A list of mood history records.
        """
        return self.mood_db.fetch_mood_history(id_token)