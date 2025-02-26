import sys
import os
from PyQt5 import uic
from PyQt5.QtWidgets import (QMainWindow, QPushButton, QRadioButton, QLabel, QGroupBox)
from PyQt5.QtCore import *
from All_Files.controller.StressLogic import Stress
from .results import Result


# Add the parent directory to the system path to allow module imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))



class StressTracker(QMainWindow):
    """
    A class representing the Stress Tracker window in the application. This window allows users to
    answer stress-related questions, track their stress level, and view results.

    Attributes:
        stress (Stress): An instance of the `Stress` class for handling stress-related logic.
        id_token (str): The ID token associated with the user's session.
        questions (list): A list of stress-related questions.
        num (int): The current question number.
        dict (dict): A dictionary to store user responses.
        question_no_label (QLabel): Label to display the question number.
        question_label (QLabel): Label to display the question.
        error_label (QLabel): Label to display error messages.
        radio_btn1 (QRadioButton): Radio button for the first option.
        radio_btn2 (QRadioButton): Radio button for the second option.
        radio_btn3 (QRadioButton): Radio button for the third option.
        radio_btn4 (QRadioButton): Radio button for the fourth option.
        radio_btn5 (QRadioButton): Radio button for the fifth option.
        back_btn (QPushButton): Button to navigate to the previous question.
        next_btn (QPushButton): Button to navigate to the next question.
        main_btn (QPushButton): Button to return to the main menu.
        results_btn (QPushButton): Button to display the stress results.
        group_box (QGroupBox): Group box to display error messages.
    """
    
    def __init__(self, id_token,parent=None):
        """
        Initializes the StressTracker window and sets up the UI elements and event handlers.

        Args:
            id_token (str): The ID token associated with the user's session.
            parent (QWidget, optional): The parent widget. Defaults to None.
        """

        super(StressTracker, self).__init__(parent)
        uic.loadUi(os.path.join(os.path.dirname(__file__), "UI files", "stress_tracker.ui"), self)
        
        
        self.stress = Stress()
        self.id_token = id_token
        self.questions = self.stress.stress_test()  # stress tracker questions
        self.num = 1                                # stress tracker question number
        self.dict = {"1":0, "2":0, "3":0, "4":0, "5":0}
        
        self.question_no_label = self.findChild(QLabel, "question_no_label")
        self.question_label = self.findChild(QLabel, "question_label")
        self.error_label = self.findChild(QLabel, "error_label")
        
        self.radio_btn1 = self.findChild(QRadioButton, "radio_btn1")
        self.radio_btn2 = self.findChild(QRadioButton, "radio_btn2")
        self.radio_btn3 = self.findChild(QRadioButton, "radio_btn3")
        self.radio_btn4 = self.findChild(QRadioButton, "radio_btn4")
        self.radio_btn5 = self.findChild(QRadioButton, "radio_btn5")
        
        self.back_btn = self.findChild(QPushButton, "back_btn")
        self.next_btn = self.findChild(QPushButton, "next_btn")
        self.main_btn = self.findChild(QPushButton, "main_btn")
        self.results_btn = self.findChild(QPushButton, "results_btn")
        
        self.group_box = self.findChild(QGroupBox, 'groupBox_2')
        
        
        self.initial_question()
        
        self.group_box.hide()
        
        self.back_btn.clicked.connect(self.back)
        
        self.next_btn.clicked.connect(self.next)
        self.next_btn.clicked.connect(self.finish)
        self.main_btn.clicked.connect(self.main)
        
        self.results_btn.clicked.connect(self.display_result)
        
    
    def initial_question(self):
        """
        Sets up the initial question and connects radio buttons to their respective methods.
        """

        self.question_no_label.setText(f"Question {self.num}")
        self.question_label.setText(self.questions[self.num-1])
        
        self.radio_btn1.clicked.connect(self.no1)
        self.radio_btn2.clicked.connect(self.no2)
        self.radio_btn3.clicked.connect(self.no3)
        self.radio_btn4.clicked.connect(self.no4)
        self.radio_btn5.clicked.connect(self.no5)
        
        self.back_btn.hide()
        self.results_btn.hide()
        
        
    def back(self):
        """
        Navigates to the previous question and updates the UI.
        """

        if self.num > 1:
            self.num -= 1
            self.question_label.setText(self.questions[self.num-1])
            self.question_no_label.setText(f"Question {self.num}")
            
            self.results_btn.hide()
            self.next_btn.show()
            
            if self.num == 1:
                self.back_btn.hide()
            self.group_box.hide()
            self.reset_checked()
            self.set_checked()
        
        
    
    def next(self):
        """
        Navigates to the next question and updates the UI. Displays an error message if no option is selected.
        """

        if self.num < 5 and self.check_button():
            self.num += 1
            self.question_label.setText(self.questions[self.num-1])
            self.question_no_label.setText(f"Question {self.num}")
            self.back_btn.show()
            
            
            self.reset_checked()
            self.set_checked()
            self.error_label.setText("")
            self.group_box.hide()
            
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
            
        
    def finish(self):
        """
        Finalizes the stress tracking process and prepares the UI for displaying results.
        """

        if self.num == 5 and self.check_button():
            self.next_btn.hide()
            self.results_btn.show()
            
    def result(self):
        """
        Calculates the total stress score based on user responses.

        Returns:
            int: The total stress score.
        """

        value = list(self.dict.values())
        return sum(value)
            
    def set_checked(self):
        """
        Sets the radio button to the user's previously selected option for the current question.
        """

        if self.dict[str(self.num)] == 5:
            self.radio_btn1.setChecked(True)
        elif self.dict[str(self.num)] == 4:
            self.radio_btn2.setChecked(True)
        elif self.dict[str(self.num)] == 3:
            self.radio_btn3.setChecked(True)
        elif self.dict[str(self.num)] == 2:
            self.radio_btn4.setChecked(True)
        elif self.dict[str(self.num)] == 1:
            self.radio_btn5.setChecked(True)
    
    def no1(self):
        """
        Records the user's selection of the first option for the current question.
        """

        self.dict[str(self.num)] = 5
    
    def no2(self):
        """
        Records the user's selection of the second option for the current question.
        """

        self.dict[str(self.num)] = 4
        
    def no3(self):
        """
        Records the user's selection of the third option for the current question.
        """

        self.dict[str(self.num)] = 3
        
    def no4(self):
        """
        Records the user's selection of the fourth option for the current question.
        """

        self.dict[str(self.num)] = 2
        
    def no5(self):
        """
        Records the user's selection of the fifth option for the current question.
        """

        self.dict[str(self.num)] = 1
            
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
    
    def display_result(self):
        """
        Opens the results window and closes the current stress tracker window.
        """

        sums = self.result()
        self.result_window = Result(self.id_token, sums)
        self.clear_window()
        self.reset_checked()
        self.result_window.show()
        self.close()
    
    def clear_window(self):
        """
        Clears all labels and hides the error group box.
        """

        self.question_label.setText("")
        self.question_no_label.setText("")
        self.error_label.setText("")
        self.group_box.hide()
    
    def main(self):
        """
        Returns to the main menu and closes the current stress tracker window.
        """
        
        from view.menu import MenuWindow
        self.menu_window = MenuWindow(self.id_token)
        self.clear_window()
        self.reset_checked()
        self.menu_window.show()
        self.close()  # Closes Stress tracker window
    