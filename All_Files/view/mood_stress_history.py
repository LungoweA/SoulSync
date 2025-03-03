import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QPushButton, QTableWidget
from PyQt5.QtCore import *

class MoodStressHistory(QMainWindow):
    def __init__(self, id_token, parent=None):
        super().__init__(parent)
        uic.loadUi(os.path.join(os.path.dirname(__file__), "UI files", "mood_stress_history.ui"), self)
    
        self.id_token = id_token

        #Accessing widgets
        self.MoodStressHistory = self.findChild(QTableWidget, "MoodStressHistory")
      
        self.btn_menu = self.findChild(QPushButton, "btn_menu")

        #Actions
        self.btn_menu.clicked.connect(self.menu)
        
    
    def menu(self):
        """
        Returns to the main menu
        """
        from view.menu import MenuWindow
        self.menu_window = MenuWindow(self.id_token)
        self.menu_window.show()
        self.close()  
