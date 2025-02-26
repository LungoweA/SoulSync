from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QPushButton
import os
from .mood_tracker import MoodTrackerWindow
from .stress_tracker import StressTracker
<<<<<<< HEAD
from .journal import Journal
=======

>>>>>>> Michael2024-coder



class MenuWindow(QMainWindow):
    def __init__(self, id_token):
        super().__init__()
        self.id_token = id_token
        uic.loadUi(os.path.join(os.path.dirname(__file__), "UI files", "menu.ui"), self)

        self.mood_tracker_pushbutton = self.findChild(QPushButton, "mood_tracker_pushbutton")
        self.stress_tracker_pushbutton = self.findChild(QPushButton, "stress_tracker_pushbutton")
        self.diary_pushbutton = self.findChild(QPushButton, "diary_pushbutton")
        self.stress_history_btn = self.findChild(QPushButton, "stress_history_btn")
        self.journal_history_btn = self.findChild(QPushButton, "journal_history_btn")
        self.settings_btn = self.findChild(QPushButton, "settings_btn")
        
        self.mood_tracker_pushbutton.clicked.connect(self.open_mood_tracker)
        self.stress_tracker_pushbutton.clicked.connect(self.open_stress_tracker)
        self.diary_pushbutton.clicked.connect(self.open_journal)

    def open_mood_tracker(self):
        self.mood_window = MoodTrackerWindow(self.id_token)
        self.mood_window.resize(self.size())
        self.mood_window.show()
        self.close()

    def open_stress_tracker(self):
        self.stress_window = StressTracker(self.id_token)
        self.stress_window.resize(self.size())
        self.stress_window.show()
        self.close()
        
    
    def open_journal(self):
<<<<<<< HEAD
=======
        from All_Files.view.journal import Journal
>>>>>>> Michael2024-coder
        self.journal_window = Journal(self.id_token)
        self.journal_window.resize(self.size())
        self.journal_window.show()
        self.close()