from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow
import os


class MoodTrackerWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(os.path.join(os.path.dirname(__file__), "UI files", "mood_tracker.ui"), self)
