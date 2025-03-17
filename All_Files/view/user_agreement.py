from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTextEdit, QPushButton, QCheckBox

class UserAgreementDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("User Agreement")
        self.setGeometry(400, 200, 700, 500)  # Set window size

        layout = QVBoxLayout()

        # User Agreement Text
        self.agreement_text = QTextEdit()
        self.agreement_text.setReadOnly(True)
        self.agreement_text.setText("""
        USER AGREEMENT
        
        1. ACCEPTANCE OF TERMS
        By accessing or using Soul Sync, you acknowledge that you have read, understood, 
        and agree to be bound by this User Agreement and our Privacy Policy.
        
        If you do not agree, please do not use the App.


        2. NOT A SUBSTITUTE FOR PROFESSIONAL HELP
        Soul Sync provides mental health support but is not a substitute for professional 
        medical advice, diagnosis, or treatment.
        
        If you are in crisis or experiencing an emergency, call emergency services or seek
        immediate professional help.


        3. PRIVACY & DATA SECURITY
        Your privacy is important to us. We collect and process your data as described in 
        our Privacy Policy.
        
        
        4. LIMITATION OF LIABILITY
        We are not responsible for any emotional distress, health issues, or damages 
        arising from the use of the App.
    
    
        5. CHANGES TO THIS AGREEMENT
        We may update these terms at any time. Continued use of the App after changes 
        means you accept the new terms.
        """)
        
        layout.addWidget(self.agreement_text)

        # Checkbox for Agreement
        self.checkbox = QCheckBox("I agree to the terms and conditions")
        self.checkbox.stateChanged.connect(self.toggle_button)
        layout.addWidget(self.checkbox)

        # Continue Button (Initially Disabled)
        self.continue_button = QPushButton("Continue")
        self.continue_button.setEnabled(False)
        self.continue_button.clicked.connect(self.accept)
        layout.addWidget(self.continue_button)

        self.setLayout(layout)

    def toggle_button(self):
        """Enable the continue button only if the checkbox is checked."""
        self.continue_button.setEnabled(self.checkbox.isChecked())
