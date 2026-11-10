import pygame
import os
from PIL import Image
import random
from game_utils import load_image, load_sound, init_mixer, play_sound

# Переходим в директорию скрипта, чтобы относительные пути работали при запуске напрямую
os.chdir(os.path.dirname(os.path.abspath(__file__)))

class PacmanGame:
    def __init__(self, parent=None):
        self.parent = parent
        pygame.init()
        init_mixer()

        # Константы
        self.TILE_SIZE = 30
        self.SPEED = 2
        self.ENEMY_SPEED = 2
        self.FPS = 60

        # Лабиринт
        self.maze = [
            "1111111111111111111111111111",
            "1000000000110000000000000001",
            "1011110110110110110111111101",
            "1011110110110110110111111101",
            "1000000000000000000000000001",
            "1011110111011111011101111101",
            "1000000111000000001110000001",
            "1111010111011111011101111101",
            "3000010000000000000010000003",
            "1111010110110110110111111101",
            "1000000111000000001110000001",
            "1011110110110110110111111101",
            "1011110110110110110111111101",
            "1000000000110000000000000001",
            "1011110111011111011101111101",
            "1000000111000000001110000001",
            "1111010110110110110111111101",
            "1111010000000000000010000001",
            "1111010110110110110111111101",
            "1000000000000000000000000001",
            "1011110110110110110111111101",
            "1000000111000000001110000001",
            "1011110110110110110111111101",
            "1000000000000000000000000001",
            "1011110111011111011101111101",
            "1000000111000000001110000001",
            "1111111111111111111111111111",
        ]

        # Размеры экрана
        self.WIDTH = len(self.maze[0]) * self.TILE_SIZE
        self.HEIGHT = len(self.maze) * self.TILE_SIZE

        # Цвета
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.BLUE = (0, 0, 255)
        self.YELLOW = (255, 255, 0)

        # Создание окна
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Pac-Man")

        # Звук
        self.waka_sound = load_sound(os.path.join("musik", "pacman_waka.mp3"))
        if self.waka_sound:
            self.waka_sound.set_volume(0.3)

        # Анимация Пакмена и призраков
        self.pacman_frames = self.load_frames_from_gif(os.path.join("gallery", "pacman.gif"), frame_count=4)
        self.ghost_frames = self.load_frames_from_gif(os.path.join("gallery", "ghost.gif"), frame_count=4)
        self.ghost2_frames = self.load_frames_from_gif(os.path.join("gallery", "ghost2.gif"), frame_count=4)
        self.ghost3_frames = self.load_frames_from_gif(os.path.join("gallery", "ghost3.gif"), frame_count=4)
        self.ghost4_frames = self.load_frames_from_gif(os.path.join("gallery", "ghost4.gif"), frame_count=4)
        self.deadly_ghost_frames = self.load_frames_from_gif(os.path.join("gallery", "deadly_ghost.gif"), frame_count=4)

        # Начальные параметры
        self.pacman_direction = "LEFT"
        self.pacman_frame_index = 0
        self.animation_counter = 0
        self.animation_speed = 5
        self.pacman_x, self.pacman_y = self.TILE_SIZE, 8 * self.TILE_SIZE

        # Точки и мега шарики
        self.dots = {(col * self.TILE_SIZE + self.TILE_SIZE // 2, row * self.TILE_SIZE + self.TILE_SIZE // 2)
                     for row, line in enumerate(self.maze) for col, cell in enumerate(line) if cell == "0"}
        self.mega_dots = {(5 * self.TILE_SIZE + self.TILE_SIZE // 2, 5 * self.TILE_SIZE + self.TILE_SIZE // 2),
                          (15 * self.TILE_SIZE + self.TILE_SIZE // 2, 10 * self.TILE_SIZE + self.TILE_SIZE // 2)}

        # Счёт и состояние уязвимости
        self.score = 0
        self.font = pygame.font.Font(None, 36)
        self.vulnerable_mode = False
        self.vulnerable_timer = 0

    def load_frames_from_gif(self, gif_path, frame_count=4):
        try:
            gif = Image.open(gif_path)
            frames = {"LEFT": [], "RIGHT": [], "UP": [], "DOWN": []}

            for frame in range(frame_count):
                gif.seek(frame)
                frame_image = gif.convert("RGBA")
                frame_pygame = pygame.image.fromstring(frame_image.tobytes(), gif.size, "RGBA")
                frame_pygame = pygame.transform.scale(frame_pygame, (self.TILE_SIZE, self.TILE_SIZE))

                frames["LEFT"].append(frame_pygame)
                frames["RIGHT"].append(pygame.transform.flip(frame_pygame, True, False))
                frames["UP"].append(pygame.transform.rotate(frame_pygame, -90))
                frames["DOWN"].append(pygame.transform.rotate(frame_pygame, 90))

            return frames

        except EOFError:
            gif = Image.open(gif_path)
            frame_image = gif.convert("RGBA")
            frame_pygame = pygame.image.fromstring(frame_image.tobytes(), gif.size, "RGBA")
            frame_pygame = pygame.transform.scale(frame_pygame, (self.TILE_SIZE, self.TILE_SIZE))

            frames = {"LEFT": [frame_pygame], "RIGHT": [pygame.transform.flip(frame_pygame, True, False)],
                      "UP": [pygame.transform.rotate(frame_pygame, -90)], "DOWN": [pygame.transform.rotate(frame_pygame, 90)]}

            return frames

    def check_tunnel(self, x, y):
        if x < 0:
            return self.WIDTH - self.TILE_SIZE, y
        elif x > self.WIDTH - self.TILE_SIZE:
            return 0, y
        return x, y

    def draw_maze(self):
        for row_idx, row in enumerate(self.maze):
            for col_idx, cell in enumerate(row):
                x, y = col_idx * self.TILE_SIZE, row_idx * self.TILE_SIZE

                if cell == "1":
                    pygame.draw.rect(self.screen, self.BLACK, (x, y, self.TILE_SIZE, self.TILE_SIZE))

                    top = row_idx > 0 and self.maze[row_idx - 1][col_idx] == "1" if row_idx > 0 else False
                    bottom = row_idx < len(self.maze) - 1 and self.maze[row_idx + 1][col_idx] == "1" if row_idx < len(self.maze) - 1 else False
                    left = col_idx > 0 and self.maze[row_idx][col_idx - 1] == "1" if col_idx > 0 else False
                    right = col_idx < len(row) - 1 and self.maze[row_idx][col_idx + 1] == "1" if col_idx < len(row) - 1 else False

                    pygame.draw.rect(self.screen, self.BLACK, (x, y, self.TILE_SIZE, self.TILE_SIZE))

                    if not top:
                        pygame.draw.line(self.screen, self.BLUE, (x, y), (x + self.TILE_SIZE, y), 2)
                    if not bottom:
                        pygame.draw.line(self.screen, self.BLUE, (x, y + self.TILE_SIZE), (x + self.TILE_SIZE, y + self.TILE_SIZE), 2)
                    if not left:
                        pygame.draw.line(self.screen, self.BLUE, (x, y), (x, y + self.TILE_SIZE), 2)
                    if not right:
                        pygame.draw.line(self.screen, self.BLUE, (x + self.TILE_SIZE, y), (x + self.TILE_SIZE, y + self.TILE_SIZE), 2)

    def can_move(self, x, y):
        pacman_rect = pygame.Rect(x + 5, y + 5, self.TILE_SIZE - 5, self.TILE_SIZE - 5)

        if x < 0 or x >= self.WIDTH or y < 0 or y >= self.HEIGHT:
            return False

        walls = []
        for row, line in enumerate(self.maze):
            for col, cell in enumerate(line):
                if cell == "1":
                    wall_rect = pygame.Rect(col * self.TILE_SIZE, row * self.TILE_SIZE, self.TILE_SIZE, self.TILE_SIZE)
                    walls.append(wall_rect)

        for wall in walls:
            if pacman_rect.colliderect(wall):
                return False
        return True

    def check_for_dots(self):
        pacman_center = (self.pacman_x + self.TILE_SIZE // 2, self.pacman_y + self.TILE_SIZE // 2)
        for dot in list(self.dots):
            if pygame.Rect(dot[0] - 4, dot[1] - 4, 8, 8).collidepoint(pacman_center):
                self.dots.remove(dot)
                self.score += 1
                play_sound(self.waka_sound)

    def check_for_mega_dots(self):
        pacman_center = (self.pacman_x + self.TILE_SIZE // 2, self.pacman_y + self.TILE_SIZE // 2)

        for dot in list(self.mega_dots):
            if pygame.Rect(dot[0] - 8, dot[1] - 8, 16, 16).collidepoint(pacman_center):
                self.mega_dots.remove(dot)
                self.vulnerable_mode = True
                self.vulnerable_timer = 500
                play_sound(self.waka_sound)

    def update_vulnerability(self):
        if self.vulnerable_mode:
            self.vulnerable_timer -= 1
            if self.vulnerable_timer <= 0:
                self.vulnerable_mode = False

    def create_intersections(self):
        intersections = {}
        for row_idx, row in enumerate(self.maze):
            for col_idx, cell in enumerate(row):
                if cell == "0":
                    x, y = col_idx * self.TILE_SIZE, row_idx * self.TILE_SIZE
                    directions = []
                    if self.can_move(x - self.TILE_SIZE, y):
                        directions.append("LEFT")
                    if self.can_move(x + self.TILE_SIZE, y):
                        directions.append("RIGHT")
                    if self.can_move(x, y - self.TILE_SIZE):
                        directions.append("UP")
                    if self.can_move(x, y + self.TILE_SIZE):
                        directions.append("DOWN")
                    if directions:
                        intersections[(x, y)] = directions
        return intersections

    class Ghost:
        def __init__(self, x, y, color, game):
            self.x = x
            self.y = y
            self.color = color
            self.direction = "LEFT"
            self.speed = game.ENEMY_SPEED
            self.ghost_frame_index = 0
            self.target_x = x
            self.target_y = y
            self.game = game

        def chase_pacman(self, pacman_x, pacman_y, intersections):
            dx = pacman_x - self.x
            dy = pacman_y - self.y

            if (self.x, self.y) in intersections:
                directions = intersections[(self.x, self.y)]
                random.shuffle(directions)

                for direction in directions:
                    if direction == "LEFT" and self.game.can_move(self.x - self.game.TILE_SIZE, self.y):
                        self.target_x = self.x - self.game.TILE_SIZE
                        self.target_y = self.y
                        self.direction = "LEFT"
                        return
                    elif direction == "RIGHT" and self.game.can_move(self.x + self.game.TILE_SIZE, self.y):
                        self.target_x = self.x + self.game.TILE_SIZE
                        self.target_y = self.y
                        self.direction = "RIGHT"
                        return
                    elif direction == "UP" and self.game.can_move(self.x, self.y - self.game.TILE_SIZE):
                        self.target_x = self.x
                        self.target_y = self.y - self.game.TILE_SIZE
                        self.direction = "UP"
                        return
                    elif direction == "DOWN" and self.game.can_move(self.x, self.y + self.game.TILE_SIZE):
                        self.target_x = self.x
                        self.target_y = self.y + self.game.TILE_SIZE
                        self.direction = "DOWN"
                        return

            self.direction = "LEFT"

        def move(self):
            if self.x < self.target_x:
                self.x = min(self.x + self.speed, self.target_x)
            elif self.x > self.target_x:
                self.x = max(self.x - self.speed, self.target_x)

            if self.y < self.target_y:
                self.y = min(self.y + self.speed, self.target_y)
            elif self.y > self.target_y:
                self.y = max(self.y - self.speed, self.target_y)

            self.ghost_frame_index = (self.ghost_frame_index + 1) % 4

        def draw(self, screen):
            if self.game.vulnerable_mode:
                frames = self.game.deadly_ghost_frames[self.direction]
            else:
                if self.color == "red":
                    frames = self.game.ghost_frames[self.direction]
                elif self.color == "pink":
                    frames = self.game.ghost2_frames[self.direction]
                elif self.color == "blue":
                    frames = self.game.ghost3_frames[self.direction]
                elif self.color == "orange":
                    frames = self.game.ghost4_frames[self.direction]
                else:
                    frames = self.game.ghost_frames[self.direction]

            if len(frames) > self.ghost_frame_index:
                ghost_frame = frames[self.ghost_frame_index]
            else:
                ghost_frame = frames[0]

            screen.blit(ghost_frame, (self.x, self.y))

    def start_game(self):
        print("Start game method called.")
        running = True
        clock = pygame.time.Clock()

        intersections = self.create_intersections()

        ghosts = [
            self.Ghost(13 * self.TILE_SIZE, 11 * self.TILE_SIZE, "red", self) if self.can_move(13 * self.TILE_SIZE, 11 * self.TILE_SIZE) else self.Ghost(self.TILE_SIZE, self.TILE_SIZE, "red", self),
            self.Ghost(14 * self.TILE_SIZE, 11 * self.TILE_SIZE, "pink", self) if self.can_move(14 * self.TILE_SIZE, 11 * self.TILE_SIZE) else self.Ghost(self.TILE_SIZE, self.TILE_SIZE, "pink", self),
            self.Ghost(15 * self.TILE_SIZE, 11 * self.TILE_SIZE, "blue", self) if self.can_move(15 * self.TILE_SIZE, 11 * self.TILE_SIZE) else self.Ghost(self.TILE_SIZE, self.TILE_SIZE, "blue", self),
            self.Ghost(16 * self.TILE_SIZE, 11 * self.TILE_SIZE, "orange", self) if self.can_move(16 * self.TILE_SIZE, 11 * self.TILE_SIZE) else self.Ghost(self.TILE_SIZE, self.TILE_SIZE, "orange", self)
        ]

        moving_direction = self.pacman_direction
        x_velocity = 0
        y_velocity = 0

        while running:
            self.screen.fill(self.BLACK)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT and self.can_move(self.pacman_x - self.TILE_SIZE, self.pacman_y):
                        moving_direction = "LEFT"
                        x_velocity = -self.SPEED
                        y_velocity = 0
                    elif event.key == pygame.K_RIGHT and self.can_move(self.pacman_x + self.TILE_SIZE, self.pacman_y):
                        moving_direction = "RIGHT"
                        x_velocity = self.SPEED
                        y_velocity = 0
                    elif event.key == pygame.K_UP and self.can_move(self.pacman_x, self.pacman_y - self.TILE_SIZE):
                        moving_direction = "UP"
                        x_velocity = 0
                        y_velocity = -self.SPEED
                    elif event.key == pygame.K_DOWN and self.can_move(self.pacman_x, self.pacman_y + self.TILE_SIZE):
                        moving_direction = "DOWN"
                        x_velocity = 0
                        y_velocity = self.SPEED

            self.pacman_x += x_velocity
            self.pacman_y += y_velocity

            if not self.can_move(self.pacman_x, self.pacman_y):
                self.pacman_x -= x_velocity
                self.pacman_y -= y_velocity

            self.pacman_x, self.pacman_y = self.check_tunnel(self.pacman_x, self.pacman_y)

            self.check_for_dots()
            self.check_for_mega_dots()
            self.update_vulnerability()

            for ghost in ghosts:
                ghost.chase_pacman(self.pacman_x, self.pacman_y, intersections)
                ghost.move()
                ghost.draw(self.screen)
                ghost.x, ghost.y = self.check_tunnel(ghost.x, ghost.y)

            pacman_rect = pygame.Rect(self.pacman_x, self.pacman_y, self.TILE_SIZE, self.TILE_SIZE)
            for ghost in ghosts:
                ghost_rect = pygame.Rect(ghost.x, ghost.y, self.TILE_SIZE, self.TILE_SIZE)
                if pacman_rect.colliderect(ghost_rect):
                    if self.vulnerable_mode:
                        print("Вы съели призрака!")
                        ghost.x, ghost.y = 0, 0
                    else:
                        print("ВЫ проиграли!")
                        running = False

            self.animation_counter += 1
            if self.animation_counter >= self.animation_speed:
                self.pacman_frame_index = (self.pacman_frame_index + 1) % 4
                self.animation_counter = 0

            self.draw_maze()
            for dot in self.mega_dots:
                pygame.draw.circle(self.screen, self.YELLOW, dot, 12)

            for dot in self.dots:
                pygame.draw.circle(self.screen, self.WHITE, dot, 4)

            self.screen.blit(self.pacman_frames[moving_direction][self.pacman_frame_index], (self.pacman_x, self.pacman_y))

            score_text = self.font.render(f"Score: {self.score}", True, self.WHITE)
            self.screen.blit(score_text, (10, 10))

            pygame.display.flip()
            clock.tick(self.FPS)

        pygame.quit()
        if self.parent:
            self.parent.show()


if __name__ == "__main__":
    game = PacmanGame()
    game.start_game()