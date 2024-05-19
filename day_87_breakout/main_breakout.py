from turtle import Turtle, Screen
from ball import Ball
from wall import Wall
from paddle import Paddle
import time

s = Screen()
s.bgcolor('black')
s.setup(400, 400)
s.title('Breakout')

ball = Ball()
paddle = Paddle(length_of_paddle=11)
wall = Wall(number_of_rows=5)

s.onkeypress(paddle.move_left, "Left")
s.onkeypress(paddle.move_right, "Right")
s.listen()

game_is_on = True
while game_is_on:
    ball.move_ball()
    ball.check_collision_paddle(paddle)
    wall, game_is_on = ball.check_collision_wall(wall)
    time.sleep(1e-2)
if len(wall.list_wall_objects) > 0:
    wall.game_over(win=False)
else:
    wall.game_over(win=True)
s.mainloop()
