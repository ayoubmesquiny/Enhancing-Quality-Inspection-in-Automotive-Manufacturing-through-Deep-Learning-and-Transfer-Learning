import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QGridLayout, QSpacerItem, QSizePolicy, QDesktopWidget
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt

class Message(QWidget):
    def __init__(self, message, background, color):
        super().__init__()

        self.setWindowFlags(Qt.Window | Qt.CustomizeWindowHint)
        self.setWindowIcon(QIcon('img/learLogo.png'))
        self.setWindowOpacity(0.8)

        desktop = QDesktopWidget()
        fixed_width_percentage = 1.0
        fixed_width = int(desktop.screenGeometry().width() * fixed_width_percentage)

        fixed_height_percentage = 0.5
        fixed_height = int(desktop.screenGeometry().height() * fixed_height_percentage)

        self.setFixedSize(fixed_width, fixed_height)
        self.setStyleSheet("background-color:" + background + ";color:" + color + "")

        font = QFont()
        font.setPointSize(50)
        self.message_label = QLabel(message)
        self.message_label.setAlignment(Qt.AlignCenter)
        self.message_label.setFont(font)

        self.ok_button = QPushButton("OK")
        self.ok_button.setFixedSize(200, 50)
        self.ok_button.setCursor(Qt.PointingHandCursor)
        self.ok_button.clicked.connect(self.on_ok_clicked)

        layout = QGridLayout(self)
        layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding), 0, 0)  # Add spacer at the top
        layout.addWidget(self.message_label, 1, 0, alignment=Qt.AlignCenter)  # Center the label in the grid
        layout.addWidget(self.ok_button, 2, 0, alignment=Qt.AlignCenter)  # Center the button in the grid
        layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding), 3, 0)  # Add spacer at the bottom

        self.setLayout(layout)
        self.center_on_screen()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.center_on_screen()

    def center_on_screen(self):
        screen_center = QDesktopWidget().screenGeometry().center()
        self.move(screen_center - self.rect().center())

    def on_ok_clicked(self):
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Message("Your message goes here", "lightgray", "black")
    window.show()
    sys.exit(app.exec_())
