import os
import random

from PyQt5.QtMultimedia import QSoundEffect
from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl, pyqtSignal
class SnowFlake(QWidget):
    closed = pyqtSignal()
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(900, 600)
        self.setStyleSheet("""
        background-color: #0f0f0f;
        border-radius:22px;
        """)
        self.click_sounds = []
        for i in range(1, 6):
            sound = QSoundEffect(self)
            sound.setSource(
                QUrl.fromLocalFile(
                    os.path.join(
                        os.path.dirname(__file__),
                        "sounds",
                        f"{i}-click-for-w12-we.wav"
                    )
                )
            )
            sound.setVolume(0.6)
            self.click_sounds.append(sound)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(10)
        top = QHBoxLayout()
        self.back_btn = QPushButton("<")
        self.forward_btn = QPushButton(">")
        self.reload_btn = QPushButton("⟳")
        self.close_btn = QPushButton("X")
        self.url_bar = QLineEdit()
        for btn in (self.back_btn, self.forward_btn, self.reload_btn, self.close_btn):
            btn.setFixedSize(36, 36)
            btn.setStyleSheet("""
            QPushButton {
            background-color: rgba(255,255,255,40);
            border: none;
            color: white;
            font-size:16px;
            border-radius: 12px;
            }
            QPushButton:hover {
            background-color: rgba(255,255,255,80);
            }
            """)
        self.url_bar.setPlaceholderText("URL")
        self.url_bar.setStyleSheet("""
        QLineEdit {
        background-color: rgba(255,255,255,20);
        border: none;
        border-radius: 12px;
        padding:8px;
        color:white;
        font-size:14px;
        }
        """)
        top.addWidget(self.back_btn)
        top.addWidget(self.forward_btn)
        top.addWidget(self.reload_btn)
        top.addWidget(self.url_bar)
        top.addWidget(self.close_btn)
        layout.addLayout(top)
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("https://google.com"))
        layout.addWidget(self.browser)
        self.back_btn.clicked.connect(self.browser.back)
        self.back_btn.clicked.connect(self.play_click)
        self.forward_btn.clicked.connect(self.browser.forward)
        self.forward_btn.clicked.connect(self.play_click)
        self.reload_btn.clicked.connect(self.browser.reload)
        self.reload_btn.clicked.connect(self.play_click)
        self.close_btn.clicked.connect(self.close_browser)
        self.close_btn.clicked.connect(self.play_click)
        self.url_bar.returnPressed.connect(self.load_url)
        self.browser.urlChanged.connect(self.update_url)
        self.browser.urlChanged.connect(self.play_click)
    def load_url(self):
        url = self.url_bar.text().strip()
        if not url.startswith("http"):
            url = "https://" + url
        self.browser.setUrl(QUrl(url))
    def update_url(self, url):
        self.url_bar.setText(url.toString())
    def close_browser(self):
        self.hide()
        self.closed.emit()
    def play_click(self):
        sound = random.choice(self.click_sounds)
        if sound.isPlaying():
            sound.stop()
        sound.play()