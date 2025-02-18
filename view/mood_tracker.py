from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow
from PyQt5 import QtWidgets
# from model.write_db import Write_db
import os


class MoodTrackerWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(os.path.join(os.path.dirname(__file__), "UI files", "mood_tracker.ui"), self)

        self.mood_next_question1 = self.findChild(QtWidgets.QPushButton, "mood_next_question1")
        self.mood_back_question1 = self.findChild(QtWidgets.QPushButton, "mood_back_question1")
        # self.mood_next_question2 = self.findChild(QtWidgets.QPushButton, "mood_next_question2")

        self.mood_question1 = self.findChild(QtWidgets.QFrame, "mood_question1_frame")
        # self.mood_question2 = self.findChild(QtWidgets.QFrame, "mood_question2")
        # self.mood_question3 = self.findChild(QtWidgets.QFrame, "mood_question3")

        self.mood_question1.show()
        # self.mood_question2.hide()
        # self.mood_question3.hide()

        self.mood_next_question1.clicked.connect(self.show_question2)
        # self.mood_next_question2.clicked.connect(self.show_question3)
        self.mood_back_question1.clicked.connect(self.go_back_to_menu)

        self.mood_rate1 = self.findChild(QtWidgets.QRadioButton, "mood_rate1")
        self.mood_rate2 = self.findChild(QtWidgets.QRadioButton, "mood_rate2")
        self.mood_rate3 = self.findChild(QtWidgets.QRadioButton, "mood_rate3")
        self.mood_rate4 = self.findChild(QtWidgets.QRadioButton, "mood_rate4")
        self.mood_rate5 = self.findChild(QtWidgets.QRadioButton, "mood_rate5")

        self.mood_rate1.clicked.connect(lambda: self.rate_mood(1))
        self.mood_rate2.clicked.connect(lambda: self.rate_mood(2))
        self.mood_rate3.clicked.connect(lambda: self.rate_mood(3))
        self.mood_rate4.clicked.connect(lambda: self.rate_mood(4))
        self.mood_rate5.clicked.connect(lambda: self.rate_mood(5))

        self.quote_label1 = self.findChild(QtWidgets.QLabel, "quote_label1")

        self.quotes1 = {
            1: "It's okay to have bad days. Tomorrow is a new start.",
            2: "Take a deep breath. You are doing your best.",
            3: "Keep going, one step at a time.",
            4: "Good job! You are making progress.",
            5: "Amazing! Celebrate the little victories."
        }

        # self.db = Write_db()

    def rate_mood(self, rating):
        if self.quote_label1:
            self.quote_label1.setText(self.quotes1[rating])
        print(f"User rated: {rating}")

        # Saving to Firebase
        #self.db.database.child("MoodTrackerAnswers").push({
        #    "question": "How are you feeling today?",
        #    "answer": rating
        #})

    def show_question2(self):
        print("Moving to the question 2, not implemented yet")
        #self.mood_question1.hide()
        #self.mood_question2.show()

    def go_back_to_menu(self):
        from view.menu import MenuWindow
        self.menu_window = MenuWindow()
        self.menu_window.show()
        self.close()  # Closes Mood tracker window
    
    #def show_question3(self):
        #self.mood_question2.hide()
        #self.mood_question3.show()
