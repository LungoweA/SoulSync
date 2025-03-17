import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from datetime import datetime
from controller.AccountLogic import AccountDetails

class MoodStressHistory(QMainWindow):
    
    """
    A window displaying mood and stress history for a user, allowing them to view past entries.

    Attributes:
        id_token (str): The ID token for the user's session.
        uid (str): The user's ID.
        user_details (AccountDetails): Instance for accessing user details and history.
        mood_stress_list (QListWidget): List widget to display available mood and stress dates.
        title_label, description_label, influence_label, rate_label, stress_label (QLabel): Labels for displaying mood and stress details.
        menu_btn, back_btn (QPushButton): Buttons for navigation.
        stackedWidget (QStackedWidget): Stack widget for displaying different sections (main menu or history).
    """
    
    def __init__(self, uid, id_token, parent=None):
        """
        Initializes the MoodStressHistory window and sets up the UI elements and event handlers.

        Args:
            uid (str): User ID for the current session.
            id_token (str): The ID token for the user's session.
            parent (QWidget, optional): The parent widget. Defaults to None.
        """
        
        super().__init__(parent)
        uic.loadUi(os.path.join(os.path.dirname(__file__), "UI files", "mood_stress_history.ui"), self)
    
        self.id_token = id_token
        self.uid = uid
        
        self.user_details = AccountDetails(self.uid, self.id_token)
        
        #Accessing widgets
        self.mood_stress_list = self.findChild(QListWidget, "listWidget")
        self.title_label = self.findChild(QLabel, "title_label")
        self.description_label = self.findChild(QLabel, "description_label")
        self.influence_label = self.findChild(QLabel, "influence_label")
        self.rate_label = self.findChild(QLabel, "rate_label")
        self.stress_label = self.findChild(QLabel, "stress_label")
        self.menu_btn = self.findChild(QPushButton, "btn_menu")
        self.back_btn = self.findChild(QPushButton, "back_btn")
        self.delete_btn = self.findChild(QPushButton, "delete_btn")
        
        self.stackedWidget = self.findChild(QStackedWidget, "stackedWidget")
        self.stackedWidget.setCurrentIndex(1)
        
        self.menu_btn.clicked.connect(self.menu)
        self.back_btn.clicked.connect(self.show_main_menu)
        self.delete_btn.clicked.connect(self.delete_history)
        self.display_dates()
        self.mood_stress_list.itemClicked.connect(self.show_history)
        
        
        
    def show_main_menu(self):
        """Switches to the main menu view."""
        
        self.stackedWidget.setCurrentIndex(1)
        

    def show_history(self, clicked_item):
        """Displays the mood and stress history for the selected date."""
        
        self.stackedWidget.setCurrentIndex(0)
        self.display_history(clicked_item)
        
        
    def display_dates(self):
        """Displays all available mood and stress dates in the list."""
        
        self.dates = self.user_details.get_mood_stress_dates()
        if self.dates != []:
            for i in self.dates:
                self.mood_stress_list.addItem(f'•  {i}')
        else:
            self.mood_stress_list.addItem('No mood and stress history available')
        
        
    def display_history(self, clicked_item):
        """Displays detailed history for the selected date."""
        msg = 'No mood and stress history available'
        self.mood_history_dict = self.user_details.read_mood_level()
        self.stress_history_dict = self.user_details.read_stress_level()
        string = clicked_item.text() # Retrieving the date that was clicked
        if string != msg:
            self.date = string.split('  ')[1]
        
        # display formatted date
            self.format_date(self.date)
        
        # Display mood and stress history
            self.mood_and_stress(self.date)
        else:
            self.show_main_menu()
        
        
    def format_date(self, date):
        """Formats the date to a more readable format."""
        
        date_obj = datetime.strptime(date, "%Y-%m-%d")
        formatted_date = date_obj.strftime("%A %d %Y")
        self.title_label.setText(formatted_date)
        
        
    def mood_and_stress(self, date):
        """Displays mood and stress history for the selected date."""
        
        if date in self.mood_history_dict:
            self.description_label.setText(self.mood_history_dict[date][0])
            self.influence_label.setText(self.mood_history_dict[date][1])
            self.rate_label.setText(self.mood_history_dict[date][2])
        else:
            self.influence_label.setText("No mood history available.")
        
        if date in self.stress_history_dict:
            self.stress_label.setText(self.stress_history_dict[date])
        else:
            self.stress_label.setText("No stress history available.")
            
            
    def delete_history(self):
        """
        Deletes the selected mood and stress history.

        Prompts the user for confirmation before deleting mood and stress data for the 
        selected date. If successful, it displays a confirmation message, refreshes 
        the journal list, and returns to the main menu. If an error occurs, an 
        error message is shown.
        """
        
        reply = QMessageBox.question(
            self, "Delete History",
            "Are you sure you want to delete this mood and stress history?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            stress_success, message = self.user_details.delete_stress_level(self.date)
            mood_success, message = self.user_details.delete_mood_level(self.date)
            
            if stress_success or mood_success:
                result = QMessageBox.information(self, "Delete History", "Mood and stress history deleted", QMessageBox.Ok)

                if result == QMessageBox.Ok:
                    self.mood_stress_list.clear()
                    self.display_dates()
                    self.show_main_menu()
            else:
                result = QMessageBox.information(self, "Delete History", "Unknown error occurred", QMessageBox.Ok)

                if result == QMessageBox.Ok:
                    self.mood_stress_list.clear()
                    self.display_dates()
                    self.show_main_menu()
                    
                    
    def clear(self):
        """Clears the displayed history information."""
        self.description_label.setText("")
        self.influence_label.setText("")
        self.rate_label.setText("")
        self.stress_label.setText("")
        
    def menu(self):
        """
        Returns to the main menu
        """
        from view.menu import MenuWindow
        self.menu_window = MenuWindow(self.uid, self.id_token)
        self.clear()
        self.menu_window.show()
        self.close()