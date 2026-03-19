from PyQt5.QtWidgets import QWidget, QLabel, QPushButton
from PyQt5.QtCore import Qt, QTimer
import os,random
from PyQt5.QtMultimedia import QSoundEffect
from PyQt5.QtCore import QUrl
class ShutdownConfirm(QWidget):
    def __init__(self, parent=None, on_confirm=None):
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
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.on_confirm = on_confirm
        self.setFixedSize(420, 180)
        self.setStyleSheet("""
            background-color: rgba(20,20,20,230);
            border-radius: 22px;
            color: white;
        """)
        self.label = QLabel("Виключити систему?", self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setGeometry(0, 30, 420, 40)
        self.label.setAutoFillBackground(True)
        self.label.setStyleSheet("""
        QLabel {
        font-size:20px;
        background-color: transparent;
        color: red;}
        """)
        self.ok = QPushButton("Виключити", self)
        self.ok.setGeometry(60, 100, 130, 40)
        self.cancel = QPushButton("Скасувати", self)
        self.cancel.setGeometry(230, 100, 130, 40)
        for btn in (self.ok, self.cancel):
            btn.setStyleSheet("""
                QPushButton {
                background: rgba(255,255,255,40);
                border: none;
                border-radius: 14px;
                }
                QPushButton:hover {
                background: rgba(255,255,255,80);
                }
            """)
        self.ok.clicked.connect(self._on_confirm)
        self.ok.clicked.connect(self.play_click)
        self.cancel.clicked.connect(self._on_cancel)
        self.cancel.clicked.connect(self.play_click)
    def _on_confirm(self):
        self.close()
        if self.on_confirm:
            QTimer.singleShot(0, self.on_confirm)
    def _on_cancel(self):
        self.close()
    def play_click(self):
        sound = random.choice(self.click_sounds)
        if sound.isPlaying():
            sound.stop()
        sound.play()