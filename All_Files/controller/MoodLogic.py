import sys
import os

# Add the parent directory to the system path to allow module imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from model.mood_db import Mood_db

class Mood:

    def __init__(self):
        self.mood_db = Mood_db()

    
    def quotes(self):
        return self.mood_db.quotes()
    
    def tips_and_quotes(self):
        return self.mood_db.tips_and_quotes()
    
    def mood_rating(self, rating):
        return self.mood_db.mood_rating(rating)
    
    def mood_reason(self, reason):
        return self.mood_db.mood_reason(reason)
    
    def mood_improvement(self, improvement):
        return self.mood_db.mood_improvement(improvement)
    
    def save_data(self, id_token):
        return self.mood_db.save_data(id_token)