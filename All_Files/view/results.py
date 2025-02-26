import sys
import os
from PyQt5 import uic
from PyQt5.QtWidgets import (QMainWindow, QPushButton, QLabel)
from PyQt5.QtCore import *
from All_Files.controller.StressLogic import Stress


# Add the parent directory to the system path to allow module imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))



class Result(QMainWindow):
    """
    A class representing the Results window in the application. This window displays the user's stress level,
    along with tips, exercises, and motivational quotes tailored to their stress level.

    Attributes:
        id_token (str): The ID token associated with the user's session.
        stress (Stress): An instance of the `Stress` class for handling stress-related logic.
        sums (int): The sum of the user's stress test responses.
        result_label (QLabel): Label to display the stress level result.
        exercise_label (QLabel): Label to display recommended exercises.
        tips_label (QLabel): Label to display stress management tips.
        quote_label (QLabel): Label to display a motivational quote.
        owner_label (QLabel): Label to display the author of the motivational quote.
        menu_btn (QPushButton): Button to return to the main menu.
    """

    def __init__(self, id_token, sums, parent=None):
        """
        Initializes the Results window and sets up the UI elements and event handlers.

        Args:
            id_token (str): The ID token associated with the user's session.
            sums (int): The sum of the user's stress test responses.
            parent (QWidget, optional): The parent widget. Defaults to None.
        """

        super(Result, self).__init__(parent)
        uic.loadUi(os.path.join(os.path.dirname(__file__), "UI files", "results.ui"), self)
        
        self.id_token = id_token
        self.stress = Stress()
        self.sums = sums
        
        self.result_label = self.findChild(QLabel, "result_label")
        self.exercise_label = self.findChild(QLabel, "exercise_label")
        self.tips_label = self.findChild(QLabel, "tips_label")
        self.quote_label = self.findChild(QLabel, "quote_label")
        self.owner_label = self.findChild(QLabel, "owner_label")
        
        self.menu_btn = self.findChild(QPushButton, "menu_btn")
        self.show_result()
        self.show_tips()
        self.show_exercises()
        self.show_quotes()
        self.menu_btn.clicked.connect(self.menu)
        
    
    def show_result(self):
        """
        Displays the user's stress level result and saves it to the database.
        """

        self.result = self.stress.result(self.sums)
        if self.result == "Low":
            self.result_label.setText(f"Your Stress Level: {self.result}\nYou're doing great! Keep up the healthy habits to maintain balance.\nThere are tips and recommended exercises below to help keep you on track.")
        elif self.result == "Moderate":
            self.result_label.setText(f"Your Stress Level: {self.result}\nYou're feeling some stress—let’s take small steps to unwind and recharge. \nBelow are some tips and recommended exercises to help you relieve your stress.")
        elif self.result == "High":
            self.result_label.setText(f"Your Stress Level: {self.result}\nYour stress level is high. It’s time to pause, breathe, and focus on self-care.\nBelow are some tips and recommended exercises to help you ease your stress.")
        
        self.stress.save_data(self.id_token, self.result)   # Save stress level
            
            
    def show_tips(self):
        """
        Displays stress management tips tailored to the user's stress level.
        """

        tips = self.stress.tips()
        if self.result == "Low":
            self.tips_label.setText(f" \n {1}. {tips['Low'][0]}\n\n {2}. {tips['Low'][1]}\n\n {3}. {tips['Low'][2]}\n\n {4}. {tips['Low'][3]}\n\n {5}. {tips['Low'][4]}")
        elif self.result == "Moderate":
            self.tips_label.setText(f" \n {1}. {tips['Moderate'][0]}\n\n {2}. {tips['Moderate'][1]}\n\n {3}. {tips['Moderate'][2]}\n\n {4}. {tips['Moderate'][3]}\n\n {5}. {tips['Moderate'][4]}")
        elif self.result == "High":
            self.tips_label.setText(f" \n {1}. {tips['High'][0]}\n\n {2}. {tips['High'][1]}\n\n {3}. {tips['High'][2]}\n\n {4}. {tips['High'][3]}\n\n {5}. {tips['High'][4]}")
                
            
    def show_exercises(self):
        """
        Displays recommended exercises tailored to the user's stress level.
        """

        exercises = self.stress.exercises()
        if self.result == "Low":
            self.exercise_label.setText(f"\n {1}. {exercises['Low'][0]}\n\n {2}. {exercises['Low'][1]}\n\n {3}. {exercises['Low'][2]}\n\n {4}. {exercises['Low'][3]}\n\n {5}. {exercises['Low'][4]}")
        elif self.result == "Moderate":
            self.exercise_label.setText(f"\n {1}. {exercises['Moderate'][0]}\n\n {2}. {exercises['Moderate'][1]}\n\n {3}. {exercises['Moderate'][2]}\n\n {4}. {exercises['Moderate'][3]}\n\n {5}. {exercises['Moderate'][4]}")
        elif self.result == "High":
            self.exercise_label.setText(f"\n{ 1}. {exercises['High'][0]}\n\n {2}. {exercises['High'][1]}\n\n {3}. {exercises['High'][2]}\n\n {4}. {exercises['High'][3]}\n\n {5}. {exercises['High'][4]}")
                
        
    def show_quotes(self):
        """
        Displays a random motivational quote tailored to the user's stress level.
        """

        import random
        
        quotes = self.stress.quotes()
        if self.result == "Low":
            owner1, quote1 = random.choice(quotes['Low'])
            self.quote_label.setText(f'"{quote1}"')
            self.owner_label.setText(f'{owner1}')
        elif self.result == "Moderate":
            owner2, quote2 = random.choice(quotes['Moderate'])
            self.quote_label.setText(f'"{quote2}"')
            self.owner_label.setText(f'{owner2}')
        elif self.result == "High":
            owner3, quote3 = random.choice(quotes['High'])
            self.quote_label.setText(f'"{quote3}"')
            self.owner_label.setText(f'{owner3}')
            
    def clear(self):
        """
        Clears all labels in the window.
        """

        self.result_label.setText("")
        self.exercise_label.setText("")
        self.tips_label.setText("")
        self.quote_label.setText("")
        self.owner_label.setText("")
        
        
    def menu(self):
        """
        Returns to the main menu and closes the current Results window.
        """
        
        from view.menu import MenuWindow
        self.menu_window = MenuWindow(self.id_token)
        self.clear()
        self.menu_window.show()
        self.close()  # Closes Result window