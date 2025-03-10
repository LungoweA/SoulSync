import sys
import os
from PyQt5 import uic
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (QMainWindow, QPushButton, QLabel, QTextEdit, QGroupBox, QMessageBox)
from PyQt5.QtCore import *
from controller.JournalLogic import Diary


# Add the parent directory to the system path to allow module imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))



class Journal(QMainWindow):
    """
    A class representing the Journal window in the application. This window allows users to write,
    save, and clear journal entries. It also provides navigation back to the main menu.

    Attributes:
        id_token (str): The ID token associated with the user's session.
        diary (Diary): An instance of the `Diary` class for saving journal entries.
        clear_btn (QPushButton): Button to clear the journal text.
        save_btn (QPushButton): Button to save the journal entry.
        menu_btn (QPushButton): Button to navigate back to the main menu.
        journal_text (QTextEdit): Text area for writing journal entries.
        error_label (QLabel): Label to display error messages.
        group_box (QGroupBox): Group box to display error messages.
    """

    def __init__(self, uid, id_token,parent=None):
        """
        Initializes the Journal window.

        Args:
            id_token (str): The ID token associated with the user's session.
            parent (QWidget, optional): The parent widget. Defaults to None.
        """

        super(Journal, self).__init__(parent)
        uic.loadUi(os.path.join(os.path.dirname(__file__), "UI files", "journal.ui"), self)
        
        self.id_token = id_token
        self.uid = uid
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
        """
        Clears the text in the journal text area.
        """

        journal_text = self.findChild(QTextEdit)
        if journal_text:
            journal_text.clear()
        
    def save_journal(self):
        """
        Saves the journal entry to the database if it is not empty. Displays an error message
        if the journal entry is empty.
        """

        entry = self.journal_text.toPlainText()
        if entry != "":
            self.diary.save(self.id_token, entry)
            self.group_box.hide()
            reply = QMessageBox.question(
            self, "Saved Journal",
            "Your journal has been saved. Do you want to go back to the main menu?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

            if reply == QMessageBox.Yes:
                self.menu()
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
        """
        Navigates back to the main menu window. Clears the journal text and closes the current window.
        """
        
        from .menu import MenuWindow
        self.menu_window = MenuWindow(self.uid, self.id_token)
        self.clear_journal()
        self.menu_window.show()
        self.close()  # Closes Journal window