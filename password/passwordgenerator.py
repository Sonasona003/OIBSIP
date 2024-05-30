import sys
import random
import string
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
    QPushButton, QCheckBox, QSpinBox, QMessageBox
)

class PasswordGenerator(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.length_label = QLabel('Password Length:')
        self.length_spinbox = QSpinBox()
        self.length_spinbox.setRange(8, 128)
        self.length_spinbox.setValue(12)

        length_layout = QHBoxLayout()
        length_layout.addWidget(self.length_label)
        length_layout.addWidget(self.length_spinbox)

        self.uppercase_checkbox = QCheckBox('Include Uppercase Letters')
        self.uppercase_checkbox.setChecked(True)
        self.lowercase_checkbox = QCheckBox('Include Lowercase Letters')
        self.lowercase_checkbox.setChecked(True)
        self.digits_checkbox = QCheckBox('Include Digits')
        self.digits_checkbox.setChecked(True)
        self.special_checkbox = QCheckBox('Include Special Characters')
        self.special_checkbox.setChecked(True)

        self.generate_button = QPushButton('Generate Password')
        self.generate_button.clicked.connect(self.generate_password)

        self.password_label = QLabel('Generated Password:')
        self.password_display = QLineEdit()
        self.password_display.setReadOnly(True)

        self.copy_button = QPushButton('Copy to Clipboard')
        self.copy_button.clicked.connect(self.copy)

        layout.addLayout(length_layout)
        layout.addWidget(self.uppercase_checkbox)
        layout.addWidget(self.lowercase_checkbox)
        layout.addWidget(self.digits_checkbox)
        layout.addWidget(self.special_checkbox)
        layout.addWidget(self.generate_button)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_display)
        layout.addWidget(self.copy_button)

        self.setLayout(layout)
        self.setWindowTitle('Advanced Password Generator')
        self.setGeometry(300, 300, 400, 200)

    def generate_password(self):
        length = self.length_spinbox.value()
        include_uppercase = self.uppercase_checkbox.isChecked()
        include_lowercase = self.lowercase_checkbox.isChecked()
        include_digits = self.digits_checkbox.isChecked()
        include_special = self.special_checkbox.isChecked()

        if not (include_uppercase or include_lowercase or include_digits or include_special):
            QMessageBox.warning(self, 'Warning', 'Please select at least one character type.')
            return

        characters = ''
        if include_uppercase:
            characters += string.ascii_uppercase
        if include_lowercase:
            characters += string.ascii_lowercase
        if include_digits:
            characters += string.digits
        if include_special:
            characters += string.punctuation

        password = ''.join(random.choice(characters) for _ in range(length))
        self.password_display.setText(password)

    def copy(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.password_display.text())
        QMessageBox.information(self, 'Copied', 'Password copied to clipboard.')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PasswordGenerator()
    ex.show()
    sys.exit(app.exec_())
