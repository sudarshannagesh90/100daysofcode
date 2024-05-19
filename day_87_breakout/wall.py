from turtle import Turtle
SCREEN_SIZE = 400
TURTLE_SIZE = 20

class Wall(Turtle):
    def __init__(self, number_of_rows=5):
        super().__init__()
        self.number_of_rows = number_of_rows
        self.list_wall_objects = []
        self.initialize_wall()

    def initialize_wall(self):
        self.list_wall_objects = []
        p = (SCREEN_SIZE // 2 - TURTLE_SIZE // 2) // (TURTLE_SIZE - 1)
        for row_idx in range(self.number_of_rows):
            for x in range(-p, p + 1):
                t = Turtle(shape='square')
                t.speed('fastest')
                t.pu()
                t.color('red')
                t.setpos(x * TURTLE_SIZE - x, row_idx * TURTLE_SIZE - row_idx)
                self.list_wall_objects.append(t)

    def game_over(self, win=False):
        t = Turtle()
        t.setpos(0, 0)
        t.color('White')
        t.hideturtle()
        if win:
            t.write("You win!", align='center', font=('Courier', 20, 'normal'))
        else:
            t.write('Game-over', align='center', font=('Courier', 20, 'normal'))
