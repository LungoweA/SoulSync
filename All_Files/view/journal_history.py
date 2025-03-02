from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QPushButton, QListWidget
import os
from firebase_admin import db, auth
from datetime import datetime
import traceback


class JournalHistory(QMainWindow):
    def __init__(self, user_id):
        super().__init__()
        uic.loadUi(os.path.join(os.path.dirname(__file__), "UI files", "journal_history.ui"), self)

        self.user_id = user_id

        self.back_btn = self.findChild(QPushButton, "back_btn")
        self.journal_list = self.findChild(QListWidget, "journal_list")

        self.back_btn.clicked.connect(self.go_back)

        self.load_journal_entries()

    def load_journal_entries(self):
        """Fetch journal entries from Firebase and display them in QListWidget."""
        try:
            print("Fetching journal entries for the user: ", self.user_id)

            uid = self.user_id
            
            if "." in self.user_id:
                try:
                    decoded_token = auth.verify_id_token(self.user_id)
                    uid = decoded_token.get("uid")
                except Exception as e:
                    print("Invalid ID token: ", str(e))
                    return
            
            print(f"Querying Firebase path: journals/{uid}")  # Debuggining output
            
            ref = db.reference(f"journals/{uid}")
            journals = ref.get()

            print("Data retrieved from Firebase: ", journals)  # Debugging output
            self.journal_list.clear()

            if journals:
                for key, data in journals.items():
                    date = data.get("date", "Unknown Date")

                    if isinstance(date, (int, float)):
                        date = datetime.fromtimestamp(date).strftime("%Y-%m-%d")

                    content = data.get("content", "No content available")
                    snippet = content[:30] + "..." if len(content) > 30 else content                    
                    item_text = f"{date} - {snippet}"

                    self.journal_list.addItem(item_text)
                    print("Journal entries successfully added to UI.")
            else:
                print("No journal entries found for this user.")
                self.journal_list.addItem("No journal entries available.")

        except Exception as e:
            print("Error fetching journal entries: ", e)
            traceback.print_exc()  # Printing full error stack trace

    def go_back(self):
        """Closes Journal History and returns to Menu."""
        from view.menu import MenuWindow
        self.menu_window = MenuWindow(self.user_id)
        self.menu_window.show()
        self.close()
