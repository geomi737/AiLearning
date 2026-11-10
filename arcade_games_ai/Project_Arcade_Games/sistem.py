import os
from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt, pyqtSignal, QObject
from sys import *
from main_ui import Ui_MainWindow
import subprocess

# Автоматически переходим в папку со скриптом
os.chdir(os.path.dirname(os.path.abspath(__file__)))

import game_utils

# Включает музыку при запуске программы
game_utils.load_music("musik/Julian Cha — Arcade Game Music Type Beat (www.lightaudio.ru).mp3")

# Сигнал для уведомления о закрытии дочернего окна
class GameSignal(QObject):
    game_closed = pyqtSignal()

# Главное меню
class Menu(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.Pacman.clicked.connect(self.new_game_pacman)
        self.Save_USA.clicked.connect(self.play_save_USA)
        self.Snake.clicked.connect(self.play_Snake)
        self.Star_Batls.clicked.connect(self.play_Star_Batls)
        self.Honey_Bee.clicked.connect(self.play_Honey_Bee)
        self.Car_Survival.clicked.connect(self.play_Car_Survival)
        self.Close_window.clicked.connect(self.close_main_window)

        # Флаг для отслеживания состояния музыки
        self.music_playing = True

        # Сигнал для уведомления о закрытии дочернего окна
        self.game_signal = GameSignal()
        self.game_signal.game_closed.connect(self.on_game_closed)

    # Останавливает музыку
    def stop_music(self):
        game_utils.stop_music()
        self.music_playing = False

    # Возобновляет музыку
    def resume_music(self):
        if not self.music_playing:
            game_utils.resume_music()
            self.music_playing = True

    # Обработчик закрытия дочернего окна
    def on_game_closed(self):
        self.setEnabled(True)
        self.showNormal()
        self.resume_music()

    def _run_game(self, script):
        self.stop_music()
        self.setEnabled(False)
        self.setWindowState(Qt.WindowState.WindowMinimized)
        subprocess.run([executable, script])
        self.setEnabled(True)
        self.showNormal()
        self.resume_music()

    # Открывает окно Pacman
    def new_game_pacman(self):
        self._run_game('pacman.py')

    # Открывает окно Save USA
    def play_save_USA(self):
        self._run_game('save_USA.py')

    # Открывает окно Змейки
    def play_Snake(self):
        self._run_game('snake.py')

    # Открывает окно Star Battles
    def play_Star_Batls(self):
        self._run_game('star_batls.py')

    # Открывает окно Honey Bee
    def play_Honey_Bee(self):
        self._run_game('honey_bee.py')

    # Открывает окно Survival Car
    def play_Car_Survival(self):
        self._run_game('survival_car.py')

    # Кнопка выхода
    def close_main_window(self):
        dlg = QMessageBox(self)
        btn = dlg.question(
            self,
            "Подтверждение выхода",
            "Выйти из приложения?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if btn == QMessageBox.StandardButton.Yes:
            self.stop_music()
            self.close()

    # Обработка события закрытия окна
    def closeEvent(self, event):
        self.resume_music()
        event.accept()

if __name__ == '__main__':
    app = QApplication(argv)
    ex = Menu()
    ex.show()
    exit(app.exec())
