from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow
from PyQt5 import QtWidgets
from model.write_db import Write_db
from controller.MoodLogic import Mood
import os


class MoodTrackerWindow(QMainWindow):
    def __init__(self, id_token):
        super().__init__()
        self.id_token = id_token
        uic.loadUi(os.path.join(os.path.dirname(__file__), "UI files", "mood_tracker.ui"), self)
        
        self.mood = Mood()

       

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

        

        self.mood_tip_label = self.findChild(QtWidgets.QLabel, "mood_tip_label")
        self.mood_quote_label = self.findChild(QtWidgets.QLabel, "mood_quote_label")

        self.db = Write_db()
        self.id_token = id_token  # Saving the token for this user

    def rate_mood(self, rating):
        if self.quote_label1:
            self.quote_label1.setText(self.mood.quotes()[rating])
            self.mood.mood_rating(rating) # Saving rating locally
        
    

        # In the question 1
    def go_back_to_menu(self):
        from view.menu import MenuWindow
        self.menu_window = MenuWindow(self.id_token)
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
        
        self.mood.mood_reason(answer)  # Saving reason locally

    def answer_question3(self, answer):
        
        self.mood.mood_improvement(answer)   # Saving improvement locally

        if answer in self.mood.tips_and_quotes():
            self.mood_tip_label.setText(self.mood.tips_and_quotes()[answer]["tip"])
            self.mood_quote_label.setText(self.mood.tips_and_quotes()[answer]["quote"])

        # After question 3
    def finish_mood_tracker(self):
        self.mood.save_data(self.id_token)
        
        # Going back to Menu window
        from view.menu import MenuWindow
        self.menu_window = MenuWindow(self.id_token)
        self.menu_window.show()
        self.close()  # Closes Mood tracker window
