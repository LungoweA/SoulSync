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
    
    def __init__(self, id_token, rate, description, influence, parent=None):
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
        mood_message = self.mood.supportive_messages()
        self.message_label.setText(f"{mood_message[self.description]}\nBelow are a few simple tips to bring more joy and brightness to your day!")
        
    def set_tips(self):
        tip_dict = self.mood.tips()
        mood_tips = tip_dict[self.influence]
        self.tips_label.setText(f"\n 1. {mood_tips[0]}\n\n 2. {mood_tips[1]}\n\n 3. {mood_tips[2]}\n\n 4. {mood_tips[3]}\n\n 5. {mood_tips[4]}")
        
        
    def set_quotes(self):
        import random
        
        quote_dict = self.mood.quotes()
        quotes = quote_dict[self.description]
        name, quote = random.choice(quotes)
        self.quote_label.setText(f'"{quote}"')
        self.owner_label.setText(name)
        
        
    def save_log(self):
        self.mood.mood_score(self.rate, self.description, self.influence)
        self.mood.save_data(self.id_token)
        
    def clear(self):
        self.message_label.setText("")
        self.tips_label.setText("")
        self.quote_label.setText("")
        self.owner_label.setText("")
        
        
    def menu(self):
        from view.menu import MenuWindow
        self.menu_window = MenuWindow(self.id_token)
        self.clear()
        self.menu_window.show()
        self.close()  # Closes Tips window