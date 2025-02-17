from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow
from PyQt5 import QtWidgets
import os


class MoodTrackerWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(os.path.join(os.path.dirname(__file__), "UI files", "mood_tracker.ui"), self)

        self.mood_question1 = self.findChild(QtWidgets.QFrame, "mood_question1")

        # self.mood_rate1 = self.findChild(QtWidgets.QRadioButton, "mood_rate1")
        # self.mood_rate2 = self.findChild(QtWidgets.QRadioButton, "mood_rate2")
        # self.mood_rate3 = self.findChild(QtWidgets.QRadioButton, "mood_rate3")
        # self.mood_rate4 = self.findChild(QtWidgets.QRadioButton, "mood_rate4")
        # self.mood_rate5 = self.findChild(QtWidgets.QRadioButton, "mood_rate5")

        # self.mood_rate1.clicked.connect(lambda: self.rate_mood(1))
        # self.mood_rate2.clicked.connect(lambda: self.rate_mood(2))
        # self.mood_rate3.clicked.connect(lambda: self.rate_mood(3))
        # self.mood_rate4.clicked.connect(lambda: self.rate_mood(4))
        # self.mood_rate5.clicked.connect(lambda: self.rate_mood(5))

        self.quote_label1 = self.findChild(QtWidgets.QLabel, "quote_label1")

        self.quotes1 = {
            1: "It's okay to have bad days. Tomorrow is a new start.",
            2: "Take a deep breath. You are doing your best.",
            3: "Keep going, one step at a time.",
            4: "Good job! You are making progress.",
            5: "Amazing! Celebrate the little victories."
        }

    def rate_mood(self, rating):
        if self.quote_label1:
            self.quote_label1.setText(self.quotes1[rating])
        print(f"User rated: {rating}")
