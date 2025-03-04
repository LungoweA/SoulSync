from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QPushButton, QListWidget
import os
from firebase_admin import db, auth
from datetime import datetime
import traceback

from All_Files.controller.JournalLogic import Diary



class JournalHistory(QMainWindow):
    def __init__(self, user_id):
        super().__init__()
        uic.loadUi(os.path.join(os.path.dirname(__file__), "UI files", "journal_history.ui"), self)

        self.user_id = user_id
        self.journal_controller = Diary()  # Initialize the journal controller here

        self.back_btn = self.findChild(QPushButton, "back_btn")
        self.journal_list = self.findChild(QListWidget, "journal_list")

        self.back_btn.clicked.connect(self.go_back)

        self.load_journal_entries()


    def go_back(self):
        """Closes Journal History and returns to Menu."""
        from view.menu import MenuWindow
        self.menu_window = MenuWindow(self.user_id)
        self.menu_window.show()
        self.close()



    def load_journal_entries(self):      
        
        try:
            journals = self.journal_controller.fetch_journal_history(self.user_id)

            self.journal_list.clear()

            if journals:
                for entry in journals:
                    date = entry["Created_at"]
                    content = entry["Entry"]
                    snippet = content[:30] + "..." if len(content) > 30 else content
                    item_text = f"{date} - {snippet}"

                    self.journal_list.addItem(item_text)
            else:
                self.journal_list.addItem("No journal entries available.")
        except Exception as e:
            print(f"Error loading journal entries: {e}")
        
        
    
           

    
