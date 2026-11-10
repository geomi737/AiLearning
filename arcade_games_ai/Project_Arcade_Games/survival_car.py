import pygame
import random
import os
from game_utils import load_image, load_sound, load_music, init_mixer, play_sound

# Переходим в директорию скрипта, чтобы относительные пути работали при запуске напрямую
os.chdir(os.path.dirname(os.path.abspath(__file__)))


class SurvivalCarGame:
    def __init__(self):
        # Инициализация Pygame
        pygame.init()
        init_mixer()

        # Параметры окна
        self.WIDTH, self.HEIGHT = 600, 800
        self.LANE_WIDTH = self.WIDTH // 3
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Car Dodge Game")

        # Загрузка изображений
        self.road_img = load_image("gallery/road.jpg")
        self.road_img = pygame.transform.scale(self.road_img, (self.WIDTH, self.HEIGHT))

        self.player_img = load_image("gallery/black_car.png")
        self.player_img = pygame.transform.scale(self.player_img, (100, 100))
        self.player_img.set_colorkey((255, 255, 255))

        self.obstacle_img = load_image("gallery/green_car.png")
        self.obstacle_img.set_colorkey((255, 255, 255))
        self.obstacle_img = pygame.transform.scale(self.obstacle_img, (60, 100))

        # Загрузка звуков
        load_music("""musik/[cover] T2 - The Arcade Game — Analyzing Performance_Level Complete (by Alexys) (www.lightaudio.ru).mp3""")
        self.move_sound = load_sound("musik/pryijok-v-igre.mp3")
        self.crash_sound = load_sound("musik/d8a048f-8891-4b.mp3")

        # Шрифты
        self.font = pygame.font.Font(None, 36)

        # Игровые переменные
        self.player_lane = 1
        self.player_y = self.HEIGHT - 150
        self.obstacle_speed = 5
        self.spawn_delay = 60
        self.record_score = 0
    
    # Обработка событий
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if not self.game_over:
                    if event.key == pygame.K_LEFT and self.player_lane > 0:
                        self.player_lane -= 1
                        play_sound(self.move_sound)
                    if event.key == pygame.K_RIGHT and self.player_lane < 2:
                        self.player_lane += 1
                        play_sound(self.move_sound)
                else:
                    if event.key == pygame.K_r:
                        return "restart"
                    if event.key == pygame.K_q:
                        return False
        return True
    
    # Спавн машин-препятствий
    def spawn_obstacles(self):
        self.spawn_timer += 1
        if self.spawn_timer > self.spawn_delay:
            available_lanes = [0, 1, 2]
            num_obstacles = random.choice([1, 2])
            random.shuffle(available_lanes)

            for i in range(num_obstacles):
                lane = available_lanes[i]
                lane_x = lane * self.LANE_WIDTH + (self.LANE_WIDTH - 60) // 2
                self.obstacles.append(pygame.Rect(lane_x, -100 - random.randint(50, 300), 60, 100))

            self.spawn_timer = 0

    # Обновление позиций машин
    def update_obstacles(self):
        for obs in self.obstacles[:]:
            obs.y += self.obstacle_speed
            if obs.y > self.HEIGHT:
                self.obstacles.remove(obs)
    
    # Проверка на столкновение
    def check_collisions(self):    
        player_x = self.player_lane * self.LANE_WIDTH + (self.LANE_WIDTH - 60) // 2
        player_rect = pygame.Rect(player_x, self.player_y, 60, 100)
        for obs in self.obstacles:
            if player_rect.colliderect(obs):
                self.game_over = True
                play_sound(self.crash_sound)
                if self.score > self.record_score:
                    self.record_score = self.score
    
    # Отрисовка объектов
    def draw_objects(self):
        self.screen.blit(self.road_img, (0, 0))
        self.screen.blit(self.player_img, (self.player_lane * self.LANE_WIDTH + (self.LANE_WIDTH - 60) // 2, self.player_y))
        for obs in self.obstacles:
            self.screen.blit(self.obstacle_img, (obs.x, obs.y))
    
    # Отрисовка счета
    def draw_score(self):
        score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        record_text = self.font.render(f"Record: {self.record_score}", True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(record_text, (10, 40))
    
    # Отрисовка меню после смерти
    def draw_game_over(self):
        game_over_text = self.font.render("Game Over!", True, (0, 0, 0))
        final_score_text = self.font.render(f"Final Score: {self.score}", True, (0, 0, 0))
        restart_text = self.font.render("Press R to Restart, Q to Quit", True, (0, 0, 0))
        self.screen.blit(game_over_text, (self.WIDTH // 2 - 80, self.HEIGHT // 2 - 50))
        self.screen.blit(final_score_text, (self.WIDTH // 2 - 100, self.HEIGHT // 2))
        self.screen.blit(restart_text, (self.WIDTH // 2 - 160, self.HEIGHT // 2 + 50))
    
    # Основной игровой цикл
    def run_game(self):
        self.player_lane = 1
        self.obstacles = []
        self.spawn_timer = 0
        self.score = 0
        self.score_timer = 0
        self.game_over = False
        self.running = True

        clock = pygame.time.Clock()
        
        while self.running:
            event_result = self.handle_events()
            if event_result == "restart":
                return self.run_game()
            elif not event_result:
                break

            if not self.game_over:
                self.score_timer += 1
                if self.score_timer % 10 == 0:
                    self.score += 1

                self.spawn_obstacles()
                self.update_obstacles()
                self.check_collisions()

            self.draw_objects()
            self.draw_score()

            if self.game_over:
                self.draw_game_over()

            pygame.display.flip()
            clock.tick(30)

        pygame.quit()

if __name__ == "__main__":
    game = SurvivalCarGame()
    game.run_game()