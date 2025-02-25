import sys
import os

# Add the parent directory to the system path to allow module imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from model.stress_db import Journal_db

class Diary:
    
    def __init__(self):
        self.journal_db = Journal_db()
        
    def save(self, id_token, journal):
        self.journal_db.save(id_token, journal)