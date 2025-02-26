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
    
    def tips(self):
        return self.mood_db.tips()
    
    def mood_score(self, rating, description, influence):
        return self.mood_db.mood_score(rating, description, influence)
    
    def mood_question(self):
        return self.mood_db.mood_question()
    
    def options(self):
        return self.mood_db.options()
    
    def supportive_messages(self):
        return self.mood_db.supportive_messages()
    
    def save_data(self, id_token):
        return self.mood_db.save_data(id_token)