import sys
import os

# Add the absolute path of the SoulSync directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from PyQt5.QtWidgets import QApplication
from view.login import LogIn
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Add the parent directory to the system path to allow module imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))



def main():
    """Entry point of the application, initializing the login window."""

    app = QApplication(sys.argv)
    window = LogIn()

    app.exec_()


if __name__ == '__main__':
    main()
