from datetime import datetime
import time
from collections import deque
import torch
import random
import pygame
import os
from game_utils import load_image, load_sound, load_music, init_mixer, play_sound
# Переходим в директорию скрипта, чтобы относительные пути работали при запуске напрямую
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

# Добавляем директорию скрипта в sys.path, чтобы импорт honey_bee_torch работал надежно
import sys
if script_dir not in sys.path:
    sys.path.append(script_dir)

try:
    import honey_bee_torch as hbt
except ImportError:
    model = None


class HoneyBeeGame:
    def __init__(self):
        # Инициализация Pygame
        pygame.init()
        init_mixer()

        # Загрузка звуков
        load_music('musik/Teenage Mutant Ninja Turtles 2 — The Arcade Game (NES) Music - Scene 1 (www.lightaudio.ru).mp3')
        self.jump_sound = load_sound('musik/pryijok-v-igre.mp3')

        # Настройки окна
        self.screen = pygame.display.set_mode((1250, 700))
        pygame.display.set_caption('Honey Bee')

        # Загрузка спрайтов
        self.sprite_player1 = load_image('gallery/be_medium.jpg')
        self.sprite_player2 = load_image('gallery/be_up.jpg')
        self.sprite_player3 = load_image('gallery/be_down.jpg')
        self.sprite_fon = load_image('gallery/fon_flappy_be.jpg')
        self.sprite_one = load_image('gallery/one.webp')
        self.sprite_coin = load_image('gallery/coin.jpg')

        self.sprite_column1 = load_image('gallery/honey_down.jpg')
        self.sprite_column2 = load_image('gallery/honey_top.jpg')

        # Игнорирование не нужных цветов
        self.sprite_player1.set_colorkey((0, 0, 0))
        self.sprite_player2.set_colorkey((0, 0, 0))
        self.sprite_player3.set_colorkey((0, 0, 0))
        self.sprite_column1.set_colorkey((0, 0, 0))
        self.sprite_column2.set_colorkey((0, 0, 0))
        self.sprite_coin.set_colorkey((255, 255, 255))

        # Цвета
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)

        # Константы
        self.gravity = 0.5
        self.jump = -10
        self.font = pygame.font.Font(None, 36)
        self.size_column = 450
        self.RECORD_FILE = "records/record_honey_bee.txt"

        if os.path.exists(self.RECORD_FILE):
            with open(self.RECORD_FILE, "r") as file:
                self.RECORD = int(file.read())
        else:
            self.RECORD = 0

    def reset_game(self):
        # Начальные параметры
        self.player_y = 360
        self.player_velocity = 0
        self.sky = 10

        # Позиции колонн и монеты
        self.column_x1 = 1400
        self.column_y1 = random.randint(400, 700)

        self.column_x2 = 1900
        self.column_y2 = random.randint(400, 700)

        self.column_x3 = 2400
        self.column_y3 = random.randint(400, 700)

        self.coin_x = self.column_x2 + 200
        self.coin_y = self.column_y2 - random.randint(-100, 350)

        self.points = 0
        self.running = True

        self.passed_column1 = False
        self.passed_column2 = False
        self.passed_column3 = False

        self.points = 0
        self.running = True
    # Обработка событий
    def handle_events(self, action = None):
        if action == 1:
            self.player_velocity = self.jump
            self.sky = 40
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                    return "toggle_mode"
        return "continue"

    def update_player_position(self):
        self.player_velocity += self.gravity
        self.player_y += self.player_velocity

        if self.player_y < 0:
            self.player_y = 0
            self.player_velocity = 0
    
    # Обновление позиции колонн и монеты
    def update_columns_and_coin(self):
        self.column_x1 -= 10
        self.column_x2 -= 10
        self.column_x3 -= 10
        self.coin_x -= 10
        self.sky -= 1

        # ---- ПРОВЕРКА ПРОЛЕТА ТРУБЫ №1 ----
        # Если труба зашла за птицу (x <= 20) и мы ЕЩЕ НЕ давали за неё очко
        if self.column_x1 <= 20 and not self.passed_column1:
            self.points += 1
            self.passed_column1 = True # Запираем триггер

        if self.column_x1 <= -100:
            self.column_x1 = 1400
            self.column_y1 = random.randint(400, 700)
            self.passed_column1 = False # Сбрасываем флаг для новой трубы


        # ---- ПРОВЕРКА ПРОЛЕТА ТРУБЫ №2 ----
        if self.column_x2 <= 20 and not self.passed_column2:
            self.points += 1
            self.passed_column2 = True

        if self.column_x2 <= -100:
            self.column_x2 = 1400
            self.column_y2 = random.randint(400, 700)
            self.coin_x = self.column_x2 + 200
            self.coin_y = self.column_y2 - random.randint(-100, 350)
            self.passed_column2 = False


        # ---- ПРОВЕРКА ПРОЛЕТА ТРУБЫ №3 ----
        if self.column_x3 <= 20 and not self.passed_column3:
            self.points += 1
            self.passed_column3 = True

        if self.column_x3 <= -100:
            self.column_x3 = 1400
            self.column_y3 = random.randint(400, 700)
            self.points += 1
            self.passed_column3 = False # Тут у тебя в коде был баг (было points+=1 два раза), исправляем на сброс флага
    
    # Проверка столкновений с колоннами
    def check_collisions(self):
        player_rect = pygame.Rect(100, self.player_y, 80, 80)
        columns = [
            pygame.Rect(self.column_x1, self.column_y1, 80, self.size_column),
            pygame.Rect(self.column_x1, self.column_y1 - 700, 80, self.size_column),
            pygame.Rect(self.column_x2, self.column_y2, 80, self.size_column),
            pygame.Rect(self.column_x2, self.column_y2 - 700, 80, self.size_column),
            pygame.Rect(self.column_x3, self.column_y3, 80, self.size_column),
            pygame.Rect(self.column_x3, self.column_y3 - 700, 80, self.size_column)
        ]

        for column in columns:
            if player_rect.colliderect(column):
                return False

        coin_rect = pygame.Rect(self.coin_x, self.coin_y, 50, 50)

        if self.player_y > 720:
            return False

        return True

    # Отрисовка фона
    def draw_objects(self):
        self.screen.blit(self.sprite_fon, (0, 0))

        columns = [
            (self.column_x1, self.column_y1),
            (self.column_x1, self.column_y1 - 700),
            (self.column_x2, self.column_y2),
            (self.column_x2, self.column_y2 - 700),
            (self.column_x3, self.column_y3),
            (self.column_x3, self.column_y3 - 700)
        ]

        for x, y in columns:
            if y > 0:
                self.screen.blit(pygame.transform.scale(self.sprite_column1, (80, self.size_column)), (x, y))
            else:
                self.screen.blit(pygame.transform.scale(self.sprite_column2, (80, self.size_column)), (x, y))

        self.screen.blit(pygame.transform.scale(self.sprite_coin, (50, 50)), (self.coin_x, self.coin_y))

        if self.sky >= 20:
            self.screen.blit(pygame.transform.scale(self.sprite_player2, (80, 80)), (100, self.player_y))
        elif 20 >= self.sky >= 0:
            self.screen.blit(pygame.transform.scale(self.sprite_player1, (80, 80)), (100, self.player_y))
        else:
            self.screen.blit(pygame.transform.scale(self.sprite_player3, (80, 80)), (100, self.player_y))
    
    # Отрисовка счёта
    def draw_score(self):
        if self.RECORD < self.points:
            self.RECORD = self.points
        self.screen.blit(self.font.render(f"Points: {self.points}", True, self.WHITE), (50, 50))
        self.screen.blit(self.font.render(f"Record: {self.RECORD}", True, self.WHITE), (5, 5))

    def game_cycle(self):
        clock = pygame.time.Clock()
        self.reset_game()
        
        local_catched_timer = 0
        training_state = False
        replay_buffer = deque(maxlen=50000)

        if os.path.exists("honeyAIBackup.pth"):
            hbt.learner.load_state_dict(torch.load("honeyAIBackup.pth"))
            hbt.expert.load_state_dict(hbt.learner.state_dict())

        while self.running:
            if training_state:
                #learning sequence
                if self.points == 1000:
                    torch.save(hbt.learner.state_dict(), "honeyAI.pth")
                    training_state = False
                    continue

                if local_catched_timer == 1000:
                    hbt.expert.load_state_dict(hbt.learner.state_dict())
                    local_catched_timer = 0
                
                closest_tube_x = min(filter(lambda x: x > 10, (self.column_x1, self.column_x2, self.column_x3)))
                y_tube_map = {self.column_x1: self.column_y1, self.column_x2: self.column_y2, self.column_x3: self.column_y3}
                closest_tube_y = y_tube_map[closest_tube_x]

                state = [self.player_velocity, closest_tube_x - 100, closest_tube_y - 125 - self.player_y]

                action = torch.argmax(hbt.learner(torch.Tensor(state).to(hbt.device))).item() if random.uniform(0, 1) > hbt.epsilone else 1 if random.randint(1, 30) == 1 else 0
                
                event_result = self.handle_events(action)
                if event_result == "quit":
                    torch.save(hbt.learner.state_dict(), "honeyAIBackup.pth")
                    self.running = False
                elif event_result == "toggle_mode":
                    training_state = False

                self.update_player_position()
                self.update_columns_and_coin()

                if not self.check_collisions():
                    hbt.epsilone = max(0.1, hbt.epsilone * 0.99)
                    next_state = [0, 0, 0]
                    replay_buffer.append([state, hbt.LOOSE_Q, action, next_state, 1])
                    self.backpropagation(replay_buffer)
                    self.reset_game()
                    continue


                self.draw_objects()
                self.draw_score()

                pygame.display.update()
                # Preparing next
                closest_tube_x = min(filter(lambda x: x > 15, (self.column_x1, self.column_x2, self.column_x3)))
                y_tube_map = {self.column_x1: self.column_y1, self.column_x2: self.column_y2, self.column_x3: self.column_y3}
                closest_tube_y = y_tube_map[closest_tube_x]

                next_state = [self.player_velocity, closest_tube_x - 100, closest_tube_y - 125 - self.player_y]
                
                if self.player_y + 80 <= closest_tube_y and self.player_y >= closest_tube_y - 250:
                    replay_buffer.append([state, hbt.TUBE_Q, action, next_state, 0])
                else:
                    replay_buffer.append([state, hbt.FRAME_Q, action, next_state, 0])

                local_catched_timer += 1

                self.backpropagation(replay_buffer)
                clock.tick(0)
            else:
                closest_tube_x = min(filter(lambda x: x > 10, (self.column_x1, self.column_x2, self.column_x3)))
                y_tube_map = {self.column_x1: self.column_y1, self.column_x2: self.column_y2, self.column_x3: self.column_y3}
                closest_tube_y = y_tube_map[closest_tube_x]

                state = [self.player_velocity, closest_tube_x - 100, closest_tube_y - 125 - self.player_y]
                
                action = torch.argmax(hbt.learner(torch.Tensor(state).to(hbt.device))).item()
                
                event_result = self.handle_events(action)
                if event_result == "quit":
                    self.running = False
                elif event_result == "toggle_mode":
                    training_state = True

                self.update_player_position()
                self.update_columns_and_coin()

                if not self.check_collisions():
                    next_state = [0, 0, 0]
                    self.reset_game()
                    continue

                self.draw_objects()
                self.draw_score()

                pygame.display.update()
                clock.tick(0)
        pygame.quit()

    def backpropagation(self, replay_buffer):
        if len(replay_buffer) >= 2000 and len(replay_buffer) % 5 == 0:
            batch = random.sample(replay_buffer, k=hbt.BATCH)
            s, reward, action, sf, done = zip(*batch)
            index_map = torch.Tensor(action).int().reshape(hbt.BATCH, 1).to(hbt.device)
            q_output = torch.gather(hbt.learner(torch.Tensor(s).to(hbt.device)), 1, index_map)
            with torch.no_grad():
                expert_prediction = torch.max(hbt.expert(torch.Tensor(sf).to(hbt.device)), dim=1, keepdim=True)[0]
            q_prediction = torch.Tensor(reward).to(hbt.device).unsqueeze(1) + 0.99 * expert_prediction * (1 - torch.Tensor(done).to(hbt.device).unsqueeze(1))
            loss = hbt.loss_function(q_output, q_prediction)
            loss.backward()
            hbt.optimizer.step()
            hbt.optimizer.zero_grad()

            with open("honeybeeAI.logs", "a") as f:
                print(f"Loss: {loss}, time: {datetime.now().time()}, points: {self.points}", file=f)


game = HoneyBeeGame()
if __name__ == "__main__":
    game.game_cycle()
    