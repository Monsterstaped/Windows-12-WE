import os.path
import sys
from PyQt5.QtMultimedia import QSoundEffect
from PyQt5.QtGui import QIcon, QPixmap,QKeySequence
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel,QPushButton,QGraphicsOpacityEffect,QShortcut
from PyQt5.QtCore import QSize, QPropertyAnimation, QTimer, QUrl, Qt
from Settings import Settings
from SnowFlake import SnowFlake
from ShutDownConfirm import ShutdownConfirm
from Windows12DB import create_tables,save_settings,load_settings
from Calculator import Calculator
import os,random


class MainWindow(QMainWindow):
    def start_system(self):
        self.bg.show()
        self.taskbar.show()
        self.apply_hide_icons()
        self.boot_sound.play()
        self.fade_in_system()
    def __init__(self):
        super().__init__()
        brightness, hide_icons,wallpaper = load_settings()
        self.brightness = brightness
        self.wallpapers = [
            os.path.join(os.path.dirname(__file__), "images", "wallpaper", "1-wallpaper-for-w12-we.png"),
            os.path.join(os.path.dirname(__file__), "images", "wallpaper", "2-wallpaper-for-w12-we.png"),
            os.path.join(os.path.dirname(__file__), "images", "wallpaper", "3-wallpaper-for-w12-we.png"),
            os.path.join(os.path.dirname(__file__), "images", "wallpaper", "4-wallpaper-for-w12-we.png"),
            os.path.join(os.path.dirname(__file__), "images", "wallpaper", "5-wallpaper-for-w12-we.png"),
            os.path.join(os.path.dirname(__file__), "images", "wallpaper", "6-wallpaper-for-w12-we.png"),
            os.path.join(os.path.dirname(__file__), "images", "wallpaper", "7-wallpaper-for-w12-we.png"),
            os.path.join(os.path.dirname(__file__), "images", "wallpaper", "8-wallpaper-for-w12-we.png"),
            os.path.join(os.path.dirname(__file__), "images", "wallpaper", "9-wallpaper-for-w12-we.png"),
            os.path.join(os.path.dirname(__file__), "images", "wallpaper", "10-wallpaper-for-w12-we.png")
        ]
        self.current_wallpaper = wallpaper
        self.hide_icons = hide_icons
        self.boot_sound = QSoundEffect(self)
        self.boot_sound.setSource(
            QUrl.fromLocalFile(os.path.join(os.path.dirname(__file__),"sounds","1-bootsound-for-w12-we.WAV"))
        )
        self.boot_sound.setVolume(1.0)
        self.victory_sound = QSoundEffect(self)
        self.victory_sound.setSource(
            QUrl.fromLocalFile(os.path.join(os.path.dirname(__file__),"sounds","1-victory-for-w12-we.wav"))
        )
        self.victory_sound.setVolume(0.5)
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
        self.setWindowTitle("Windows12:WE")
        self.central = QWidget(self)
        self.setCentralWidget(self.central)
        self.central.setStyleSheet("background-color: black")
        self.bg = QLabel(self.central)
        self.bg.setScaledContents(True)
        self.set_wallpaper(self.current_wallpaper)
        self.bg.hide()
        self.taskbar = QWidget(self.central)
        self.taskbar.setStyleSheet("background-color: rgba(15,15,15,0.5);"
                                   "border-radius: 30px;")
        self.taskbar.hide()
        self.setting_btn = QPushButton(self.taskbar)
        self.setting_btn.setIcon(QIcon(os.path.join(os.path.dirname(__file__),"images","1-setting-for-w12-we.png")))
        self.setting_btn.setIconSize(QSize(50,50))
        self.setting_btn.setFixedSize(48,48)
        self.setting_btn.setStyleSheet("""
        QPushButton {
        background: transparent;
        border:none;
        }
        QPushButton:hover {
        background-color: rgba(255,255,255,40);
        border-radius: 12px;}
        """)
        self.settings = Settings(self)
        self.settings.hide()
        self.setting_btn.clicked.connect(self.open_settings)
        self.setting_btn.clicked.connect(self.play_click)
        self.overlay = QWidget(self)
        self.overlay.setStyleSheet("background-color: black;")
        self.overlay.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        self.overlay.setFocusPolicy(Qt.NoFocus)
        self.overlay_effect = QGraphicsOpacityEffect(self.overlay)
        opacity = (100 - self.brightness) / 100
        self.overlay_effect.setOpacity(opacity)
        self.overlay.setGraphicsEffect(self.overlay_effect)
        self.set_brightness(self.brightness)
        self.overlay.show()
        self.overlay.raise_()
        self.browser_btn = QPushButton(self.taskbar)
        self.browser_btn.setIcon(QIcon(os.path.join(os.path.dirname(__file__),"images","5-SnowFlake-for-w12-we.png")))
        self.browser_btn.setIconSize(QSize(50,50))
        self.browser_btn.setFixedSize(48,48)
        self.browser_btn.setStyleSheet("""
        QPushButton {
        background:transparent;
        border:none}
        QPushButton:hover {
        background-color: rgba(255,255,255,40);
        border-radius:12px;}
        """)
        self.calculator = Calculator(self)
        self.calculator.hide()
        self.calculator_btn = QPushButton(self.taskbar)
        self.calculator_btn.setIcon(QIcon(os.path.join(os.path.dirname(__file__), "images", "5-calculator-for-w12-we.png")))
        self.calculator_btn.setIconSize(QSize(50, 50))
        self.calculator_btn.setFixedSize(48, 48)
        self.calculator_btn.setStyleSheet("""
        QPushButton {
        background: transparent;
        border:none;
        }
        QPushButton:hover {
        background-color: rgba(255,255,255,40);
        border-radius: 12px;}
        """)
        self.calculator_btn.clicked.connect(self.open_calculator)
        self.calculator_btn.clicked.connect(self.play_click)
        self.browser_btn.clicked.connect(self.open_browser)
        self.browser_btn.clicked.connect(self.play_click)
        self.windows_btn = QPushButton(self.taskbar)
        self.windows_btn.setIcon(QIcon(os.path.join(os.path.dirname(__file__),"images", "1-windows-for-w12-we.png")))
        self.windows_btn.setIconSize(QSize(50,50))
        self.windows_btn.setFixedSize(48,48)
        self.windows_btn.setStyleSheet("""
        QPushButton {
        background: transparent;
        border:none;
        }
        QPushButton:hover {
        background-color: rgba(255,255,255,40);
        border-radius: 12px;}
        """)
        self.windows_btn.clicked.connect(self.play_victory)
        self.windows_btn.clicked.connect(self.play_click)
        self.desktop_setting_btn = QPushButton(self.central)
        self.desktop_setting_btn.setIcon(QIcon(os.path.join(os.path.dirname(__file__),"images","3-setting-for-w12-we.png")))
        self.desktop_setting_btn.setIconSize(QSize(150,150))
        self.desktop_setting_btn.setFixedSize(150,150)
        self.desktop_setting_btn.setStyleSheet("""
        QPushButton {
        background: transparent;
        border:none;}
        QPushButton:hover {
        background-color: rgba(255,255,255,40);
        border-radius: 12px;}
        """)
        self.desktop_setting_btn.clicked.connect(self.open_settings)
        self.desktop_setting_btn.clicked.connect(self.play_click)
        self.desktop_setting_label =QLabel("Settings",self)
        self.desktop_setting_label.setAlignment(Qt.AlignCenter)
        self.desktop_setting_label.setStyleSheet("""
        QLabel{
        color:white;
        font-size:12px;}
        """)
        self.desktop_setting_label.setFixedWidth(150)
        self.desktop_browser_btn = QPushButton(self.central)
        self.desktop_browser_btn.setIcon(
            QIcon(os.path.join(os.path.dirname(__file__), "images", "4-SnowFlake-for-w12-we.png")))
        self.desktop_browser_btn.setIconSize(QSize(150, 150))
        self.desktop_browser_btn.setFixedSize(150, 150)
        self.desktop_browser_btn.setStyleSheet("""
        QPushButton {
        background: transparent;
        border:none;}
        QPushButton:hover {
        background-color: rgba(255,255,255,40);
        border-radius: 12px;}
        """)
        self.desktop_calculator_btn = QPushButton(self.central)
        self.desktop_calculator_btn.setIcon(QIcon(os.path.join(os.path.dirname(__file__), "images", "4-calculator-for-w12-we.png")))
        self.desktop_calculator_btn.setIconSize(QSize(150, 150))
        self.desktop_calculator_btn.setFixedSize(150, 150)
        self.desktop_calculator_btn.setStyleSheet("""
        QPushButton {
        background: transparent;
        border:none;}
        QPushButton:hover {
        background-color: rgba(255,255,255,40);
        border-radius: 12px;}
        """)
        self.desktop_calculator_btn.clicked.connect(self.open_calculator)
        self.desktop_calculator_btn.clicked.connect(self.play_click)
        self.desktop_calculator_label = QLabel("Calculator", self)
        self.desktop_calculator_label.setAlignment(Qt.AlignCenter)
        self.desktop_calculator_label.setStyleSheet("""
        QLabel{
        color:white;
        font-size:12px;}
        """)
        self.desktop_calculator_label.setFixedWidth(150)
        self.desktop_browser_window = SnowFlake(self)
        self.desktop_browser_window.hide()
        self.desktop_browser_btn.clicked.connect(self.open_browser)
        self.desktop_browser_btn.clicked.connect(self.play_click)
        self.desktop_browser_label = QLabel("SnowFlake \nBrowser",self)
        self.desktop_browser_label.setAlignment(Qt.AlignCenter)
        self.desktop_browser_label.setStyleSheet("""
        QLabel {
        color:white;
        font-size:12px;}
        """)
        self.desktop_browser_label.setFixedWidth(150)
        self.desktop_icons = [
            self.desktop_calculator_btn,
            self.desktop_calculator_label,
            self.desktop_browser_btn,
            self.desktop_browser_label,
            self.desktop_setting_label,
            self.desktop_setting_btn
        ]

        for w in self.desktop_icons:
            w.setVisible(False)
        delay = random.randint(1000,5000)
        self.shutdown_shortcut = QShortcut(QKeySequence("Ctrl+Q"), self)
        self.shutdown_shortcut.setContext(Qt.ApplicationShortcut)
        self.shutdown_shortcut.setAutoRepeat(False)
        self.shutdown_shortcut.activated.connect(self.ask_shutdown)
        self.shutting_down = False
        QTimer.singleShot(delay, self.start_system)
    def open_calculator(self):
        self.calculator.show()
        self.calculator.raise_()
        self.calculator.move(
            (self.width() - self.calculator.width()) // 2,
            (self.height() - self.calculator.height()) // 2
        )
        self.overlay.raise_()

    def apply_hide_icons(self):
        for widget in self.desktop_icons:
            widget.setVisible(not self.hide_icons)
    def open_settings(self):
        self.settings.show()
        self.settings.raise_()
        self.settings.move(
            (self.width() - self.settings.width()) // 2,
            (self.height() - self.settings.height()) // 2
        )
        self.overlay.raise_()
    def fade_in_system(self):
        self.opacity = QGraphicsOpacityEffect(self.central)
        self.central.setGraphicsEffect(self.opacity)
        self.opacity.setOpacity(0)
        self.anim = QPropertyAnimation(self.opacity, b"opacity")
        self.anim.setDuration(1200)
        self.anim.setStartValue(0)
        self.anim.setEndValue(1)
        self.anim.start()
    def resizeEvent(self, event):
        self.bg.setGeometry(self.central.rect())
        taskbar_width = 700
        taskbar_height = 75
        x = (self.width() - taskbar_width) // 2
        y = self.height() - taskbar_height - 20
        self.overlay.setGeometry(self.central.rect())
        self.overlay.raise_()
        self.taskbar.setGeometry(x, y, taskbar_width, taskbar_height)
        self.setting_btn.move(88, (taskbar_height - 48) // 2)
        self.windows_btn.move(20, (taskbar_height - 48) // 2)
        self.browser_btn.move(156,(taskbar_height - 48) // 2)
        self.calculator_btn.move(224,(taskbar_height - 48) // 2)
        icon_x = 40
        icon_y = 40
        self.desktop_setting_btn.move(icon_x, icon_y + 40)
        self.desktop_setting_label.move(icon_x, icon_y + 195)
        self.desktop_browser_btn.move(icon_x, icon_y + 260)
        self.desktop_calculator_btn.move(icon_x, icon_y + 480)
        self.desktop_browser_label.move(icon_x, icon_y + 415)
        self.desktop_calculator_label.move(icon_x, icon_y + 635)
        super().resizeEvent(event)
    def set_brightness(self, value):
        self.brightness = value
        save_settings(brightness=value, hide_icons=self.hide_icons)
        opacity = (100 - value) / 100
        self.overlay_effect.setOpacity(opacity)
    def play_victory(self):
        self.victory_sound.stop()
        self.victory_sound.play()
    def play_click(self):
        sound = random.choice(self.click_sounds)
        if sound.isPlaying():
            sound.stop()
        sound.play()
    def set_wallpaper(self, index):
        self.current_wallpaper = index
        self.bg.setPixmap(QPixmap(self.wallpapers[index]))
        save_settings(
            brightness=self.brightness,
            hide_icons=self.hide_icons,
            wallpaper=index
        )
    def start_shutdown_animation(self):
        if self.shutting_down:
            return
        self.shutting_down = True
        self.shutdown_overlay = QWidget(self)
        self.shutdown_overlay.setGeometry(self.rect())
        texts = ["Виключення...","Оновлення...1 з 3","Вимкнення...","Завершення роботи...","Не вимикайте компютер","Збереження Налаштувань...","Сеанс буде завершено...","Майже готово..."]
        self.shutdown_overlay.setStyleSheet("background-color: black;")
        self.label = QLabel((random.choice(texts)), self.shutdown_overlay)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("""
        color: white;
        font-size: 28px;
        font-weight: 300;
        """)
        self.label.setGeometry(self.overlay.rect())
        self.shutdown_overlay_effect = QGraphicsOpacityEffect(self.shutdown_overlay)
        self.shutdown_overlay.setGraphicsEffect(self.shutdown_overlay_effect)
        self.shutdown_overlay_effect.setOpacity(0)
        self.fade_anim = QPropertyAnimation(self.shutdown_overlay_effect, b"opacity")
        self.fade_anim.setDuration(900)
        self.fade_anim.setStartValue(0)
        self.fade_anim.setEndValue(1)
        self.fade_anim.start()
        self.shutdown_overlay.show()
        self.shutdown_overlay.raise_()
        self.overlay.raise_()
        QTimer.singleShot(random.randint(1000,5000), self.close)
    def open_browser(self):
        self.desktop_browser_window.show()
        self.desktop_browser_window.raise_()
        self.desktop_browser_window.move(
            (self.width() - self.desktop_browser_window.width()) // 2,
            (self.height() - self.desktop_browser_window.height()) // 2
        )
        self.overlay.raise_()
    def ask_shutdown(self):
        if hasattr(self, "confirm") and self.confirm.isVisible():
            return
        self.confirm = ShutdownConfirm(
            self,
            on_confirm=self.start_shutdown_animation
        )
        self.confirm.move(
            (self.width() - self.confirm.width()) // 2,
            (self.height() - self.confirm.height()) // 2
        )
        self.confirm.show()
        self.overlay.raise_()
    def closeEvent(self, event):
        if self.shutting_down:
            event.accept()
        else:
            event.ignore()
            self.ask_shutdown()
if __name__ == "__main__":
    create_tables()
    app = QApplication(sys.argv)
    window = MainWindow()
    window.showFullScreen()
    app.setQuitOnLastWindowClosed(True)
    sys.exit(app.exec_())
