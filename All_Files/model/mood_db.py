import sys
import os
from model.write_db import Write_db
from datetime import datetime

# Add the parent directory to the system path to allow module imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


class Mood_db:
    """
    A class to manage mood-related data and operations, including retrieving quotes, mood questions,
    options, tips, supportive messages, calculating mood scores, and saving mood data to a database.

    Attributes:
        user_data (dict): A dictionary to store user mood data, including mood rating, description,
                          influence, and creation timestamp.
        db (Write_db): An instance of the `Write_db` class to interact with the database.
    """

    def __init__(self):
        """
        Initializes the Mood_db class by setting up the `user_data` dictionary and creating an instance
        of the `Write_db` class for database interactions.
        """

        # Saving data to Firebase
        self.user_data = {
            "Mood rating": None,
            "Mood description": None,
            "Mood influenced by": None,
            'Created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        self.db = Write_db()
    
    def quotes(self):
        """
        Retrieves a dictionary of quotes categorized by mood.

        Returns:
            dict: A dictionary where keys are mood categories (e.g., "Very Happy", "Calm & Relaxed")
                  and values are lists of tuples containing quotes and their authors.
        """

        quote = {"Very Happy": [('Dalai Lama', 'Happiness is not something ready-made. It comes from your own actions.'), ('Oprah Winfrey', "The more you praise and celebrate your life, the more there is in life to celebrate.")], 
                "Calm & Relaxed": [('Buddha', 'Peace comes from within. Do not seek it without.'), ('Anne Lamott', 'Almost everything will work again if you unplug it for a few minutes… including you.')], 
                "Neutral": [('Alice Morse Earle', 'Every day may not be good, but there is something good in every day.'), ('William James', 'Act as if what you do makes a difference. It does.')], 
                "Stressed": [('Wayne Dyer', 'You cannot always control what goes on outside. But you can always control what goes on inside.'), ('Dan Millman', 'You don’t have to control your thoughts. You just have to stop letting them control you.')], 
                "Angry": [('Buddha', 'Holding onto anger is like drinking poison and expecting the other person to die.'), ('Nelson Mandela', 'Resentment is like drinking poison and then hoping it will kill your enemies.')]
                }
        
        return quote
    
    def mood_question(self):
        """
        Retrieves a list of mood-related questions.

        Returns:
            list: A list of strings containing mood-related questions.
        """

        question = ['How are you feeling today?', 'Which of the following best describes your mood right now?', 'What influenced your mood the most today?']
        return question

    def options(self):
        """
        Retrieves a dictionary of options for mood-related questions.

        Returns:
            dict: A dictionary where keys are question identifiers (e.g., '0', '1', '2') and values
                  are lists of options for each question.
        """

        option_dict = {'0': ['Very Bad', 'Bad', 'Normal', 'Good', 'Very Good'],
                        '1': ['Very Happy', 'Calm & Relaxed', 'Neutral', 'Stressed', 'Angry'],
                        '2': ['School', 'Work', 'Health', 'Weather', 'Sleep']}
        return option_dict

    def tips(self):
        """
        Retrieves a dictionary of tips categorized by mood influence.

        Returns:
            dict: A dictionary where keys are mood influences (e.g., "School", "Work") and values
                  are lists of tips for managing stress or improving mood.
        """

        tip = {"School": ['Prioritize tasks', 'Schedule your programs', 'Practice self-care', 'Avoid negative comparisons', 'Avoid procrastination'], 
                    "Work": ['Take Short Breaks', 'Declutter Your Space', 'Personalize Your Workspace', 'Communicate Openly', 'Unplug After Hours '], 
                    "Health": ['Prioritize Rest & Sleep', 'Stay Physically Active', 'Nourish Your Body with Healthy Foods', 'Manage Stress & Anxiety', 'Seek Medical Support When Needed'], 
                    "Weather": ['Listen to uplifting music', 'Engage in comforting activities', 'Stay socially connected', 'Practice Mindfulness & Relaxation', 'Create a Cozy & Positive Environment'], 
                    "Sleep": ['Maintain a Consistent Sleep Schedule', 'Create a Relaxing Bedtime Routine', 'Limit Screen Time Before Bed', 'Get Natural Light During the Day', 'Keep Your Sleep Environment Comfortable']
                    }
        
        return tip
    
    def supportive_messages(self):
        """
        Retrieves a dictionary of supportive messages categorized by mood.

        Returns:
            dict: A dictionary where keys are mood categories (e.g., "Very Happy", "Stressed") and
                  values are supportive messages tailored to each mood.
        """

        message =  {"Very Happy": "It's great to feel at peace. Take a deep breath and enjoy the moment. Keep nurturing this calm energy!",
                    "Calm & Relaxed": "It's okay to feel neutral. Every day is a new opportunity to find joy and meaning. Keep going!",
                    "Neutral": "You're not alone. Take a deep breath and give yourself a moment of kindness. \nYou've handled tough days before—you'll get through this too!",
                    "Stressed": "It's okay to have low days. Be gentle with yourself, and remember that brighter days are ahead. You matter.",
                    "Angry": "It's normal to feel this way sometimes. Take a deep breath, step back, and focus on what you can control. You've got this!"
                    }
        return message
    
    def mood_score(self, rating, description, influence):
        """
        Updates the user's mood data with the provided rating, description, and influence.

        Args:
            rating (str): The user's mood rating.
            description (str): A description of the user's mood.
            influence (str): The factor influencing the user's mood.
        """

        self.user_data["Mood rating"] = rating
        
        self.user_data["Mood description"] = description
    
        self.user_data["Mood influenced by"] = influence

    def save_data(self, id_token):
        """
        Saves the user's mood data to the database.

        Args:
            id_token (str): The ID token associated with the user's session.

        Returns:
            str: A message indicating whether the data was successfully saved or if there was an error.
        """
        
        # Saving data to Firebase
        user_id = self.db.auth.get_account_info(id_token)['users'][0]['localId']
        if None in self.user_data.values():
            return "Error: Some fields are missing!"
        else:
            self.db.database.child("Users").child(user_id).child("Mood").push(self.user_data, id_token)
            return "Your results have been saved"