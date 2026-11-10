import pygame
import random
import os
from game_utils import load_image, load_sound, load_music, init_mixer, play_sound

# Переходим в директорию скрипта, чтобы относительные пути работали при запуске напрямую
os.chdir(os.path.dirname(os.path.abspath(__file__)))

class SnakeGame:
    def __init__(self):
        # Инициализация Pygame
        pygame.init()
        init_mixer()

        # Цвета
        self.BLACK = (0, 0, 0)
        self.YELLOW = (255, 255, 102)
        self.RED = (213, 50, 80)
        self.GREEN = (0, 255, 0)
        self.BLUE = (50, 153, 213)

        # Размеры окна
        self.WIDTH = 800
        self.HEIGHT = 600

        # Создание окна
        self.game_window = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption('Змейка')

        # Часы для управления скоростью игры
        self.clock = pygame.time.Clock()

        # Размер блока змейки и скорость змейки
        self.BLOCK_SIZE = 25
        self.SNAKE_SPEED = 10

        # Шрифты
        self.font_style = pygame.font.SysFont("bahnschrift", 25)
        self.score_font = pygame.font.SysFont("comicsansms", 35)

        # Загрузка изображений
        self.food_image = load_image("gallery/apple.png")
        self.sprite_fon = load_image("gallery/sneip_fon.jpg")
        # Масштабируем изображение под размеры
        self.food_image = pygame.transform.scale(self.food_image, (self.BLOCK_SIZE, self.BLOCK_SIZE))
        self.sprite_fon = pygame.transform.scale(self.sprite_fon, (self.WIDTH, self.HEIGHT))

        # Загрузка звуков
        self.eat_sound = load_sound('musik/eating_song.mp3')
        load_music('musik/Julian Cha — Arcade Game Music Type Beat (www.lightaudio.ru).mp3')

    def your_score(self, score):
        value = self.score_font.render("Ваш счет: " + str(score), True, self.BLUE)
        self.game_window.blit(value, [0, 0])

    def our_snake(self, block_size, snake_list):
        for x in snake_list:
            pygame.draw.ellipse(self.game_window, self.BLUE, [x[0], x[1], block_size, block_size])

    def message(self, msg, color, width_text, height_text):
        mesg = self.font_style.render(msg, True, color)
        self.game_window.blit(mesg, [width_text, height_text])

    def generate_food(self):
        return (
            round(random.randrange(0, self.WIDTH - self.BLOCK_SIZE) / self.BLOCK_SIZE) * self.BLOCK_SIZE,
            round(random.randrange(0, self.HEIGHT - self.BLOCK_SIZE) / self.BLOCK_SIZE) * self.BLOCK_SIZE
        )

    def handle_events(self, x1_change, y1_change):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True, x1_change, y1_change
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    return False, -self.BLOCK_SIZE, 0
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    return False, self.BLOCK_SIZE, 0
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    return False, 0, -self.BLOCK_SIZE
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    return False, 0, self.BLOCK_SIZE
        return False, x1_change, y1_change

    def game_over_screen(self, length_of_snake):
        with open('records/record_sneip.txt', 'r', encoding='utf8') as file:
            record_snake = file.read()
        self.message("Вы проиграли! Нажмите Q-Выход", self.RED, self.WIDTH * 0.1, self.HEIGHT // 2 - 50)
        self.message("или C-Играть снова", self.RED, self.WIDTH * 0.1, self.HEIGHT // 2)
        self.message(f'Ваш счет - {length_of_snake - 1}', self.RED, self.WIDTH * 0.1, self.HEIGHT * 0.8)
        self.message(f'Ваш рекорд - {record_snake}', self.RED, self.WIDTH * 0.6, self.HEIGHT * 0.8)
        self.message("Чтобы сбросить рекорд нажмите N", self.RED, self.WIDTH * 0.1, self.HEIGHT * 0.7)
        self.your_score(length_of_snake - 1)
        pygame.display.update()

    def game_loop(self):
        game_over = False
        game_close = False

        x1 = self.WIDTH / 2
        y1 = self.HEIGHT / 2

        x1_change = 0
        y1_change = 0

        snake_list = []
        length_of_snake = 1

        food_x, food_y = self.generate_food()

        while not game_over:
            while game_close:
                self.game_window.blit(self.sprite_fon, (0, 0))
                self.game_over_screen(length_of_snake)

                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            game_over = True
                            game_close = False
                        elif event.key == pygame.K_c:
                            self.game_loop()
                        elif event.key == pygame.K_n:
                            with open('records/record_sneip.txt', 'w', encoding='utf8') as file:
                                file.write(str(0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        x1_change = -self.BLOCK_SIZE
                        y1_change = 0
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        x1_change = self.BLOCK_SIZE
                        y1_change = 0
                    elif event.key == pygame.K_UP or event.key == pygame.K_w:
                        y1_change = -self.BLOCK_SIZE
                        x1_change = 0
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        y1_change = self.BLOCK_SIZE
                        x1_change = 0

            if x1 >= self.WIDTH or x1 < 0 or y1 >= self.HEIGHT or y1 < 0:
                game_close = True

            x1 += x1_change
            y1 += y1_change
            self.game_window.blit(self.sprite_fon, (0, 0))
            self.game_window.blit(self.food_image, (food_x, food_y))

            snake_head = [x1, y1]
            snake_list.append(snake_head)
            if len(snake_list) > length_of_snake:
                del snake_list[0]

            for x in snake_list[:-1]:
                if x == snake_head:
                    game_close = True

            self.our_snake(self.BLOCK_SIZE, snake_list)
            self.your_score(length_of_snake - 1)
            pygame.display.update()

            if x1 == food_x and y1 == food_y:
                food_x, food_y = self.generate_food()
                length_of_snake += 1
                play_sound(self.eat_sound)

            self.clock.tick(self.SNAKE_SPEED)

            with open('records/record_sneip.txt', 'r+', encoding='utf8') as file:
                if int(file.read()) < length_of_snake - 1:
                    file.seek(0)
                    file.write(str(length_of_snake - 1))

        pygame.quit()
        quit()

# Запуск игры
if __name__ == "__main__":
    game = SnakeGame()
    game.game_loop()