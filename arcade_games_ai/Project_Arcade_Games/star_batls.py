import pygame
import random
import os
from game_utils import load_image, load_sound, load_music, init_mixer, play_sound

# Переходим в директорию скрипта, чтобы относительные пути работали при запуске напрямую
os.chdir(os.path.dirname(os.path.abspath(__file__)))

class StarBatlsGame:
    def __init__(self):
        # Инициализация Pygame
        pygame.init()
        init_mixer()

        # Настройки окна
        self.WIDTH, self.HEIGHT = 800, 600
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Star Batls")

        # Цвета
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.RED = (213, 50, 80)

        # Загрузка рекорда из файла
        self.RECORD_FILE = "records/record_star_batls.txt"

        # Загрузка звуков
        load_music("musik/Infinite Game Music — TMNT Arcade - Stage 7 (Konami) (www.lightaudio.ru).mp3")
        self.missile_sound = load_sound("musik/vyibor-nujnoy-klavishi-v-igre-pro-kosmos.mp3")
        self.explosion_sound = load_sound("musik/zvuk-udaleniya.mp3")

        # Загрузка изображений
        self.sprite_player = load_image("gallery/my_ship.png")
        self.sprite_player.set_colorkey((255, 255, 255))
        self.sprite_uly = load_image("gallery/uly.jpg")
        self.sprite_uly.set_colorkey((0, 0, 0))
        self.sprite_missile = load_image("gallery/friend_ray.jpg")
        self.sprite_missile.set_colorkey((255, 255, 255))
        self.sprite_missile_enemy = load_image("gallery/enemy_ray.jpg")
        self.sprite_missile_enemy.set_colorkey((255, 255, 255))
        self.sprite_metior = load_image("gallery/metior.png")
        self.sprite_metior.set_colorkey((255, 255, 255))
        self.sprite_boom = load_image("gallery/boom.png")
        self.sprite_boom.set_colorkey((0, 0, 0))
        self.sprite_fon = load_image("gallery/cosmos.png")

        # Позиция и скорость игрока
        self.player_x = self.WIDTH // 2 - 25
        self.player_y = self.HEIGHT - 60
        self.player_speed = 5
        self.player_rect = pygame.Rect(self.player_x, self.player_y, 60, 60)

        # Списки для хранения объектов
        self.ulys = []
        self.metiorits = []
        self.missils = []
        self.missils_ulys = []
        self.explosions = []

        # Загрузка рекорда
        self.load_record()

        # Счёт
        self.count_points = 0
        self.font = pygame.font.Font(None, 36)
        self.running = True
        self.game_over = False

    def load_record(self):
        if os.path.exists(self.RECORD_FILE):
            with open(self.RECORD_FILE, "r") as file:
                self.record = int(file.read())
        else:
            self.record = 0

    def save_record(self):
        with open(self.RECORD_FILE, "w") as file:
            file.write(str(self.record))

    # Создает врагов
    def spawn_ulys(self, count_spam, speed):
        for _ in range(count_spam):
            uly_x = random.randint(0, self.WIDTH - 50)
            uly_y = random.randint(-100, -50)
            uly_speed = random.randint(speed[0], speed[1])
            uly_rect = pygame.Rect(uly_x, uly_y, 50, 50)
            self.ulys.append([uly_rect, uly_speed])

    # Создает метеориты
    def spawn_metiorits(self, count_spam, speed):
        for _ in range(count_spam):
            metiorits_x = random.randint(0, self.WIDTH - 50)
            metiorits_y = random.randint(-100, -50)
            metiorits_speed = random.randint(speed[0], speed[1])
            metiorits_rect = pygame.Rect(metiorits_x, metiorits_y, 50, 50)
            self.metiorits.append([metiorits_rect, metiorits_speed])

    # Обрабатывает события игры
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    missil_rect = pygame.Rect(self.player_x + 20, self.player_y, 10, 20)
                    self.missils.append(missil_rect)
                    play_sound(self.missile_sound)

    # Обновляет позицию игрока
    def update_player_position(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and self.player_x > 0:
            self.player_x -= self.player_speed
        if keys[pygame.K_d] and self.player_x < self.WIDTH - 50:
            self.player_x += self.player_speed
        if keys[pygame.K_w] and self.player_y > 0:
            self.player_y -= self.player_speed
        if keys[pygame.K_s] and self.player_y < self.HEIGHT - 50:
            self.player_y += self.player_speed
        self.player_rect.topleft = (self.player_x, self.player_y)

    # Обновляет позиции врагов и создает их пули
    def update_ulys(self):
        for ul in self.ulys:
            ul[0].y += ul[1]
            if ul[0].y > self.HEIGHT:
                ul[0].x = random.randint(0, self.WIDTH - 50)
                ul[0].y = random.randint(-100, -50)
                ul[1] = random.randint(2, 5)
            if random.randint(1, 50) == 1:
                missil_ul_rect = pygame.Rect(ul[0].x + 20, ul[0].y + 20, 10, 20)
                self.missils_ulys.append(missil_ul_rect)

    # Обновляет позиции метеоритов
    def update_metiorits(self):
        for metior in self.metiorits:
            metior[0].y += metior[1]
            if metior[0].y > self.HEIGHT:
                metior[0].x = random.randint(0, self.WIDTH - 50)
                metior[0].y = random.randint(-100, -50)
                metior[1] = random.randint(2, 5)

    # Обновляет позиции пуль игрока и врагов
    def update_missils(self):
        for missil in self.missils:
            missil.y -= 10
            if missil.y < 0:
                self.missils.remove(missil)
        for missil_ul in self.missils_ulys:
            missil_ul.y += 7
            if missil_ul.y > self.HEIGHT:
                self.missils_ulys.remove(missil_ul)

    # Проверяет столкновения
    def check_collisions(self):
        for missil in self.missils:
            for ul in self.ulys:
                if ul[0].colliderect(missil):
                    self.explosions.append([ul[0].x, ul[0].y, pygame.time.get_ticks()])
                    self.missils.remove(missil)
                    self.ulys.remove(ul)
                    self.ulys.append([pygame.Rect(random.randint(0, self.WIDTH - 50), random.randint(-100, -50), 50, 50), random.randint(2, 5)])
                    self.count_points += 10
                    play_sound(self.explosion_sound)
            for metior in self.metiorits:
                if metior[0].colliderect(missil):
                    self.explosions.append([metior[0].x, metior[0].y, pygame.time.get_ticks()])
                    self.missils.remove(missil)
                    self.metiorits.remove(metior)
                    self.metiorits.append([pygame.Rect(random.randint(0, self.WIDTH - 50), random.randint(-100, -50), 50, 50), random.randint(2, 5)])
                    self.count_points += 10
                    play_sound(self.explosion_sound)
        for ul in self.ulys:
            if self.player_rect.colliderect(ul[0]):
                self.running = False
        for missil_ul in self.missils_ulys:
            if self.player_rect.colliderect(missil_ul):
                self.running = False
        for metior in self.metiorits:
            if self.player_rect.colliderect(metior[0]):
                self.running = False

    # Отрисовывает все объекты на экране
    def draw_objects(self):
        self.screen.blit(pygame.transform.scale(self.sprite_fon, (self.WIDTH, self.HEIGHT)), (0, 0))
        self.screen.blit(pygame.transform.scale(self.sprite_player, (60, 60)), self.player_rect.topleft)
        for ul in self.ulys:
            self.screen.blit(pygame.transform.scale(self.sprite_uly, (50, 50)), ul[0].topleft)
        for missil_ul in self.missils_ulys:
            self.screen.blit(pygame.transform.scale(self.sprite_missile_enemy, (10, 20)), missil_ul.topleft)
        for missil in self.missils:
            self.screen.blit(pygame.transform.scale(self.sprite_missile, (10, 20)), missil.topleft)
        for metior in self.metiorits:
            self.screen.blit(pygame.transform.scale(self.sprite_metior, (50, 50)), metior[0].topleft)
        current_time = pygame.time.get_ticks()
        for explosion in self.explosions[:]:
            if current_time - explosion[2] < 500:
                self.screen.blit(pygame.transform.scale(self.sprite_boom, (50, 50)), (explosion[0], explosion[1]))
            else:
                self.explosions.remove(explosion)

    # Отрисовывает счет и рекорд на экране
    def draw_score(self):
        if self.count_points > self.record:
            self.record = self.count_points
            self.save_record()
        self.screen.blit(self.font.render(f"Points: {self.count_points}", True, self.WHITE), (50, 50))
        self.screen.blit(self.font.render(f"Record: {self.record}", True, self.WHITE), (5, 5))

    # Отображает экран проигрыша
    def game_over_screen(self):
        with open(self.RECORD_FILE, 'r', encoding='utf8') as file:
            record_star_batls = file.read()
        self.message("Вы проиграли! Нажмите Q-Выход", self.RED, self.WIDTH * 0.1, self.HEIGHT // 2 - 50)
        self.message("или C-Играть снова", self.RED, self.WIDTH * 0.1, self.HEIGHT // 2)
        self.message(f'Ваш счет - {self.count_points}', self.RED, self.WIDTH * 0.1, self.HEIGHT * 0.8)
        self.message(f'Ваш рекорд - {record_star_batls}', self.RED, self.WIDTH * 0.6, self.HEIGHT * 0.8)
        self.message("Чтобы сбросить рекорд нажмите N", self.RED, self.WIDTH * 0.1, self.HEIGHT * 0.7)
        pygame.display.update()

    # Отображает сообщение на экране
    def message(self, msg, color, width_text, height_text):
        font_style = pygame.font.SysFont("bahnschrift", 25)
        mesg = font_style.render(msg, True, color)
        self.screen.blit(mesg, [width_text, height_text])

    # Сбрасывает состояние игры
    def reset_game(self):
        self.player_x = self.WIDTH // 2 - 25
        self.player_y = self.HEIGHT - 60
        self.player_rect = pygame.Rect(self.player_x, self.player_y, 60, 60)
        self.ulys = []
        self.metiorits = []
        self.missils = []
        self.missils_ulys = []
        self.explosions = []
        self.count_points = 0
        self.running = True
        self.game_over = False
        self.spawn_ulys(5, [2, 5])
        self.spawn_metiorits(3, [2, 5])

    # Основной игровой цикл
    def game_cycle(self):
        clock = pygame.time.Clock()
        self.spawn_ulys(5, [2, 5])
        self.spawn_metiorits(3, [2, 5])

        while not self.game_over:
            while self.running:
                self.handle_events()
                self.update_player_position()
                self.update_ulys()
                self.update_metiorits()
                self.update_missils()
                self.check_collisions()
                self.draw_objects()
                self.draw_score()
                pygame.display.update()
                clock.tick(50)

            self.screen.blit(pygame.transform.scale(self.sprite_fon, (self.WIDTH, self.HEIGHT)), (0, 0))
            self.game_over_screen()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        self.game_over = True
                    elif event.key == pygame.K_c:
                        self.reset_game()
                    elif event.key == pygame.K_n:
                        with open(self.RECORD_FILE, 'w', encoding='utf8') as file:
                            file.write(str(0))
                        self.record = 0
                        self.save_record()

        pygame.quit()

if __name__ == "__main__":
    game = StarBatlsGame()
    game.game_cycle()
