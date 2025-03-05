from All_Files.model.write_db import Write_db
from datetime import datetime

class Stress_db:
    """
    A class to manage stress-related operations, including stress tests, results, exercises, tips,
    quotes, and saving stress data to a database. It acts as an interface to interact with the `Write_db` class.

    Attributes:
        sums (int): A placeholder for storing the sum of stress test scores (default is 0).
        total (int): The total possible score for the stress test (default is 25).
        db (Write_db): An instance of the `Write_db` class to interact with the database.
    """

    def __init__(self):
        """
        Initializes the Stress_db class by setting up default values for `sums`, `total`, and
        creating an instance of the `Write_db` class for database interactions.
        """

        self.sums = 0
        self.total = 25
        self.db = Write_db()
        
    def stress_test(self):
        """
        Retrieves a list of stress test questions.

        Returns:
            list: A list of strings containing stress test questions.
        """

        questions = ["I often have difficulty concentrating.", "I often forget meetings or the names of people I know very well.",
                    "I get easily angered and sometimes lose my composure which is abnormal for me.",
                    "Sometimes I sleep restlessly, wake at night, and don't feel rested after a night's sleep.",
                    "I get abnormally tired from daily chores and socializing with others."]
        
        return questions

    def result(self, sum):
        """
        Calculates the stress level based on the provided sum of stress test scores.

        Args:
            sum (int): The sum of the user's stress test responses.

        Returns:
            str: The stress level, which can be "Low", "Moderate", or "High".
        """

        score = (sum/self.total) * 100

        if 80 <= score <= 100:
            return "Low"
        elif 40 < score < 80:
            return "Moderate"
        elif score <= 40:
            return "High"
        
    def exercises(self):
        """
        Retrieves a dictionary of stress-relief exercises categorized by stress level.

        Returns:
            dict: A dictionary where keys are stress levels ("Low", "Moderate", "High") and values
                  are lists of recommended exercises.
        """

        exercise_dict = {"Low": ["Walking or Light Jogging", "Yoga (Gentle Flow or Hatha Yoga)", "Cycling (Recreational)",
                                "Bodyweight Strength Training", "Swimming"],
                        "Moderate": ["Brisk Walking (Outside, If Possible)", "Strength Training", "Pilates or Vinyasa Yoga",
                                    "Dancing or Zumba", "Tai Chi"],
                        "High": ["Slow, Controlled Breathing Exercises", "Gentle Yoga (Restorative or Yin Yoga)", "Progressive Muscle Relaxation",
                                "Light Stretching or Foam Rolling", "Nature Walks or Forest Bathing"]}
        
        return exercise_dict
    
    def tips(self):
        """
        Retrieves a dictionary of stress management tips categorized by stress level.

        Returns:
            dict: A dictionary where keys are stress levels ("Low", "Moderate", "High") and values
                  are lists of tips for managing stress.
        """

        tip_dict = {"Low": ["Stay Active e.g. exercise regularly", "Maintain Good Sleep", "Practice Gratitude",
                            "Enjoy Hobbies", "Stay Social"],
                    "Moderate": ["Take Short Breaks e.g. use the Pomodoro technique.", "Try Deep Breathing e.g. practice box breathing.",
                                "Reduce Stimulants like caffeine and processed sugar.", "Practice Mindful Journaling", "Listen to Music"],
                    "High": ["Limit Social Media & News", "Sleep Well e.g. aim for 7-9 hours", "Eat A Healthy Diet e.g. focus on stress reducing food",
                            "Try Laugh Therapy", "Engage In A Distraction Activity e.g. play a game or puzzle"]}
        
        return tip_dict
        
    def quotes(self):
        """
        Retrieves a dictionary of motivational quotes categorized by stress level.

        Returns:
            dict: A dictionary where keys are stress levels ("Low", "Moderate", "High") and values
                  are lists of tuples containing quotes and their authors.
        """

        quote_dict = {"Low": [("Robert Brault", "Enjoy the little things, for one day you may look back and realize they were the big things."),
                            ("Thomas Merton", "Happiness is not a matter of intensity but of balance, order, rhythm, and harmony.")],
                    "Moderate": [("Robert H. Schuller", "Tough times never last, but tough people do."), ("Anne Lamott",
                                "Almost everything will work again if you unplug it for a few minutes… including you.")],
                    "High": [("Persian Proverb", "This too shall pass. No storm lasts forever."), ("Brené Brown",
                                "Give yourself the same care and kindness you so freely give to others.")]}
    
        return quote_dict
    
    
    def save_data(self, id_token, result):
        """
        Saves the user's stress test result to the database.

        Args:
            id_token (str): The ID token associated with the user's session.
            result (str): The stress level result to be saved.

        Returns:
            Exception: If an error occurs during the save operation, the exception is returned.
        """
        
        # Saving data to Firebase
        user_id = self.db.auth.get_account_info(id_token)['users'][0]['localId']
        stress_data = {"Stress level": result,
                        "Created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        try:
            self.db.database.child("Users").child(user_id).child("Stress").push(stress_data, id_token)
        except Exception as err:
            return err
        
    def fetch_stress_history(self, id_token):
        """
    Fetches the user's stress history from Firebase.

    Args:
        id_token (str): The Firebase authentication token of the user.

    Returns:
        list: A list of dictionaries containing stress history data.
    """
        try:
            user_id = self.db.auth.get_account_info(id_token)['users'][0]['localId']
            stress_data = self.db.database.child("Users").child(user_id).child("Stress").get(id_token).val()

            if stress_data:
                return [
                    {"Created_at": entry["Created_at"], "Stress Level": entry["Stress level"]}
                    for entry in stress_data.values()
                ]
            else:
                return []
        except Exception as e:
            print(f"Error fetching stress history: {e}")
            return []
    
    
