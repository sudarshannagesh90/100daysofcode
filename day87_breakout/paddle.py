from turtle import Turtle
import time

SCREEN_SIZE = 400
TURTLE_SIZE = 20


class Paddle(Turtle):
    def __init__(self, length_of_paddle=11):
        super().__init__()

        self.length_of_paddle = length_of_paddle
        self.list_paddle_objects = []
        self.initialize_paddle()

    def initialize_paddle(self):
        self.list_paddle_objects = []
        p = self.length_of_paddle // 2
        for _ in range(-p, p + 1):
            t = Turtle(shape='square')
            t.color('green')
            t.pu()
            t.speed('fastest')
            t.setpos(_ * TURTLE_SIZE - _,
                     -SCREEN_SIZE // 2 + TURTLE_SIZE - 1)
            self.list_paddle_objects.append(t)

    def move_left(self):
        first_paddle_x = self.list_paddle_objects[0].position()[0]
        if first_paddle_x >= -SCREEN_SIZE // 2 + TURTLE_SIZE - 1:
            for paddle_idx in range(self.length_of_paddle - 1, 0, -1):
                previous_paddle_position = \
                    self.list_paddle_objects[paddle_idx - 1].position()
                self.list_paddle_objects[paddle_idx].setpos(
                    previous_paddle_position)
            self.list_paddle_objects[0].setx(first_paddle_x - TURTLE_SIZE + 1)

    def move_right(self):
        last_paddle_x = self.list_paddle_objects[-1].position()[0]
        if last_paddle_x <= SCREEN_SIZE // 2 - 2 * TURTLE_SIZE + 2:
            for paddle_idx in range(self.length_of_paddle - 1):
                next_paddle_position = \
                    self.list_paddle_objects[paddle_idx + 1].position()
                self.list_paddle_objects[paddle_idx].setpos(
                    next_paddle_position)
            self.list_paddle_objects[-1].setx(last_paddle_x + TURTLE_SIZE - 1)
