import random

import pygame


class Snake:
    def __init__(self, snake_color):
        # важливі змінні - позиція голови змії і його тіла
        self.snake_head_pos = [100, 50]  # [x, y]
        # початкове тіло змії складається з трьох сегментів
        # голова змії - перший елемент, хвіст - останній
        self.snake_body = [[100, 50], [90, 50], [80, 50]]
        self.snake_color = snake_color
        # напрямок рух змії, спочатку
        # задамося вправо
        self.direction = "RIGHT"
        # куди буде змінюватися напрвление руху змії
        # при натисканні відповідних клавіш
        self.change_to = self.direction

    def validate_direction_and_change(self):
        """Змінюємо напрямок руху змії тільки в тому випадку,
        якщо воно не прямо протилежно поточному"""
        if any((self.change_to == "RIGHT" and not self.direction == "LEFT",
                self.change_to == "LEFT" and not self.direction == "RIGHT",
                self.change_to == "UP" and not self.direction == "DOWN",
                self.change_to == "DOWN" and not self.direction == "UP")):
            self.direction = self.change_to

    def change_head_position(self):
        """Змінюємо положення голови змії"""
        if self.direction == "RIGHT":
            self.snake_head_pos[0] += 10
        elif self.direction == "LEFT":
            self.snake_head_pos[0] -= 10
        elif self.direction == "UP":
            self.snake_head_pos[1] -= 10
        elif self.direction == "DOWN":
            self.snake_head_pos[1] += 10

    def snake_body_mechanism(self, score, food_pos, screen_width, screen_height):
        self.snake_body.insert(0, list(self.snake_head_pos))
        if (self.snake_head_pos[0] == food_pos[0] and
                self.snake_head_pos[1] == food_pos[1]):
            food_pos = [random.randrange(1, screen_width / 10) * 10,
                        random.randrange(1, screen_height / 10) * 10]
            score += 10
        else:
            self.snake_body.pop()
        return score, food_pos

    def draw_snake(self, play_surface):
        """Відображаємо всі сегменти змії"""
        for pos in self.snake_body:
            pygame.draw.rect(
                play_surface, self.snake_color, pygame.Rect(
                    pos[0], pos[1], 10, 10))

    def check_for_death(self, game_over, screen_width, screen_height, wall):
        """
         Перевірка, що зіткнулися з кінцями екрану або самі з собою
        (Змія закільцювалася)"""
        if any((
                self.snake_head_pos[0] > screen_width - 10
                or self.snake_head_pos[0] < 0,
                self.snake_head_pos[1] > screen_height - 10
                or self.snake_head_pos[1] < 0,
        )):
            game_over()
        if self.snake_head_pos in wall.wall_body:
            game_over()

        if self.snake_head_pos in self.snake_body[1:]:
            game_over()



if __name__ == '__main__':
    pass