import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class MoodStressHistory(QMainWindow):
    def __init__(self, id_token, parent=None):
        super().__init__(parent)
        uic.loadUi(os.path.join(os.path.dirname(__file__), "UI files", "mood_stress_history.ui"), self)
    
        self.id_token = id_token

        #Accessing widgets
        self.MoodStressHistory = self.findChild(QTableWidget, "history_tableWidget")
      
        self.btn_menu = self.findChild(QPushButton, "btn_menu")

        #Actions
        self.btn_menu.clicked.connect(self.menu)
        self.load_history()
        
        # Ensure the table fills the available space in the widget
        self.MoodStressHistory.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.MoodStressHistory.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  
        self.MoodStressHistory.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)  
    
    def menu(self):
        """
        Returns to the main menu
        """
        from view.menu import MenuWindow
        self.menu_window = MenuWindow(self.id_token)
        self.menu_window.show()
        self.close()  

    def load_history(self):
        """
        Loads mood and stress history from the database and displays it in the table widget.
        """
        from controller.MoodLogic import Mood
        from controller.StressLogic import Stress

        # Create instances of the controller classes
        mood = Mood()
        stress = Stress()

        # Fetch mood and stress data using the id_token
        mood_data = mood.fetch_mood_history(self.id_token)
        stress_data = stress.fetch_stress_history(self.id_token)

        # Combine both datasets for display
        combined_data = []
        for item in mood_data:
            combined_data.append({
                "Created on": item["Created_at"],
                "Type": "Mood",
                "Rating": item["Mood Rating"],
                "Description": item["Description"],
                "Influence": item["Influence"]
            })
        for item in stress_data:
            combined_data.append({
                "Created_at": item["Created_at"],
                "Type": "Stress",
                "Rating": item["Stress Level"],
                "Description": "N/A",
                "Influence": "N/A"
            })

        # Populate the table widget
        self.populate_table(self.MoodStressHistory, combined_data)

    def populate_table(self, table_widget, data):
        """
        Populates the table widget with data.

        Args:
            table_widget (QTableWidget): The table widget to populate.
            data (list): A list of dictionaries containing the data to display.
        """
        table_widget.setRowCount(len(data))
        table_widget.setColumnCount(len(data[0]))

        # Set table headers
        table_widget.setHorizontalHeaderLabels(data[0].keys())

        for row, record in enumerate(data):
            for col, (key, value) in enumerate(record.items()):
                table_widget.setItem(row, col, QTableWidgetItem(str(value)))

        # Automatically resize columns and rows to fit content
        table_widget.resizeColumnsToContents()
        table_widget.resizeRowsToContents()