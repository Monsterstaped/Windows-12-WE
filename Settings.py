from PyQt5.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout,
    QPushButton, QLabel, QStackedWidget,
    QSlider, QGraphicsOpacityEffect,QCheckBox
)
from PyQt5.QtMultimedia import QSoundEffect
from PyQt5.QtCore import QUrl
import os,random
from Windows12DB import save_settings
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve
class Settings(QWidget):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.setFixedSize(700,400)
        self.setStyleSheet("background-color:#0f0f0f;color:white;border-radius:22px;")
        main = QHBoxLayout(self)
        main.setContentsMargins(0,0,0,0)
        left = QWidget()
        left.setFixedWidth(120)
        left.setStyleSheet("background-color:#0c0c0c;")
        left_layout = QVBoxLayout(left)
        left_layout.setAlignment(Qt.AlignTop)
        left_layout.setSpacing(10)
        self.btn_setting = QPushButton("Settings")
        self.btn_about = QPushButton("About")
        for btn in (self.btn_setting,self.btn_about):
            btn.setFixedSize(100,52)
            btn.setStyleSheet("""
                QPushButton {
                font-size: 16px;
                color: white;
                background: transparent;
                border: none;
                border-radius: 14px;}
                QPushButton:hover {
                background-color: rgba(255,255,255,40);}        
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
        self.brightness_label = QLabel("Brightness")
        self.brightness_slider = QSlider(Qt.Horizontal)
        self.brightness_slider.setRange(30, 100)
        self.brightness_slider.setValue(self.parent().brightness)
        self.brightness_slider.setStyleSheet(
        """
        QSlider::groove:horizontal {
        height: 4px;
        background: #2a2a2a;
        border-radius: 2px;
        }
        QSlider::sub-page:horizontal {
        background: #9adfff;
        border-radius: 2px;}
        QSlider::add-page:horizontal {
        background: #2a2a2a;
        border-radius: 2px;}
        QSlider::handle:horizontal {
        width: 12px;
        height: 12px;
        background: #e6e6e6;
        border-radius: 6px;
        margin: -4px 0;}
        QSlider::handle:horizontal:hover {
        background: #ffffff;}

        """
        )
        self.brightness_slider.valueChanged.connect(self.on_brightness_changed)
        self.brightness_slider.setTracking(True)
        self.hide_icons = QCheckBox()
        self.hide_icons.setChecked(self.parent().hide_icons)
        self.hide_icons.setStyleSheet("""
        QCheckBox{
        font-size: 14px;
        }
        QCheckBox::indicator {
        width:18px;
        height:18px;}
        """)
        self.hide_icons.stateChanged.connect(self.toggle_hide_icons)
        self.hide_icons.stateChanged.connect(self.play_click)
        left_layout.addSpacing(20)
        left_layout.addWidget(self.btn_setting)
        left_layout.addWidget(self.btn_about)
        left_layout.addStretch()
        sep = QWidget()
        sep.setFixedWidth(1)
        sep.setStyleSheet("background-color:transparent;")
        self.stack = QStackedWidget()
        setting_page = QWidget()
        sp = QVBoxLayout(setting_page)
        sp.setSpacing(15)
        sp.addWidget(QLabel("Settings"))
        sp.addWidget(QLabel("Hide Desktop Icons"))
        sp.addWidget(self.hide_icons)
        self.change_wallpaper_btn = QPushButton("Change wallpaper")
        self.change_wallpaper_btn.clicked.connect(self.change_bg)
        self.change_wallpaper_btn.clicked.connect(self.play_click)
        sp.addWidget(self.change_wallpaper_btn)
        sp.addWidget(QLabel("Brightness"))
        sp.addWidget(self.brightness_slider)
        sp.addStretch()
        about_page = QWidget()
        ap = QVBoxLayout(about_page)
        ap.addWidget(QLabel("About Windows 12 Winter Edition:"))
        ap.addWidget(QLabel("Windows 12 Winter Edition is a fan made project \n"
                            "This is not an official Microsoft product"))
        ap.addStretch()
        self.close_btn = QPushButton("X", self)
        self.close_btn.setFixedSize(32, 32)
        self.close_btn.move(self.width() - 42, 10)
        self.close_btn.setStyleSheet("""
                QPushButton {
                background: transparent;
                border: none;
                color: white;
                font-size: 20px;
                }
                QPushButton:hover {
                background-color: rgba(255,255,255,40);
                border-radius: 10px;}
                """)
        self.close_btn.clicked.connect(self.close)
        self.close_btn.clicked.connect(self.play_click)
        self.stack.addWidget(setting_page)
        self.stack.addWidget(about_page)
        main.addWidget(left)
        main.addWidget(sep)
        main.addWidget(self.stack)
        self.close_btn.raise_()
        self.btn_setting.clicked.connect(self.show_setting)
        self.btn_setting.clicked.connect(self.play_click)
        self.btn_about.clicked.connect(self.show_about)
        self.btn_about.clicked.connect(self.play_click)
        effect = QGraphicsOpacityEffect(self.btn_setting)
        self.btn_setting.setGraphicsEffect(effect)
        self.anim = QPropertyAnimation(effect, b"opacity")
        self.anim.setDuration(1400)
        self.anim.setStartValue(1.0)
        self.anim.setEndValue(0.4)
        self.anim.setLoopCount(-1)
        self.anim.setDirection(QPropertyAnimation.Forward)
        self.anim.setEasingCurve(QEasingCurve.InOutSine)
        self.anim.start()
        self.opacity = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity)
        self.fade_in = QPropertyAnimation(self.opacity, b"opacity")
        self.fade_in.setDuration(300)
        self.fade_in.setStartValue(0)
        self.fade_in.setEndValue(1)
        self.show_setting()
    def set_active(self,active_btn):
        for btn in (self.btn_setting,self.btn_about):
            btn.setStyleSheet("""
                QPushButton {
                font-size: 16px;
                color: white;
                background: transparent;
                border: none;
                border-radius: 14px;}
                QPushButton:hover {
                background-color: rgba(255,255,255,40);}        
                """)
        active_btn.setStyleSheet("""
                QPushButton {
                font-size: 16px;
                color: white;
                background: rgba(255,255,255,70);
                border-radius: 14px;}
                """)

    def change_bg(self):
        mv = self.parent()
        mv.current_wallpaper += 1
        if mv.current_wallpaper >= len(mv.wallpapers):
            mv.current_wallpaper = 0
        mv.set_wallpaper(mv.current_wallpaper)
    def show_setting(self):
        self.stack.setCurrentIndex(0)
        self.set_active(self.btn_setting)
    def show_about(self):
        self.stack.setCurrentIndex(1)
        self.set_active(self.btn_about)
    def on_brightness_changed(self,value):
        self.parent().set_brightness(value)
    def toggle_hide_icons(self, state):
        mw = self.parent()
        mw.hide_icons = bool(state)
        save_settings(
            brightness=mw.brightness,
            hide_icons=mw.hide_icons,
            wallpaper=mw.current_wallpaper
        )
        mw.apply_hide_icons()
    def play_click(self):
        sound = random.choice(self.click_sounds)
        if sound.isPlaying():
            sound.stop()
        sound.play()



