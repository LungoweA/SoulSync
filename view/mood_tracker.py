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

        self.mood_question1 = self.findChild(QtWidgets.QFrame, "mood_question1_frame")
        self.mood_question2 = self.findChild(QtWidgets.QFrame, "mood_question2_frame")
        self.mood_question3 = self.findChild(QtWidgets.QFrame, "mood_question3_frame")

        self.mood_question1.show()
        self.mood_question2.hide()
        self.mood_question3.hide()

        self.mood_next_question1.clicked.connect(self.show_question2)
        self.mood_next_question2.clicked.connect(self.show_question3)
        self.mood_back_question1.clicked.connect(self.go_back_to_menu)

        # QUESTION 1
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

        # QUESTION 2
        self.mood_school = self.findChild(QtWidgets.QRadioButton, "mood_school")
        self.mood_work = self.findChild(QtWidgets.QRadioButton, "mood_work")
        self.mood_relationship = self.findChild(QtWidgets.QRadioButton, "mood_relationship")
        self.mood_weather = self.findChild(QtWidgets.QRadioButton, "mood_weather")
        self.mood_health = self.findChild(QtWidgets.QRadioButton, "mood_health")
        self.mood_sleep = self.findChild(QtWidgets.QRadioButton, "mood_sleep")

        self.mood_back_question2 = self.findChild(QtWidgets.QPushButton, "mood_back_question2")
        self.mood_next_question2 = self.findChild(QtWidgets.QPushButton, "mood_next_question2")

        self.mood_school.clicked.connect(lambda: self.answer_question2("School"))
        self.mood_work.clicked.connect(lambda: self.answer_question2("Work"))
        self.mood_relationship.clicked.connect(lambda: self.answer_question2("Relationship"))
        self.mood_weather.clicked.connect(lambda: self.answer_question2("Weather"))
        self.mood_health.clicked.connect(lambda: self.answer_question2("Health"))
        self.mood_sleep.clicked.connect(lambda: self.answer_question2("Sleep"))

        self.mood_back_question2.clicked.connect(self.show_question1)
        self.mood_next_question2.clicked.connect(self.show_question3)

        # QUESTION 3
        self.mood_music = self.findChild(QtWidgets.QRadioButton, "mood_music")
        self.mood_enjoy = self.findChild(QtWidgets.QRadioButton, "mood_enjoy")
        self.mood_rest = self.findChild(QtWidgets.QRadioButton, "mood_rest")
        self.mood_talk = self.findChild(QtWidgets.QRadioButton, "mood_talk")
        self.mood_walk = self.findChild(QtWidgets.QRadioButton, "mood_walk")

        self.mood_back_question3 = self.findChild(QtWidgets.QPushButton, "mood_back_question3")
        self.mood_next_question3 = self.findChild(QtWidgets.QPushButton, "mood_next_question3")

        self.mood_music.clicked.connect(lambda: self.answer_question3("Music"))
        self.mood_enjoy.clicked.connect(lambda: self.answer_question3("Enjoy"))
        self.mood_rest.clicked.connect(lambda: self.answer_question3("Rest"))
        self.mood_talk.clicked.connect(lambda: self.answer_question3("Talk"))
        self.mood_walk.clicked.connect(lambda: self.answer_question3("Walk"))

        self.mood_back_question3.clicked.connect(self.show_question2)
        self.mood_next_question3.clicked.connect(self.finish_mood_tracker)

        # TIPS AND QUOTES
        self.tips_and_quotes = {
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

        self.mood_tip_label = self.findChild(QtWidgets.QLabel, "mood_tip_label")
        self.mood_quote_label = self.findChild(QtWidgets.QLabel, "mood_quote_label")

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

        # In the question 1
    def go_back_to_menu(self):
        from view.menu import MenuWindow
        self.menu_window = MenuWindow()
        self.menu_window.show()
        self.close()  # Closes Mood tracker window

    def show_question1(self):
        self.mood_question1.show()
        self.mood_question2.hide()
        self.mood_question3.hide()

    def show_question2(self):
        self.mood_question1.hide()
        self.mood_question2.show()
        self.mood_question3.hide()

    def show_question3(self):
        self.mood_question1.hide()
        self.mood_question2.hide()
        self.mood_question3.show()

    def answer_question2(self, answer):
        print(f"User selected: {answer} for question 2")

    def answer_question3(self, answer):
        print(f"User selected: {answer} for question 3")

        if answer in self.tips_and_quotes:
            self.mood_tip_label.setText(self.tips_and_quotes[answer]["tip"])
            self.mood_quote_label.setText(self.tips_and_quotes[answer]["quote"])

        # After question 3
    def finish_mood_tracker(self):
        from view.menu import MenuWindow
        self.menu_window = MenuWindow()
        self.menu_window.show()
        self.close()  # Closes Mood tracker window
