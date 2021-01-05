import sys
import time
from datetime import datetime, timedelta
from random import randint

import pygame
import pygame_menu

from food import Food
from snake import Snake
from wall import Wall


class Game:
    def __init__(self, game_name):
        self.game_name = game_name
        # задаємо розміри екрану
        self.screen_width = 720
        self.screen_height = 460
        self.play_surface = pygame.display.set_mode((
            self.screen_width, self.screen_height))

        # необхідні кольори
        self.red = pygame.Color(255, 0, 0)
        self.green = pygame.Color(0, 255, 0)
        self.black = pygame.Color(0, 0, 0)
        self.white = pygame.Color(255, 255, 255)
        self.brown = pygame.Color(165, 42, 42)

        # задає кількість кадрів в секуну
        self.fps_controller = pygame.time.Clock()

        # змінна для відображення результату
        # (скільки їжі зїли)
        self.score = 0
        pygame.display.set_caption(self.game_name)
        self.snake = Snake(self.green)
        self.food = Food(self.brown, self.screen_width, self.screen_height)
        self.wall = Wall(self.white)
        self.difficulty = 10
        self.ratio = 10
        self.playername = "Gamer"
        self.is_wall = False
        self.wall_start_time = None
        pygame.init()

    def init_menu(self):
        self.menu = pygame_menu.Menu(height=400,
                                     width=600,
                                     theme=pygame_menu.themes.THEME_GREEN,
                                     title=self.game_name)

        self.menu.add_image('Images/snake_menu_hard.png', scale=(0.4, 0.4))
        self.menu.add_text_input('Name: ', default=self.playername, onchange=self.set_playername)
        self.menu.add_selector('Difficulty: ', [('Easy', 1), ('Hard', 2), ('Hell', 3)], onchange=self.set_difficulty)
        self.menu.add_button('Play', self.start_the_game)
        self.menu.add_button('Quit', pygame_menu.events.EXIT)
        self.menu.mainloop(self.play_surface)

    def set_difficulty(self, selected, value):
        """
        Встановіть складність гри.
        """
        if value == 1:
            self.difficulty = 10
            self.ratio = 10

        elif value == 2:
            self.difficulty = 20
            self.ratio = 20
        else:
            self.difficulty = 100
            self.ratio = 50


    def set_playername(self, value):
        self.playername = value

    def start_the_game(self):
        """
        Функція, яка починає гру.
        """
        while True:
            self.snake.change_to = self.event_loop(self.snake.change_to)
            self.snake.validate_direction_and_change()
            self.snake.change_head_position()
            self.score, self.food.food_pos = self.snake.snake_body_mechanism(
                self.score, self.food.food_pos, self.screen_width, self.screen_height)
            self.play_surface.fill(self.black)
            self.snake.draw_snake(self.play_surface)

            self.food.draw_food(self.play_surface)

            if not self.is_wall:
                self.wall_start_time = datetime.now()
                if randint(1, 100) <= self.ratio:
                    self.wall.wall_generation_mechanism(self.screen_width, self.screen_height, self.ratio)
                    if not self.wall.is_snake_in_wall(self.snake.snake_body):
                        self.is_wall = True
                        self.wall.draw_wall(self.play_surface)
                    else:
                        self.wall.wall_body = []
            else:
                self.wall.draw_wall(self.play_surface)
                if datetime.now() >= self.wall_start_time + timedelta(seconds=randint(5, 45)):
                    self.wall.wall_body = []
                    self.is_wall = False

            self.snake.check_for_death(
                self.game_over, self.screen_width, self.screen_height, self.wall)

            self.show_score()
            self.refresh_screen()

    def event_loop(self, change_to):
        """ Функція для відстеження натискань клавіш гравцем """

        # запускаємо цикл по івент
        for event in pygame.event.get():
            # якщо натиснули клавишу
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT or event.key == ord('d'):
                    change_to = "RIGHT"
                elif event.key == pygame.K_LEFT or event.key == ord('a'):
                    change_to = "LEFT"
                elif event.key == pygame.K_UP or event.key == ord('w'):
                    change_to = "UP"
                elif event.key == pygame.K_DOWN or event.key == ord('s'):
                    change_to = "DOWN"
                # натиснули escape
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        return change_to

    def refresh_screen(self):
        """Оновлюємо екран і задаємо фпс """
        pygame.display.flip()
        self.fps_controller.tick(self.difficulty)

    def show_score(self):
        """Відображення результату"""
        pygame.display.set_caption(f"{self.game_name} Score: {self.score}")

    def game_over(self):
        """Функція для виведення напису Game Over і результатів
        в разі завершення гри і вихід з гри"""
        go_font = pygame.font.SysFont('monaco', 72)
        go_surf = go_font.render('Game over', True, self.red)
        go_rect = go_surf.get_rect()
        go_rect.midtop = (360, 15)
        p_font = pygame.font.SysFont('monaco', 40)
        p_surf = p_font.render('Player: {0}'.format(self.playername), True, self.red)
        p_rect = p_surf.get_rect()
        p_rect.midtop = (360, 90)

        s_font = pygame.font.SysFont('monaco', 24)
        s_surf = s_font.render('Score: {0}'.format(self.score), True, self.red)
        s_rect = s_surf.get_rect()
        s_rect.midtop = (360, 120)
        self.play_surface.blit(go_surf, go_rect)
        self.play_surface.blit(p_surf, p_rect)
        self.play_surface.blit(s_surf, s_rect)
        pygame.display.flip()
        time.sleep(3)
        self.restart_game()

    def restart_game(self):
        self.snake.snake_head_pos = [100, 50]
        self.snake.snake_body = [[100, 50], [90, 50], [80, 50]]
        self.snake.direction = "RIGHT"
        self.snake.change_to = self.snake.direction
        self.wall.wall_body = []
        self.is_wall = False
        self.score = 0
        self.init_menu()


if __name__ == '__main__':
    pass