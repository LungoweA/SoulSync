from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QPushButton
import os
from All_Files.controller.AccountLogic import AccountCreation


class MenuWindow(QMainWindow):
    """
    The main menu window that allows the user to navigate to different features of the application.
    It provides options for mood tracking, stress tracking, journaling, viewing history, and settings.

    Attributes:
        id_token (str): The ID token for the user's session.
        uid (str): The user's ID.
        mood_tracker_pushbutton (QPushButton): Button to open the mood tracker.
        stress_tracker_pushbutton (QPushButton): Button to open the stress tracker.
        diary_pushbutton (QPushButton): Button to open the journal.
        stress_history_btn (QPushButton): Button to open the mood and stress history.
        journal_history_btn (QPushButton): Button to open the journal history.
        settings_btn (QPushButton): Button to open the settings window.
        logout_btn (QPushButton): Button to log out the user.
    """
    
    def __init__(self, uid, id_token):
        """
        Initializes the MenuWindow and sets up UI elements and event handlers.

        Args:
            uid (str): The user ID for the current session.
            id_token (str): The ID token for the user's session.
        """
        
        super().__init__()
        self.id_token = id_token
        self.uid = uid
        uic.loadUi(os.path.join(os.path.dirname(__file__), "UI files", "menu.ui"), self)

        self.mood_tracker_pushbutton = self.findChild(QPushButton, "mood_tracker_pushbutton")
        self.stress_tracker_pushbutton = self.findChild(QPushButton, "stress_tracker_pushbutton")
        self.diary_pushbutton = self.findChild(QPushButton, "diary_pushbutton")
        self.stress_history_btn = self.findChild(QPushButton, "stress_history_btn")
        self.journal_history_btn = self.findChild(QPushButton, "journal_history_btn")
        self.settings_btn = self.findChild(QPushButton, "settings_btn")
        self.logout_btn = self.findChild(QPushButton, "logout_btn")
        self.journal_history_btn = self.findChild(QPushButton, "journal_history_btn")
        self.settings_btn = self.findChild(QPushButton, "settings_btn")

        self.mood_tracker_pushbutton.clicked.connect(self.open_mood_tracker)
        self.stress_tracker_pushbutton.clicked.connect(self.open_stress_tracker)
        self.diary_pushbutton.clicked.connect(self.open_journal)
        self.logout_btn.clicked.connect(self.handle_logout)
        self.journal_history_btn.clicked.connect(self.open_journal_history)
        self.settings_btn.clicked.connect(self.open_settings)
        self.stress_history_btn.clicked.connect(self.open_mood_stress_history)

    def handle_logout(self):
        """Handles the logout process and redirects the user to the login screen."""
        
        from All_Files.view.login import LogIn
        account = AccountCreation()
        success = account.log_out()

        if success:
            self.close()
            self.login_window = LogIn()
            self.login_window.show()


    def open_mood_tracker(self):
        """Opens the Mood Tracker window."""
        
        from All_Files.view.mood_tracker import MoodTrackerWindow
        self.mood_window = MoodTrackerWindow(self.uid, self.id_token)
        self.mood_window.resize(self.size())
        self.mood_window.show()
        self.close()

    def open_stress_tracker(self):
        """Opens the Stress Tracker window."""
        
        from All_Files.view.stress_tracker import StressTracker
        self.stress_window = StressTracker(self.uid, self.id_token)
        self.stress_window.resize(self.size())
        self.stress_window.show()
        self.close()

    def open_journal(self):
        """Opens the Journal window."""
        
        from All_Files.view.journal import Journal
        self.journal_window = Journal(self.uid, self.id_token)
        self.journal_window.resize(self.size())
        self.journal_window.show()
        self.close()

    def open_journal_history(self):
        """Opens the Journal History window."""
        from All_Files.view.journal_history import JournalHistory
        self.journal_history_window = JournalHistory(self.uid, self.id_token)
        self.journal_history_window.show()
        self.close()

    def open_settings(self):
        """Open the Settings window and pass the id_token"""
        from All_Files.view.settings import SettingsWindow
        self.settings_window = SettingsWindow(self.uid, self.id_token)
        self.settings_window.show()
        self.close()

    def open_mood_stress_history(self):
        """Opens the Mood and Stress History window."""
        
        from All_Files.view.mood_stress_history import MoodStressHistory
        self.mood_stress_history_window = MoodStressHistory(self.uid, self.id_token)
        self.mood_stress_history_window.resize(self.size())
        self.mood_stress_history_window.show()
        self.close()