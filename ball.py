import globals as g
import random as r
from turtle import Turtle

BALL_STEP = 20
RANDOM_ANGLE_RANGE = 15


class Ball(Turtle):
    def __init__(self):
        super().__init__()
        self.shape("circle")
        self.color(g.THEME_COLOR[1])
        self.penup()
        self.setheading(r.randint(0, RANDOM_ANGLE_RANGE))

    def move(self):
        self.forward(BALL_STEP)

    def bounce(self, side=False):
        heading = self.heading() + r.randint(0, RANDOM_ANGLE_RANGE)
        if side:
            heading = (360 - heading + 180) % 360
        else:
            heading = 360 - heading

        self.setheading(heading)

    def recenter(self):
        self.goto(0, 0)
        self.setheading(r.randint(0, RANDOM_ANGLE_RANGE))
