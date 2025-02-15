from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QPushButton
import os
from view.mood_tracker import MoodTrackerWindow  # Importing mood tracker window


class MenuWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(os.path.join(os.path.dirname(__file__), "UI files", "menu.ui"), self)

        self.mood_tracker_pushbutton = self.findChild(QPushButton, "mood_tracker_pushbutton")
        self.mood_tracker_pushbutton.clicked.connect(self.open_mood_tracker)

    def open_mood_tracker(self):
        self.mood_window = MoodTrackerWindow()
        self.mood_window.resize(self.size())
        self.mood_window.show()
        self.close()
