import sys
import os

# Add the parent directory to the system path to allow module imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from model.stress_db import Stress_db

class Stress:
    """
    A class to manage stress-related operations, including stress tests, results, tips, exercises,
    quotes, and saving stress-related data. It acts as an interface to interact with the `Stress_db` class.

    Attributes:
        stress_db (Stress_db): An instance of the `Stress_db` class to interact with the stress-related database.
    """

    def __init__(self):
        """
        Initializes the Stress class by creating an instance of the `Stress_db` class.
        """

        self.stress_db = Stress_db()
    
    def stress_test(self):
        """
        Retrieves the stress test questions or data from the database.

        Returns:
            list or dict: The stress test questions or data.
        """

        return self.stress_db.stress_test()
    
    def result(self, sum):
        """
        Calculates or retrieves the stress test result based on the provided sum.

        Args:
            sum (int): The sum of the user's stress test responses.

        Returns:
            str or dict: The stress test result or analysis.
        """

        return self.stress_db.result(sum)
    
    def tips(self):
        """
        Retrieves stress management tips from the database.

        Returns:
            list or dict: A list or dictionary of stress management tips.
        """

        return self.stress_db.tips()
    
    def exercises(self):
        """
        Retrieves stress-relief exercises from the database.

        Returns:
            list or dict: A list or dictionary of stress-relief exercises.
        """

        return self.stress_db.exercises()
    
    def quotes(self):
        """
        Retrieves motivational or stress-relief quotes from the database.

        Returns:
            list or dict: A list or dictionary of quotes.
        """

        return self.stress_db.quotes()
    
    def save_data(self, id_token, result):
        """
        Saves the user's stress test result to the database.

        Args:
            id_token (str): The ID token associated with the user's session.
            result (str or dict): The stress test result to be saved.

        Returns:
            bool: True if the data was successfully saved, False otherwise.
        """
        
        return self.stress_db.save_data(id_token, result)


    def fetch_stress_history(self, id_token):
        """
    Fetches the user's stress history from the database.

    Args:
        id_token (str): The Firebase authentication token of the user.

    Returns:
        list: A list of stress history records.
    """
        return self.stress_db.fetch_stress_history(id_token)


