from random import randint

import pygame


class Wall:
    def __init__(self, wall_color):
        self.wall_body = []
        self.wall_color = wall_color

    def wall_generation_mechanism(self, screen_width, screen_height, ratio):
        self.wall_body = []
        for i in range(10, randint(20, 40 * ratio)):
            if len(self.wall_body) == 0:
                self.wall_body.append([randint(1, screen_width / 10) * 10, randint(1, screen_height / 10) * 10])
            else:
                rnd = randint(0, 101)
                if rnd <= 25:
                    self.wall_body.append(
                        [self.wall_body[len(self.wall_body) - 1][0] + 10, self.wall_body[len(self.wall_body) - 1][1]])
                elif 25 < rnd <= 50:
                    self.wall_body.append(
                        [self.wall_body[len(self.wall_body) - 1][0] - 10, self.wall_body[len(self.wall_body) - 1][1]])
                elif 50 < rnd <= 75:
                    self.wall_body.append(
                        [self.wall_body[len(self.wall_body) - 1][0], self.wall_body[len(self.wall_body) - 1][1] + 10])
                else:
                    self.wall_body.append(
                        [self.wall_body[len(self.wall_body) - 1][0], self.wall_body[len(self.wall_body) - 1][1] - 10])

    def draw_wall(self, play_surface):
        for pos in self.wall_body:
            pygame.draw.rect(
                play_surface, self.wall_color, pygame.Rect(
                    pos[0], pos[1], 10, 10))
        #print(self.wall_body)

    def is_snake_in_wall(self, snake_body):
        for i in snake_body:
            for j in self.wall_body:
                if i[0] == j[0] and i[1] == j[1]:
                    return True
                else:
                    return False


if __name__ == '__main__':
    pass