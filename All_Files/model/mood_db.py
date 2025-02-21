import sys
import os
from model.write_db import Write_db

# Add the parent directory to the system path to allow module imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


class Mood_db:
    
    def __init__(self):
        # Saving data to Firebase
        self.user_data = {
            "mood_rating": None,
            "mood_reason": None,
            "mood_improvement": None
        }
        
        self.db = Write_db()
    
    def quotes(self):
        self.quotes1 = {
            1: "It's okay to have bad days. Tomorrow is a new start.",
            2: "Take a deep breath. You are doing your best.",
            3: "Keep going, one step at a time.",
            4: "Good job! You are making progress.",
            5: "Amazing! Celebrate the little victories."
        }
        
        return self.quotes1
    
    
    def tips_and_quotes(self):
        # TIPS AND QUOTES
        self.tips_n_quotes = {
            "Music": {
                "tip": "Listening to your favorite songs can relax your mind and improve your mood.",
                "quote": "Where words fail, music speaks."
            },
            "Enjoy": {
                "tip": "Do something you enjoy today, like watching a movie or reading a book.",
                "quote": "Happiness is not something ready-made. It comes from your own actions."
            },
            "Rest": {
                "tip": "Take some time to rest. A short nap or just relaxing can help you recharge.",
                "quote": "Resting is not laziness, it is medicine for the soul."
            },
            "Talk": {
                "tip": "Reach out to a friend or family member. Talking about your feelings can help a lot.",
                "quote": "A burden shared is a burden halved."
            },
            "Walk": {
                "tip": "Go for a short walk outside. Fresh air and movement can clear your mind.",
                "quote": "Every step you take is a step closer to a better mood."
            }
        }
        
        return self.tips_n_quotes
    
    def mood_rating(self, rating):
        self.user_data["mood_rating"] = rating
        
    def mood_reason(self, reason):
        self.user_data["mood_reason"] = reason
    
    def mood_improvement(self, improvement):
        self.user_data["mood_improvement"] = improvement
    
    def save_data(self, id_token):
        # Saving data to Firebase
        user_id = self.db.auth.get_account_info(id_token)['users'][0]['localId']
        if None in self.user_data.values():
            return "Error: Some fields are missing!"
        else:
            self.db.database.child("Users").child(user_id).child("MoodTrackerAnswers").push(self.user_data, id_token)
            return "Your results have been saved"