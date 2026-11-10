import pygame
import random
import os
from game_utils import load_image, load_sound, load_music, init_mixer, play_sound

# Переходим в директорию скрипта, чтобы относительные пути работали при запуске напрямую
os.chdir(os.path.dirname(os.path.abspath(__file__)))

class SaveUSA:
    def __init__(self):
        # Инициализация Pygame
        pygame.init()
        init_mixer()

        # Загрузка звуков
        load_music("musik/Donald Trump - Macarena (Kamala Isn't Gonna Beat Me).mp3")
        self.jump_sound = load_sound('musik/pryijok-v-igre.mp3')

        # Настройки окна
        self.screen = pygame.display.set_mode((1250, 700))
        pygame.display.set_caption('Save the USA in 11 september')

        # Загрузка спрайтов
        self.sprite_player1 = load_image('gallery/plane.jpg')
        self.sprite_fon = load_image('gallery/siti_fon.jpg')
        self.sprite_one = load_image('gallery/one.webp')

        # Загрузка случайных колонн
        self.sprite_column1 = load_image('gallery/skyscraper1.png')
        self.sprite_column2 = load_image('gallery/skyscraper1.png')
        self.sprite_column3 = load_image('gallery/skyscraper1.png')
        self.sprite_column4 = load_image('gallery/skyscraper1.png')

        # Игнорирование не нужных цветов (установка прозрачности)
        self.sprite_player1.set_colorkey((255, 255, 255))
        self.sprite_column1.set_colorkey((255, 255, 255))
        self.sprite_column2.set_colorkey((255, 255, 255))
        self.sprite_column3.set_colorkey((255, 255, 255))
        self.sprite_column4.set_colorkey((255, 255, 255))

        # Цвета
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)

        # Начальные параметры
        self.player_y = 360
        self.player_velocity = 0
        self.gravity = 0.5
        self.jump = -10
        self.sky = 10

        # Позиции колонн
        self.column_x1 = 1200
        self.column_y1 = random.randint(140, 400)

        self.column_x2 = 1600
        self.column_y2 = random.randint(140, 400)

        self.column_x3 = 2000
        self.column_y3 = random.randint(140, 400)

        self.column_x4 = 2400
        self.column_y4 = random.randint(140, 400)

        self.points = 0
        self.font = pygame.font.Font(None, 36)

        # Основной цикл
        self.running = True
        self.clock = pygame.time.Clock()
        self.size_column = 700

        # Загрузка рекорда из файла
        self.RECORD_FILE = "records/record_save_USA.txt"
        if os.path.exists(self.RECORD_FILE):
            with open(self.RECORD_FILE, "r") as file:
                self.RECORD = int(file.read())
        else:
            self.RECORD = 0

    # Обрабатывает события игры
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.player_velocity = self.jump
                    play_sound(self.jump_sound)
                    self.sky = 40
    
    # Обновляет позицию игрока с учетом гравитации
    def update_player_position(self):
        self.player_velocity += self.gravity
        self.player_y += self.player_velocity

        if self.player_y < 0:
            self.player_y = 0
            self.player_velocity = 0
    
    # Обновляет позиции колонн и проверяет их рекурсию
    def update_columns_position(self):
        self.column_x1 -= 10
        self.column_x2 -= 10
        self.column_x3 -= 10
        self.column_x4 -= 10
        self.sky -= 1

        if self.column_x1 <= -100:
            self.column_x1 = 1400
            self.column_y1 = random.randint(140, 300)
            self.points += 1

        if self.column_x2 <= -100:
            self.column_x2 = 1400
            self.column_y2 = random.randint(140, 300)
            self.points += 1

        if self.column_x3 <= -100:
            self.column_x3 = 1400
            self.column_y3 = random.randint(140, 300)
            self.points += 1

        if self.column_x4 <= -100:
            self.column_x4 = 1400
            self.column_y4 = random.randint(140, 300)
            self.points += 1
    
    # Отрисовывает колонны на экране
    def draw_columns(self):
        column1 = self.screen.blit(pygame.transform.scale(self.sprite_column1, (150, self.size_column)), (self.column_x1, self.column_y1))
        column2 = self.screen.blit(pygame.transform.scale(self.sprite_column2, (150, self.size_column)), (self.column_x2, self.column_y2))
        column3 = self.screen.blit(pygame.transform.scale(self.sprite_column3, (150, self.size_column)), (self.column_x3, self.column_y3))
        column4 = self.screen.blit(pygame.transform.scale(self.sprite_column4, (150, self.size_column)), (self.column_x4, self.column_y4))
        return column1, column2, column3, column4
    
    #Отрисовывает игрока на экране
    def draw_player(self):
        if self.sky >= 20:
            player = self.screen.blit(pygame.transform.scale(self.sprite_player1, (80, 80)), (100, self.player_y))
        elif 20 >= self.sky >= 0:
            player = self.screen.blit(pygame.transform.scale(self.sprite_player1, (80, 80)), (100, self.player_y))
        else:
            player = self.screen.blit(pygame.transform.scale(self.sprite_player1, (80, 80)), (100, self.player_y))
        return player
    
    # Проверяет столкновения игрока с колоннами или выход за пределы экрана
    def check_collisions(self, player, columns):
        if player.colliderect(columns[0]) or player.colliderect(columns[1]) \
                or player.colliderect(columns[2]) or player.colliderect(columns[3]):
            self.running = False

        if self.player_y > 720:
            self.running = False
    
    # Отрисовывает счет и рекорд на экране
    def draw_score(self):
        if self.RECORD < self.points:
            self.RECORD = self.points
        self.screen.blit(self.font.render(f"Points: {self.points}", True, self.WHITE), (1100, 50))
        self.screen.blit(self.font.render(f"Record: {self.RECORD}", True, self.WHITE), (1100, 5))

    # Основной игровой цикл
    def game_cycle(self):
        while self.running:
            self.handle_events()
            self.update_player_position()
            self.update_columns_position()

            self.screen.blit(self.sprite_fon, (0, 0))

            columns = self.draw_columns()
            player = self.draw_player()

            self.check_collisions(player, columns)
            self.draw_score()

            pygame.display.update()
            self.clock.tick(30)

        with open(self.RECORD_FILE, "w") as file:
            file.write(str(self.RECORD))

        pygame.quit()

if __name__ == "__main__":
    game = SaveUSA()
    game.game_cycle()