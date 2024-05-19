import random
from turtle import Turtle

import numpy as np

SCREEN_SIZE = 400
TURTLE_SIZE = 20
SCREEN_SIZE_2 = SCREEN_SIZE // 2


def check_collision_elements(element1, element2):
    element_position1 = element1.position()
    element_position2 = element2.position()
    if element_position1[1] - TURTLE_SIZE - 1 <= element_position2[1] <= \
            element_position1[1] + TURTLE_SIZE + 1 and \
            element_position1[0] - TURTLE_SIZE + 1 <= element_position2[0] <= \
            element_position1[0] + TURTLE_SIZE - 1:
        return True
    return False


class Ball(Turtle):
    def __init__(self):
        super().__init__()
        self.t = Turtle(shape='square')
        self.t.color('blue')
        self.t.pu()
        self.t.speed('fastest')
        self.delta_x = None
        self.delta_y = None

        self.initialize_ball()

    def initialize_ball(self):
        self.t.setpos(0, -SCREEN_SIZE // 2 + 2 * TURTLE_SIZE)
        self.delta_x = random.choice([-1, 1]) * 3
        self.delta_y = random.randint(1, 5)

    def move_ball(self):
        ball_position = self.t.position()
        self.t.setpos(ball_position[0] + self.delta_x,
                      ball_position[1] + self.delta_y)

    def check_collision_paddle(self, paddle):
        for element in paddle.list_paddle_objects:
            if check_collision_elements(element, self.t):
                self.delta_y = -np.sign(self.delta_y) * random.randint(1, 5)
                break

    def check_collision_wall(self, wall):
        for element in wall.list_wall_objects:
            if check_collision_elements(element, self.t):
                self.delta_y *= -1
                wall.list_wall_objects.remove(element)
                element.hideturtle()
                return wall, len(wall.list_wall_objects) > 0
        ball_position = self.t.position()
        if ball_position[0] <= -SCREEN_SIZE_2 or \
                ball_position[0] >= SCREEN_SIZE_2 - TURTLE_SIZE:
            self.delta_x *= -1
            return wall, len(wall.list_wall_objects) > 0
        if ball_position[1] >= SCREEN_SIZE_2 - 1:
            self.delta_y *= -1
            return wall, len(wall.list_wall_objects) > 0
        if ball_position[1] <= -SCREEN_SIZE_2 + TURTLE_SIZE + 1:
            return wall, False
        return wall, len(wall.list_wall_objects) > 0
