from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QStringListModel
import os
from datetime import datetime
from controller.AccountLogic import AccountDetails

class JournalHistory(QMainWindow):
    """
    A class representing the Journal History window in the application. This window allows users
    to view a history of their journal entries. The user can navigate through journal entries by 
    date and time, as well as view the content of each entry.

    Attributes:
        user_id (str): The unique ID of the user.
        id_token (str): The session token of the user.
        num (int): The current entry index for navigating through the journal entries.
        user_details (AccountDetails): An instance of the AccountDetails class for retrieving user data.
        back_btn (QPushButton): Button to go back to the previous screen.
        prev_btn (QPushButton): Button to view the previous journal entry.
        next_btn (QPushButton): Button to view the next journal entry.
        menu_btn (QPushButton): Button to navigate back to the menu screen.
        journal_list (QListWidget): List widget to display available journal dates.
        title_label (QLabel): Label to display the title of the journal entry (date and time).
        journal_view (QLabel): Label to display the content of the journal entry.
        stackedWidget (QStackedWidget): A stacked widget to handle different views (main menu and journal entries).
    """


    def __init__(self, uid, id_token):
        """
        Initializes the JournalHistory window and sets up the UI elements and event handlers.

        Args:
            uid (str): The unique ID of the user.
            id_token (str): The session token of the user.
        """
        
        super().__init__()
        uic.loadUi(os.path.join(os.path.dirname(__file__), "UI files", "journal_history.ui"), self)

        self.user_id = uid
        self.id_token = id_token
        self.num = 0
        self.user_details = AccountDetails(self.user_id, self.id_token)
        self.back_btn = self.findChild(QPushButton, "back_btn")
        self.prev_btn = self.findChild(QPushButton, "prev_btn")
        self.next_btn = self.findChild(QPushButton, "next_btn")
        self.menu_btn = self.findChild(QPushButton, "menu_btn")
        self.journal_list = self.findChild(QListWidget, "journal_list")
        self.title_label = self.findChild(QLabel, "title_label")
        self.journal_view = self.findChild(QLabel, "journal_view")
        
        self.stackedWidget = self.findChild(QStackedWidget, "stackedWidget")
        self.stackedWidget.setCurrentIndex(1)
        
        self.menu_btn.clicked.connect(self.menu)
        self.back_btn.clicked.connect(self.show_main_menu)
        self.prev_btn.clicked.connect(self.previous)
        self.next_btn.clicked.connect(self.next)
        
        self.display_dates()
        self.journal_list.itemClicked.connect(self.show_history)
    


    def show_main_menu(self):
        """
        Switches the view back to the main menu screen.
        """
        
        self.stackedWidget.setCurrentIndex(1)
        

    def show_history(self, clicked_item):
        """
        Displays the journal entry history for the selected date.

        Args:
            clicked_item (QListWidgetItem): The item clicked in the journal date list.
        """
        
        self.stackedWidget.setCurrentIndex(0)
        self.display_history(clicked_item)
    
    def display_dates(self):
        """
        Retrieves and displays a list of dates for the user's journal entries.
        """
        
        self.dates = self.user_details.get_journal_dates()
        if self.dates != []:
            for i in self.dates:
                self.journal_list.addItem(f'•  {i}')
        else:
            self.journal_list.addItem('No journal history available')
        
            
    
    def display_history(self, clicked_item):
        """
        Displays the journal entry for the selected date, and retrieves the associated journal data.

        Args:
            clicked_item (QListWidgetItem): The item clicked in the journal date list.
        """
        
        self.journal_dict = self.user_details.read_journal()
        string = clicked_item.text()       # Retrieving the date that was clicked
        self.date = string.split('  ')[1]
        self.num = 0
        self.journal()
        
    
    
    def journal(self):
        """
        Displays the current journal entry, including the formatted date, time, and the journal content.
        If there are multiple entries for the date, the user can navigate through them using the 'previous' and 'next' buttons.
        """
        
        self.entry_list = self.journal_dict[self.date]
        time, entry = self.entry_list[0]
        formatted_date = self.format_date(self.date)
        formatted_time = self.format_time(time)
        self.title_label.setText(f'{formatted_date}\n{formatted_time}')
        
        self.journal_view.setText(entry)
        self.prev_btn.hide()
        self.next_btn.show()
        
        
    def format_date(self, date):
        """
        Formats the date string into a human-readable format.

        Args:
            date (str): The date to be formatted.
        
        Returns:
            str: The formatted date in "Day, DD Month YYYY" format.
        """
        
        date_obj = datetime.strptime(date, "%Y-%m-%d")
        formatted_date = date_obj.strftime("%A %d %Y")
        return formatted_date
        
        
    def format_time(self, time):
        """
        Formats the time string into a 12-hour format.

        Args:
            time (str): The time to be formatted in "HH:MM:SS" format.

        Returns:
            str: The formatted time in "HH:MM AM/PM" format.
        """
        
        formatted_time = datetime.strptime(time, '%H:%M:%S').strftime('%I:%M %p')
        return formatted_time
    
    
    def previous(self):
        """
        Navigates to the previous journal entry. If at the first entry, hides the 'previous' button.
        """
        
        if self.num > 0:
            self.num -= 1
            time, entry = self.entry_list[self.num]
            formatted_date = self.format_date(self.date)
            formatted_time = self.format_time(time)
            self.title_label.setText(f'{formatted_date}\n{formatted_time}')
            self.journal_view.setText(entry)
            self.next_btn.show()
            
            if self.num == 0:
                self.prev_btn.hide()
            
            
    def next(self):
        """
        Navigates to the next journal entry. If at the last entry, hides the 'next' button.
        """
        
        if self.num < len(self.entry_list)-1:
            self.num += 1
            time, entry = self.entry_list[self.num]
            formatted_date = self.format_date(self.date)
            formatted_time = self.format_time(time)
            self.title_label.setText(f'{formatted_date}\n{formatted_time}')
            self.journal_view.setText(entry)
            self.prev_btn.show()
            
            if self.num == len(self.entry_list)-1:
                self.next_btn.hide()
    
    
    def menu(self):
        """
        Opens the main menu window and closes the current journal history window.
        """
        
        from view.menu import MenuWindow
        self.menu_window = MenuWindow(self.user_id, self.id_token)
        self.menu_window.show()
        self.close()



    