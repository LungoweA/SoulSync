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
    
    def __init__(self, id_token,parent=None):
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
        if self.num == 5 and self.check_button():
            self.next_btn.hide()
            self.results_btn.show()
            
    def result(self):
        value = list(self.dict.values())
        return sum(value)
            
    def set_checked(self):
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
        self.dict[str(self.num)] = 5
    
    def no2(self):
        self.dict[str(self.num)] = 4
        
    def no3(self):
        self.dict[str(self.num)] = 3
        
    def no4(self):
        self.dict[str(self.num)] = 2
        
    def no5(self):
        self.dict[str(self.num)] = 1
            
    def reset_checked(self):
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
        return self.radio_btn1.isChecked() or self.radio_btn2.isChecked() or self.radio_btn3.isChecked() or self.radio_btn4.isChecked() or self.radio_btn5.isChecked()
    
    def display_result(self):
        sums = self.result()
        self.result_window = Result(self.id_token, sums)
        self.clear_window()
        self.reset_checked()
        self.result_window.show()
        self.close()
    
    def clear_window(self):
        self.question_label.setText("")
        self.question_no_label.setText("")
        self.error_label.setText("")
        self.group_box.hide()
    
    def main(self):
        from view.menu import MenuWindow
        self.menu_window = MenuWindow(self.id_token)
        self.clear_window()
        self.reset_checked()
        self.menu_window.show()
        self.close()  # Closes Stress tracker window