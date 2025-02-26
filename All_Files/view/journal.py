import sys
import os
from PyQt5 import uic
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (QMainWindow, QPushButton, QLabel, QTextEdit, QGroupBox)
from PyQt5.QtCore import *
from All_Files.controller.StressLogic import Diary


# Add the parent directory to the system path to allow module imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))



class Journal(QMainWindow):
    
    def __init__(self, id_token,parent=None):
        super(Journal, self).__init__(parent)
        uic.loadUi(os.path.join(os.path.dirname(__file__), "UI files", "journal.ui"), self)
        
        self.id_token = id_token
        self.diary = Diary()
        
        self.clear_btn = self.findChild(QPushButton, "clear_btn")
        self.save_btn = self.findChild(QPushButton, "save_btn")
        self.menu_btn = self.findChild(QPushButton, "menu_btn")
        self.journal_text = self.findChild(QTextEdit, "journal_textedit")
        
        self.error_label = self.findChild(QLabel, "error_label")
        self.group_box = self.findChild(QGroupBox, 'groupBox')
        
        self.group_box.hide()
        self.clear_btn.clicked.connect(self.clear_journal)
        self.save_btn.clicked.connect(self.save_journal)
        self.menu_btn.clicked.connect(self.menu)
        
        
    def clear_journal(self):
        journal_text = self.findChild(QTextEdit)
        if journal_text:
            journal_text.clear()
        
    def save_journal(self):
        entry = self.journal_text.toPlainText()
        if entry != "":
            self.diary.save(self.id_token, entry)
            self.group_box.hide()
        else:
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
            self.error_label.setText("⚠️ Empty journal cannot be saved")
            
    
    def menu(self):
        from .menu import MenuWindow
        self.menu_window = MenuWindow(self.id_token)
        self.clear_journal()
        self.menu_window.show()
        self.close()  # Closes Journal window