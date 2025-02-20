import sys
import os
from PyQt5 import uic
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (QMainWindow, QLabel)

# Add the parent directory to the system path to allow module imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


# You can delete the code and write your own, It is just here to show that the user can login into his account

class Window(QMainWindow):
    
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        uic.loadUi(os.path.join(os.path.dirname(__file__), "UI files", "Main_Window.ui"), self)
        
        self.label = self.findChild(QLabel, "label")
