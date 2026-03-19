import os
import random

from PyQt5.QtMultimedia import QSoundEffect
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QPushButton, QLineEdit, QHBoxLayout
from PyQt5.QtCore import Qt, QUrl


class Calculator(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
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
        self.setFixedSize(300, 400)
        self.setWindowTitle("Calculator")
        self.setStyleSheet("background-color:#0f0f0f; color:white;")
        main = QVBoxLayout(self)
        self.display = QLineEdit("0")
        self.display.setAlignment(Qt.AlignRight)
        self.display.setReadOnly(True)
        self.display.setFixedHeight(60)
        self.display.setStyleSheet("""
        QLineEdit {
        background:#1a1a1a;
        border:none;
        font-size:26px;
        padding:10px;
            }
        """)
        top = QHBoxLayout()
        top.addStretch()
        self.close_btn = QPushButton("X",self)
        self.close_btn.clicked.connect(self.hide)
        self.close_btn.clicked.connect(self.play_click)
        self.close_btn.setFixedSize(32, 32)
        self.close_btn.move(self.width() - 40,8)
        self.close_btn.setCursor(Qt.PointingHandCursor)
        self.close_btn.setStyleSheet("""
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
        top.addWidget(self.close_btn)
        main.addLayout(top)
        main.addWidget(self.display)
        grid = QGridLayout()
        main.addLayout(grid)
        buttons = [
            ("7", 0, 0), ("8", 0, 1), ("9", 0, 2), ("/", 0, 3),
            ("4", 1, 0), ("5", 1, 1), ("6", 1, 2), ("*", 1, 3),
            ("1", 2, 0), ("2", 2, 1), ("3", 2, 2), ("-", 2, 3),
            ("0", 3, 0), ("C", 3, 1), ("=", 3, 2), ("+", 3, 3),
        ]
        for text, row, col in buttons:
            btn = QPushButton(text)
            btn.setFixedSize(60, 60)
            btn.setStyleSheet("""
            QPushButton {
            background:#2a2a2a;
            border:none;
            font-size:18px;
            border-radius:10px;
            }
            QPushButton:hover {
                background:#3a3a3a;
                }
            """)
            btn.clicked.connect(lambda _, t=text: self.on_click(t))
            btn.clicked.connect(self.play_click)
            grid.addWidget(btn, row, col)
    def on_click(self, text):
        if text == "C":
            self.display.setText("0")
            return
        if text == "=":
            try:
                result = str(eval(self.display.text()))
                self.display.setText(result)
            except:
                self.display.setText("Error")
            return
        if self.display.text() == "0":
            self.display.setText(text)
        else:
            self.display.setText(self.display.text() + text)
    def play_click(self):
        sound = random.choice(self.click_sounds)
        if sound.isPlaying():
            sound.stop()
        sound.play()