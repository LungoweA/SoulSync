import sys
import os

# Add the parent directory to the system path to allow module imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from model.stress_db import Stress_db
from model.stress_db import Journal_db

class Stress:
    
    def __init__(self):
        self.stress_db = Stress_db()
    
    def stress_test(self):
        return self.stress_db.stress_test()
    
    def result(self, sum):
        return self.stress_db.result(sum)
    
    def tips(self):
        return self.stress_db.tips()
    
    def exercises(self):
        return self.stress_db.exercises()
    
    def quotes(self):
        return self.stress_db.quotes()
    
    def save_data(self, id_token, result):
        return self.stress_db.save_data(id_token, result)



class Diary:
    
    def __init__(self):
        self.journal_db = Journal_db()
        
    def save(self, id_token, journal):
        self.journal_db.save(id_token, journal)