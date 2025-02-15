from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow
import os


class MenuWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(os.path.join(os.path.dirname(__file__), "UI files", "menu.ui"), self)
