import sys, os
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton,
    QTextEdit, QLineEdit, QGridLayout, QVBoxLayout
)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, QTimer, QRect, QPropertyAnimation, QTime

# Optional: suppress WebEngine GPU warnings
os.environ["QTWEBENGINE_DISABLE_GPU"] = "1"

from PySide6.QtWebEngineWidgets import QWebEngineView

# ---------------- CONFIG ----------------
WIDTH, HEIGHT = 400, 644
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(BASE_DIR, "assets")
CITY = "Sylhet"

# ---------------- BASE APP ----------------
class App(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.setGeometry(0, HEIGHT, WIDTH, HEIGHT)
        self.setStyleSheet("background:black; color:white;")
        self.hide()

        close = QPushButton("✕", self)
        close.setGeometry(10, 10, 40, 40)
        close.setStyleSheet("font-size:20px;")
        close.clicked.connect(self.close_app)

    def open(self):
        self.show()
        self.raise_()
        self.animate(HEIGHT, 0)

    def close_app(self):
        self.animate(0, HEIGHT)
        self.hide()

    def animate(self, start, end):
        anim = QPropertyAnimation(self, b"geometry")
        anim.setDuration(300)
        anim.setStartValue(QRect(0, start, WIDTH, HEIGHT))
        anim.setEndValue(QRect(0, end, WIDTH, HEIGHT))
        anim.start()
        self.anim = anim

# ---------------- APPS ----------------
class ClockApp(App):
    def __init__(self, parent):
        super().__init__(parent)
        self.label = QLabel(self)
        self.label.setGeometry(0, 300, WIDTH, 200)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("font-size:64px;")

        timer = QTimer(self)
        timer.timeout.connect(self.update_time)
        timer.start(1000)
        self.update_time()

    def update_time(self):
        self.label.setText(QTime.currentTime().toString("hh:mm:ss"))

class WeatherApp(App):
    def __init__(self, parent):
        super().__init__(parent)
        label = QLabel(f"{CITY}\n🌤 28°C\nSunny", self)
        label.setGeometry(0, 300, WIDTH, 200)
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("font-size:36px;")

class CalculatorApp(App):
    def __init__(self, parent):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        self.display = QLabel("0")
        self.display.setAlignment(Qt.AlignRight)
        self.display.setStyleSheet("font-size:40px; padding:20px;")
        layout.addWidget(self.display)

        self.expr = ""
        grid = QGridLayout()
        layout.addLayout(grid)

        buttons = "789/456*123-0.=+"
        for i, b in enumerate(buttons):
            btn = QPushButton(b)
            btn.setStyleSheet("font-size:22px; padding:15px;")
            btn.clicked.connect(lambda _, x=b: self.press(x))
            grid.addWidget(btn, i // 4, i % 4)

    def press(self, k):
        if k == "=":
            try:
                self.expr = str(eval(self.expr))
            except:
                self.expr = "0"
        else:
            self.expr += k
        self.display.setText(self.expr)

class MessagesApp(App):
    def __init__(self, parent):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        self.chat = QTextEdit(readOnly=True)
        self.input = QLineEdit()
        self.input.setPlaceholderText("iMessage")
        self.input.returnPressed.connect(self.send)
        layout.addWidget(self.chat)
        layout.addWidget(self.input)

    def send(self):
        if self.input.text():
            self.chat.append("You: " + self.input.text())
            self.input.clear()

class CameraApp(App):
    def __init__(self, parent):
        super().__init__(parent)
        self.preview = QLabel("📷 Camera Preview", self)
        self.preview.setGeometry(0, 120, WIDTH, 480)
        self.preview.setAlignment(Qt.AlignCenter)
        self.preview.setStyleSheet("font-size:28px; border:2px solid white;")

        shutter = QPushButton("●", self)
        shutter.setGeometry(WIDTH // 2 - 35, 650, 70, 70)
        shutter.setStyleSheet("""
            font-size:40px;
            border-radius:35px;
            border:3px solid white;
        """)
        shutter.clicked.connect(self.snap)

    def snap(self):
        self.preview.setText("📸 Photo Captured!")

class BrowserApp(App):
    def __init__(self, parent):
        super().__init__(parent)
        layout = QVBoxLayout(self)

        self.url = QLineEdit()
        self.url.setPlaceholderText("https://example.com")
        self.url.returnPressed.connect(self.load)

        self.web = QWebEngineView()
        self.web.load("https://www.google.com")

        layout.addWidget(self.url)
        layout.addWidget(self.web)

    def load(self):
        self.web.load(self.url.text())

class AboutApp(App):
    def __init__(self, parent):
        super().__init__(parent)
        label = QLabel(
            "iOS Runner\n"
            "Version 1.0\n"
            "Python + PySide6\n"
            "Built by Me 😎",
            self
        )
        label.setGeometry(0, 300, WIDTH, 200)
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("font-size:28px;")

# ---------------- PHONE ----------------
class Phone(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(WIDTH, HEIGHT)
        self.setWindowTitle("iOS Runner")
        self.setStyleSheet("background:black;")

        # LOCK SCREEN
        self.lock = QLabel(self)
        self.lock.setPixmap(QPixmap(os.path.join(ASSETS, "lock.png")))
        self.lock.setScaledContents(True)
        self.lock.setGeometry(0, 0, WIDTH, HEIGHT)

        self.time_label = QLabel(self.lock)
        self.time_label.setGeometry(0, 200, WIDTH, 100)
        self.time_label.setAlignment(Qt.AlignCenter)
        self.time_label.setStyleSheet("font-size:60px; color:white;")

        self.city_label = QLabel(CITY, self.lock)
        self.city_label.setGeometry(0, 300, WIDTH, 50)
        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_label.setStyleSheet("font-size:24px;")

        timer = QTimer(self)
        timer.timeout.connect(self.update_time)
        timer.start(1000)
        self.update_time()

        # HOME SCREEN
        self.home = QLabel(self)
        self.home.setPixmap(QPixmap(os.path.join(ASSETS, "home.png")))
        self.home.setScaledContents(True)
        self.home.setGeometry(0, HEIGHT, WIDTH, HEIGHT)

        self.apps = {
            "clock": ClockApp(self),
            "weather": WeatherApp(self),
            "calculator": CalculatorApp(self),
            "messages": MessagesApp(self),
            "camera": CameraApp(self),
            "browser": BrowserApp(self),
            "about": AboutApp(self),
        }

        self.create_icons()
        self.start_y = 0

    def update_time(self):
        self.time_label.setText(QTime.currentTime().toString("hh:mm"))

    def create_icons(self):
        # 🔼 MOVED UP (iOS-like)
        positions = [
            (40, 430), (140, 430), (240, 430),
            (40, 530), (140, 530), (240, 530),
            (140, 630)
        ]

        for (name, app), (x, y) in zip(self.apps.items(), positions):
            btn = QPushButton(self.home)
            btn.setGeometry(x, y, 70, 70)
            btn.setIcon(QPixmap(os.path.join(ASSETS, f"{name}.png")))
            btn.setIconSize(btn.size())
            btn.setStyleSheet("border:none;")
            btn.clicked.connect(app.open)

    def mousePressEvent(self, e):
        self.start_y = e.position().y()

    def mouseReleaseEvent(self, e):
        delta = e.position().y() - self.start_y
        if delta < -120 and self.home.y() == HEIGHT:
            self.slide(self.home, HEIGHT, 0)
        elif delta > 120 and self.home.y() == 0:
            self.slide(self.home, 0, HEIGHT)

    def slide(self, widget, start, end):
        anim = QPropertyAnimation(widget, b"geometry")
        anim.setDuration(350)
        anim.setStartValue(QRect(0, start, WIDTH, HEIGHT))
        anim.setEndValue(QRect(0, end, WIDTH, HEIGHT))
        anim.start()
        self.anim = anim

# ---------------- RUN ----------------
app = QApplication(sys.argv)
phone = Phone()
phone.show()
sys.exit(app.exec())
