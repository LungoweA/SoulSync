import sys
import os
from PyQt5 import uic
from PyQt5.QtWidgets import (QMainWindow, QPushButton, QLabel)
from PyQt5.QtCore import *
from All_Files.controller.MoodLogic import Mood


# Add the parent directory to the system path to allow module imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))



class Tips(QMainWindow):
    """
    A class representing the Tips window in the application. This window displays supportive messages,
    tips, and motivational quotes based on the user's mood and stress level.

    Attributes:
        id_token (str): The ID token associated with the user's session.
        mood (Mood): An instance of the `Mood` class for handling mood-related logic.
        rate (str): The user's mood rating.
        description (str): The user's mood description.
        influence (str): The factor influencing the user's mood.
        menu_btn (QPushButton): Button to return to the main menu.
        quote_label (QLabel): Label to display a motivational quote.
        owner_label (QLabel): Label to display the author of the motivational quote.
        tips_label (QLabel): Label to display mood-related tips.
        message_label (QLabel): Label to display a supportive message.
    """

    def __init__(self, id_token, rate, description, influence, parent=None):
        """
        Initializes the Tips window and sets up the UI elements and event handlers.

        Args:
            id_token (str): The ID token associated with the user's session.
            rate (str): The user's mood rating.
            description (str): The user's mood description.
            influence (str): The factor influencing the user's mood.
            parent (QWidget, optional): The parent widget. Defaults to None.
        """

        super(Tips, self).__init__(parent)
        uic.loadUi(os.path.join(os.path.dirname(__file__), "UI files", "tips.ui"), self)
        
        self.id_token = id_token
        self.mood = Mood()
        self.rate = rate
        self.description = description
        self.influence = influence
        self.menu_btn = self.findChild(QPushButton, "menu_btn")
        self.quote_label = self.findChild(QLabel, "quote_label")
        self.owner_label = self.findChild(QLabel, "owner_label")
        self.tips_label = self.findChild(QLabel, "tips_label")
        self.message_label = self.findChild(QLabel, "message_label")
        
        self.set_message()
        self.set_tips()
        self.set_quotes()
        self.save_log()
        self.menu_btn.clicked.connect(self.menu)
        
    def set_message(self):
        """
        Displays a supportive message based on the user's mood description.
        """

        mood_message = self.mood.supportive_messages()
        self.message_label.setText(f"{mood_message[self.description]}\nBelow are a few simple tips to bring more joy and brightness to your day!")
        
    def set_tips(self):
        """
        Displays mood-related tips based on the factor influencing the user's mood.
        """

        tip_dict = self.mood.tips()
        mood_tips = tip_dict[self.influence]
        self.tips_label.setText(f"\n 1. {mood_tips[0]}\n\n 2. {mood_tips[1]}\n\n 3. {mood_tips[2]}\n\n 4. {mood_tips[3]}\n\n 5. {mood_tips[4]}")
        
        
    def set_quotes(self):
        """
        Displays a random motivational quote based on the user's mood description.
        """

        import random
        
        quote_dict = self.mood.quotes()
        quotes = quote_dict[self.description]
        name, quote = random.choice(quotes)
        self.quote_label.setText(f'"{quote}"')
        self.owner_label.setText(name)
        
        
    def save_log(self):
        """
        Saves the user's mood data to the database.
        """

        self.mood.mood_score(self.rate, self.description, self.influence)
        self.mood.save_data(self.id_token)
        
    def clear(self):
        """
        Clears all labels in the window.
        """

        self.message_label.setText("")
        self.tips_label.setText("")
        self.quote_label.setText("")
        self.owner_label.setText("")
        
        
    def menu(self):
        """
        Returns to the main menu and closes the current Tips window.
        """
        
        from view.menu import MenuWindow
        self.menu_window = MenuWindow(self.id_token)
        self.clear()
        self.menu_window.show()
        self.close()  # Closes Tips window