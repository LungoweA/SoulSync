import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
                            QPushButton, QCheckBox, QRadioButton, QButtonGroup, QLineEdit)
from PyQt5.QtGui import QIcon, QFont, QPixmap
from PyQt5.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self,):
        super().__init__()
        self.setWindowTitle("Soul Sync")
        self.setGeometry(0,0, 400, 400)
        self.setWindowIcon(QIcon('_4c8c539e-4f40-41e8-ba07-ab979aa0f9e3.jpeg'))
        self.checkbox = QCheckBox('Do you like anime?', self)
        '''self.button_group1 = QButtonGroup(self)
        self.button_group2 = QButtonGroup(self)
        self.radio1 = QRadioButton('Visa', self)
        self.radio2 = QRadioButton('Master Card', self)
        self.radio3 = QRadioButton('Gift Card', self)
        self.radio4 = QRadioButton('In Store', self)
        self.radio5 = QRadioButton('Online', self)'''
        
        '''self.label = QLabel('Hey Jane!', self)
        self.button = QPushButton('click me', self)'''
        '''self.line_edit = QLineEdit(self)
        self.push_button = QPushButton('Submit', self)'''
        
        self.button1 = QPushButton('#1')
        self.button2 = QPushButton('#2')
        self.button3 = QPushButton('#3')
        
        self.initUI()
        
        # Adding labels
        '''lab = QLabel('Hello', self)
        lab.setFont(QFont('Arial', 50))
        lab.setGeometry(50, 200, 300, 200)
        lab.setStyleSheet('color: black;'
                            'background-color: green;'
                            'font-weight: bold;'
                            'font-style: italic;'
                            'text-decoration: underline;')
        # label.setAlignment(Qt.AlignTop) # Align Vertically Top
        # label.setAlignment(Qt.AlignBottom) # Align Vertically Bottom
        #label.setAlignment(Qt.AlignVCenter) # Align Vertically Center
        
        #label.setAlignment(Qt.AlignRight) # Align Horizontally Right
        #label.setAlignment(Qt.AlignLeft) # Align Horizontally Left
        #label.setAlignment(Qt.AlignHCenter) # Align Horizontally Center
        
        # To align horizontally and vertically, use the | operator
        # label.setAlignment(Qt.AlignHCenter | Qt.AlignTop) # Horinzontally Center and Vertically Top
        lab.setAlignment(Qt.AlignCenter) # Will Align both Horizontally and Vertically Center
        
        # Adding images
        label = QLabel(self)
        label.setGeometry(0, 0, 200, 200)
        pixmap = QPixmap('_c5dca270-092d-4483-b12e-a031080d7df9.jpeg')
        label.setPixmap(pixmap)
        # For the image to scale to the size of the label
        label.setScaledContents(True)
        
        label.setGeometry((self.width()-label.width()) // 2, 0, label.width(), label.height())'''
        
    
    def initUI(self):
        # This is to set layout
        '''central_widget = QWidget()
        self.setCentralWidget(central_widget)
            
        label1 = QLabel("Apple", self)
        label2 = QLabel('Banana', self)
        label3 = QLabel('Blueberry', self)
        label4 = QLabel('Cherry', self)
        label5 = QLabel('Grape', self)
        label6 = QLabel('Orange', self)
        
        label1.setStyleSheet('background-color: green;')
        label2.setStyleSheet('background-color: yellow;')
        label3.setStyleSheet('background-color: blue;')
        label4.setStyleSheet('background-color: red;')
        label5.setStyleSheet('background-color: purple;')
        label6.setStyleSheet('background-color: orange;')
        
        # Vertical layout
        vbox = QVBoxLayout()
        vbox.addWidget(label1)
        vbox.addWidget(label2)
        vbox.addWidget(label3)
        vbox.addWidget(label4)
        vbox.addWidget(label5)
        vbox.addWidget(label6)
        
        central_widget.setLayout(vbox)
        
        # Horizontal Layout
        hbox = QHBoxLayout()
        hbox.addWidget(label1)
        hbox.addWidget(label2)
        hbox.addWidget(label3)
        hbox.addWidget(label4)
        hbox.addWidget(label5)
        hbox.addWidget(label6)
        
        central_widget.setLayout(hbox)
        
        # Grid Layout
        grid = QGridLayout()
        grid.addWidget(label1, 0, 0)
        grid.addWidget(label2, 0, 1)
        grid.addWidget(label3, 0, 2)
        grid.addWidget(label4, 1, 0)
        grid.addWidget(label5, 1, 1)
        grid.addWidget(label6, 1, 2)
        
        central_widget.setLayout(grid)'''
        
        # Using check boxes
        self.checkbox.setGeometry(10, 0, 250, 50)
        self.checkbox.setStyleSheet("font-size : 20px;"
                                    "font-family : Times;")
        
        self.checkbox.setChecked(False)
        self.checkbox.stateChanged.connect(self.checkbox_changed)
        
        # Using push buttons
        '''self.button.setGeometry(100, 150, 200, 50)
        self.button.setStyleSheet('font-size : 30px;')
        self.button.clicked.connect(self.on_click)
        
        self.label.setGeometry(100, 100, 200, 50)
        self.label.setStyleSheet('font-size : 30px;')'''
    
        # Using radio buttons
        '''self.radio1.setGeometry(10, 0, 200, 40)
        self.radio2.setGeometry(10, 30, 200, 40)
        self.radio3.setGeometry(10, 60, 200, 40)
        self.radio4.setGeometry(10, 100, 200, 40)
        self.radio5.setGeometry(10, 130, 200, 40)
        
        self.setStyleSheet('QRadioButton{'
                            "font-size : 20px;"
                            "font-family : Times;"
                            "padding : 10px"
                            '}')
        
        self.button_group1.addButton(self.radio1)
        self.button_group1.addButton(self.radio2)
        self.button_group1.addButton(self.radio3)
        self.button_group2.addButton(self.radio4)
        self.button_group2.addButton(self.radio5)
        
        self.radio1.toggled.connect(self.radio_button_changed)
        self.radio2.toggled.connect(self.radio_button_changed)
        self.radio3.toggled.connect(self.radio_button_changed)
        self.radio4.toggled.connect(self.radio_button_changed)
        self.radio5.toggled.connect(self.radio_button_changed)'''
        
        # Using line edit
        '''self.line_edit.setGeometry(10, 10, 200, 40)
        self.line_edit.setStyleSheet("font-size : 20px;"
                                    "font-family : Arial;")
        
        self.push_button.setGeometry(210, 10, 100, 40)
        self.push_button.setStyleSheet("font-size : 20px;"
                                    "font-family : Arial;")
        
        self.push_button.clicked.connect(self.submit)
        self.line_edit.setPlaceholderText('Enter your name')'''
        
        # css properties
        """central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        hbox = QHBoxLayout()
        hbox.addWidget(self.button1)
        hbox.addWidget(self.button2)
        hbox.addWidget(self.button3)
        
        central_widget.setLayout(hbox)
        
        self.button1.setObjectName('b1')
        self.button2.setObjectName('b2')
        self.button3.setObjectName('b3')
        
        
        self.setStyleSheet('''
            QPushButton {
                font-size : 30px;
                font-family : Arial;
                padding : 15px 75px;
                margin : 25px;
                border : 3px solid;
                border-radius : 15px;
                        }
                        
            QPushButton#b1 {
                background-color : red;
            }
            
            QPushButton#b2 {
                background-color : purple;
            }
            
            QPushButton#b3 {
                background-color : orange;
            }
            
            QPushButton#b1:hover {
                background-color : pink;
            }
            
            QPushButton#b2:hover {
                background-color : blue;
            }
            
            QPushButton#b3:hover {
                background-color : yellow;
            }
                        ''')"""
        
    # Function for line edit
    '''def submit(self):
        name = self.line_edit.text()
        print(f'Hello {name}!')'''
        
    # Function for radio button
    '''def radio_button_changed(self):
        radio_button = self.sender()
        if radio_button.isChecked():
            print(f'{radio_button.text()} is selected')'''

    # Function for push button
    '''def on_click(self):
        print('Hello World!')
        self.button.setText('clicked')
        self.label.setText('Bye Jane.')'''
        
    # Function for checkbox
    def checkbox_changed(self, state):
        if state == Qt.Checked:
            print('So you are an anime fan')
        else:
            print('I think you should watch Demon Slayer')
        
def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
    
    
if __name__ == '__main__':
    main()