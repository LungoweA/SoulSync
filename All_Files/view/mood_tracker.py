import sys
import os

# Add the absolute path of the SoulSync directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from PyQt5 import uic
from PyQt5.QtWidgets import (QMainWindow, QLabel, QRadioButton, QPushButton, QGroupBox)
from All_Files.controller.MoodLogic import Mood
from .tips import Tips
import os


class MoodTrackerWindow(QMainWindow):
    """
    A class representing the Mood Tracker window in the application. This window allows users to
    answer mood-related questions, track their mood, and view tips based on their responses.

    Attributes:
        id_token (str): The ID token associated with the user's session.
        mood (Mood): An instance of the `Mood` class for handling mood-related logic.
        num (int): The current question number.
        questions (list): A list of mood-related questions.
        option (dict): A dictionary of options for each question.
        dict (dict): A dictionary to store user responses.
        rate (str): The user's mood rating.
        description (str): The user's mood description.
        influence (str): The factor influencing the user's mood.
        question_no_label (QLabel): Label to display the question number.
        question_label (QLabel): Label to display the question.
        error_label (QLabel): Label to display error messages.
        option1_label (QLabel): Label for the first option.
        option2_label (QLabel): Label for the second option.
        option3_label (QLabel): Label for the third option.
        option4_label (QLabel): Label for the fourth option.
        option5_label (QLabel): Label for the fifth option.
        radio_btn1 (QRadioButton): Radio button for the first option.
        radio_btn2 (QRadioButton): Radio button for the second option.
        radio_btn3 (QRadioButton): Radio button for the third option.
        radio_btn4 (QRadioButton): Radio button for the fourth option.
        radio_btn5 (QRadioButton): Radio button for the fifth option.
        back_btn (QPushButton): Button to navigate to the previous question.
        next_btn (QPushButton): Button to navigate to the next question.
        menu_btn (QPushButton): Button to return to the main menu.
        tips_btn (QPushButton): Button to view tips based on the user's responses.
        group_box (QGroupBox): Group box to display error messages.
    """

    def __init__(self, id_token):
        """
        Initializes the MoodTrackerWindow and sets up the UI elements and event handlers.

        Args:
            id_token (str): The ID token associated with the user's session.
        """

        super().__init__()
        self.id_token = id_token
        uic.loadUi(os.path.join(os.path.dirname(__file__), "UI files", "mood_tracker.ui"), self)
        
        self.mood = Mood()

        self.num = 1
        self.questions = self.mood.mood_question()
        self.option = self.mood.options()
        self.id_token = id_token
        
        self.dict = {"1":0, "2":0, "3":0}
        
        self.rate = None
        self.description = None
        self.influence = None
        
        self.question_no_label = self.findChild(QLabel, "question_no_label")
        self.question_label = self.findChild(QLabel, "question_label")
        self.error_label = self.findChild(QLabel, "error_label")
        
        self.option1_label = self.findChild(QLabel, "option1_label")
        self.option2_label = self.findChild(QLabel, "option2_label")
        self.option3_label = self.findChild(QLabel, "option3_label")
        self.option4_label = self.findChild(QLabel, "option4_label")
        self.option5_label = self.findChild(QLabel, "option5_label")
        
        self.radio_btn1 = self.findChild(QRadioButton, "radio_btn1")
        self.radio_btn2 = self.findChild(QRadioButton, "radio_btn2")
        self.radio_btn3 = self.findChild(QRadioButton, "radio_btn3")
        self.radio_btn4 = self.findChild(QRadioButton, "radio_btn4")
        self.radio_btn5 = self.findChild(QRadioButton, "radio_btn5")
        
        self.back_btn = self.findChild(QPushButton, "back_btn")
        self.next_btn = self.findChild(QPushButton, "next_btn")
        self.menu_btn = self.findChild(QPushButton, "menu_btn")
        self.tips_btn = self.findChild(QPushButton, "tips_btn")
        
        self.group_box = self.findChild(QGroupBox, 'groupBox_2')
        
        self.group_box.hide()
        
        
        self.initial_question()
        self.back_btn.clicked.connect(self.back)
        
        self.next_btn.clicked.connect(self.next)
        self.next_btn.clicked.connect(self.finish)
        self.menu_btn.clicked.connect(self.main)
        self.tips_btn.clicked.connect(self.show_tips)
        
    def initial_question(self):
        """
        Sets up the initial question and options in the UI.
        """

        self.question_no_label.setText(f'Question {self.num}')
        self.question_label.setText(self.questions[self.num-1])
        self.option1_label.setText(self.option[str(self.num-1)][0])
        self.option2_label.setText(self.option[str(self.num-1)][1])
        self.option3_label.setText(self.option[str(self.num-1)][2])
        self.option4_label.setText(self.option[str(self.num-1)][3])
        self.option5_label.setText(self.option[str(self.num-1)][4])
        
        self.radio_btn1.clicked.connect(self.no1)
        self.radio_btn2.clicked.connect(self.no2)
        self.radio_btn3.clicked.connect(self.no3)
        self.radio_btn4.clicked.connect(self.no4)
        self.radio_btn5.clicked.connect(self.no5)
        
        self.back_btn.hide()
        self.tips_btn.hide()
        
    def back(self):
        """
        Navigates to the previous question and updates the UI.
        """

        if self.num > 1:
            self.num -= 1
            self.question_label.setText(self.questions[self.num-1])
            self.question_no_label.setText(f"Question {self.num}")
            self.option1_label.setText(self.option[str(self.num-1)][0])
            self.option2_label.setText(self.option[str(self.num-1)][1])
            self.option3_label.setText(self.option[str(self.num-1)][2])
            self.option4_label.setText(self.option[str(self.num-1)][3])
            self.option5_label.setText(self.option[str(self.num-1)][4])
            self.next_btn.show()
            if self.num == 1:
                self.back_btn.hide()
            self.tips_btn.hide()
            self.group_box.hide()
            self.reset_checked()
            self.set_checked()
            
            
    def next(self):
        """
        Navigates to the next question and updates the UI. Displays an error message if no option is selected.
        """

        if self.num < 3 and self.check_button():
            self.num += 1
            self.question_label.setText(self.questions[self.num-1])
            self.question_no_label.setText(f"Question {self.num}")
            self.option1_label.setText(self.option[str(self.num-1)][0])
            self.option2_label.setText(self.option[str(self.num-1)][1])
            self.option3_label.setText(self.option[str(self.num-1)][2])
            self.option4_label.setText(self.option[str(self.num-1)][3])
            self.option5_label.setText(self.option[str(self.num-1)][4])
            
            self.back_btn.show()
            
            self.error_label.setText("")
            self.group_box.hide()
            self.reset_checked()
            self.set_checked()
            
            
        elif not self.check_button():
            self.group_box.show()
            self.group_box.setStyleSheet(
                "background-color: #FFB3B3;"
                "border: 2px solid #FF4D4D;"
                "border-radius: 8px;"
                "padding: 10px;"
                "font-weight: bold;"
                "color: #990000;"
            )
            self.error_label.setStyleSheet('color: Black;')
            self.error_label.setText(f"⚠️ Please select an option before continuing.")
    
    def mood_rate(self):
        """
        Determines the user's mood rating based on their response to the first question.
        """

        num = self.dict['1']
        self.rate = self.option['0'][num-1]
        
        
    def mood_description(self):
        """
        Determines the user's mood description based on their response to the second question.
        """

        num = self.dict['2']
        self.description = self.option['1'][num-1]
        
    
    def mood_influence(self):
        """
        Determines the factor influencing the user's mood based on their response to the third question.
        """

        num = self.dict['3']
        self.influence = self.option['2'][num-1]
        
            
    def finish(self):
        """
        Finalizes the mood tracking process and prepares the UI for displaying tips.
        """

        if self.num == 3 and self.check_button():
            self.next_btn.hide()
            self.tips_btn.show()
            self.mood_rate()
            self.mood_description()
            self.mood_influence()
            
            
    def set_checked(self):
        """
        Sets the radio button to the user's previously selected option for the current question.
        """

        if self.dict[str(self.num)] == 1:
            self.radio_btn1.setChecked(True)
        elif self.dict[str(self.num)] == 2:
            self.radio_btn2.setChecked(True)
        elif self.dict[str(self.num)] == 3:
            self.radio_btn3.setChecked(True)
        elif self.dict[str(self.num)] == 4:
            self.radio_btn4.setChecked(True)
        elif self.dict[str(self.num)] == 5:
            self.radio_btn5.setChecked(True)
    
    def no1(self):
        """
        Records the user's selection of the first option for the current question.
        """

        self.dict[str(self.num)] = 1
    
    def no2(self):
        """
        Records the user's selection of the second option for the current question.
        """

        self.dict[str(self.num)] = 2
        
    def no3(self):
        """
        Records the user's selection of the third option for the current question.
        """

        self.dict[str(self.num)] = 3
        
    def no4(self):
        """
        Records the user's selection of the fourth option for the current question.
        """

        self.dict[str(self.num)] = 4
        
    def no5(self):
        """
        Records the user's selection of the fifth option for the current question.
        """

        self.dict[str(self.num)] = 5
            
    def reset_checked(self):
        """
        Resets all radio buttons to an unchecked state.
        """

        self.radio_btn1.setAutoExclusive(False)
        self.radio_btn1.setChecked(False)
        self.radio_btn1.setAutoExclusive(True)
        
        self.radio_btn2.setAutoExclusive(False)
        self.radio_btn2.setChecked(False)
        self.radio_btn2.setAutoExclusive(True)
        
        self.radio_btn3.setAutoExclusive(False)
        self.radio_btn3.setChecked(False)
        self.radio_btn3.setAutoExclusive(True)
        
        self.radio_btn4.setAutoExclusive(False)
        self.radio_btn4.setChecked(False)
        self.radio_btn4.setAutoExclusive(True)
        
        self.radio_btn5.setAutoExclusive(False)
        self.radio_btn5.setChecked(False)
        self.radio_btn5.setAutoExclusive(True)
        
    def check_button(self):
        """
        Checks if any radio button is selected for the current question.

        Returns:
            bool: True if any radio button is selected, False otherwise.
        """

        return self.radio_btn1.isChecked() or self.radio_btn2.isChecked() or self.radio_btn3.isChecked() or self.radio_btn4.isChecked() or self.radio_btn5.isChecked()
        
    def clear_window(self):
        """
        Clears all labels and hides the error group box.
        """

        self.question_label.setText("")
        self.question_no_label.setText("")
        self.option1_label.setText("")
        self.option2_label.setText("")
        self.option3_label.setText("")
        self.option4_label.setText("")
        self.option5_label.setText("")
        self.error_label.setText("")
        self.group_box.hide()
    
    def show_tips(self):
        """
        Opens the tips window and closes the current mood tracker window.
        """

        self.tips_window = Tips(self.id_token, self.rate, self.description, self.influence)
        self.clear_window()
        self.reset_checked()
        self.tips_window.show()
        self.close()
        
    def main(self):
        """
        Returns to the main menu and closes the current mood tracker window.
        """
        
        from view.menu import MenuWindow
        self.menu_window = MenuWindow(self.id_token)
        self.clear_window()
        self.reset_checked()
        self.menu_window.show()
        self.close()  # Closes Mood tracker window
        
        