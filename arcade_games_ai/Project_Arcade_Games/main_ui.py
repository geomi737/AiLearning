from PyQt6.QtWidgets import (
    QGridLayout, QPushButton, QWidget, QMainWindow, QStatusBar, QMenuBar,
    QVBoxLayout, QHBoxLayout
)
from PyQt6.QtCore import QMetaObject
from PyQt6.QtGui import QFont, QPixmap, QIcon


# Дизайн главного окна
class Ui_MainWindow(object):
    def setupUi(self, MainWindow: QMainWindow):
        MainWindow.resize(600, 600)
        MainWindow.setWindowTitle("Arcade Games")
        MainWindow.setGeometry(400, 150, 600, 600)
        self.centralwidget = QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralWidget")

        # Основной вертикальный layout
        self.main_layout = QVBoxLayout(self.centralwidget)
        self.centralwidget.setStyleSheet("""
            #centralWidget {
                border-image: url(gallery/Main_menu.jpg) 0 0 0 0;
            }
        """)

        # Сетка для кнопок
        self.grid_layout = QGridLayout()
        self.main_layout.addLayout(self.grid_layout)

        # Кнопки
        button_height = 60  # Увеличенная высота кнопки
        button_width = 200  # Увеличенная ширина кнопки
        # картинки для кнопок
        pixmapSnake = QPixmap("gallery/snake_background.png")
        pixmapPacman = QPixmap("gallery/pacman_background.png")
        pixmapHoneyBee = QPixmap("gallery/honey_bee_background.png")
        pixmapSurvivalCar = QPixmap("gallery/survival_car_background.png")
        pixmapSaveUsa = QPixmap("gallery/save_usa_background.png")
        pixmapStarBatles = QPixmap("gallery/star_batles_background.png")
        pixmapStarBatles = pixmapStarBatles.scaled(200, 60)  # 200x60 — размер кнопки

        


        self.Pacman = QPushButton(self.centralwidget)
        self.Pacman.setFixedHeight(button_height)
        self.Pacman.setFixedWidth(button_width)
        self.Pacman.setIcon(QIcon(pixmapPacman))
        self.Pacman.setIconSize(pixmapPacman.size())

        self.Snake = QPushButton(self.centralwidget)
        self.Snake.setFixedHeight(button_height)
        self.Snake.setFixedWidth(button_width)
        self.Snake.setIcon(QIcon(pixmapSnake))
        self.Snake.setIconSize(pixmapSnake.size())


        self.Honey_Bee = QPushButton(self.centralwidget)
        self.Honey_Bee.setFixedHeight(button_height)
        self.Honey_Bee.setFixedWidth(button_width)
        self.Honey_Bee.setIcon(QIcon(pixmapHoneyBee))
        self.Honey_Bee.setIconSize(pixmapHoneyBee.size())



        self.Car_Survival = QPushButton(self.centralwidget)
        self.Car_Survival.setFixedHeight(button_height)
        self.Car_Survival.setFixedWidth(button_width)
        self.Car_Survival.setIcon(QIcon(pixmapSurvivalCar))
        self.Car_Survival.setIconSize(pixmapSurvivalCar.size())

        self.Star_Batls = QPushButton(self.centralwidget)
        self.Star_Batls.setFixedHeight(button_height)
        self.Star_Batls.setFixedWidth(button_width)
        self.Star_Batls.setIcon(QIcon(pixmapStarBatles))
        self.Star_Batls.setIconSize(pixmapStarBatles.size())


        self.Save_USA = QPushButton(self.centralwidget)
        self.Save_USA.setFixedHeight(button_height)
        self.Save_USA.setFixedWidth(button_width)
        self.Save_USA.setIcon(QIcon(pixmapSaveUsa))
        self.Save_USA.setIconSize(pixmapSaveUsa.size())

        # Расстановка кнопок в сетке
        self.grid_layout.addWidget(self.Pacman, 0, 0)
        self.grid_layout.addWidget(self.Snake, 1, 0)
        self.grid_layout.addWidget(self.Honey_Bee, 2, 0)
        self.grid_layout.addWidget(self.Car_Survival, 0, 1)
        self.grid_layout.addWidget(self.Star_Batls, 1, 1)
        self.grid_layout.addWidget(self.Save_USA, 2, 1)

        # Горизонтальный layout для кнопки "Выход"
        self.bottom_layout = QHBoxLayout()
        self.bottom_layout.addStretch()  # Добавляем растяжку слева
        self.Close_window = QPushButton("Выход", self.centralwidget)
        self.Close_window.setStyleSheet('color: black; font-size: 30px;')
        self.Close_window.setFixedHeight(button_height)
        self.Close_window.setFixedWidth(button_width)
        self.bottom_layout.addWidget(self.Close_window)  # Добавляем кнопку "Выход"
        self.bottom_layout.addStretch()  # Добавляем растяжку справа

        # Добавляем нижний layout в основной
        self.main_layout.addLayout(self.bottom_layout)

        # Растягиваем сетку, чтобы кнопки были сверху
        self.main_layout.setStretch(0, 1)  # Сетка занимает всё доступное пространство
        self.main_layout.setStretch(1, 0)  # Нижний layout не растягивается

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(parent=MainWindow)
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(parent=MainWindow)
        MainWindow.setStatusBar(self.statusbar)

        QMetaObject.connectSlotsByName(MainWindow)