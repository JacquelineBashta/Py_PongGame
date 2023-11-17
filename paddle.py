from turtle import Turtle
import globals as g

PADDLE_SIZE = 100  # number of paddle parts, more is easier
# PADDLE_SHAPE_SIZE = 100
PADDLE_STEP = 20


class Paddle(Turtle):
    def __init__(self, loc) -> None:
        super().__init__()

        self.shape("square")
        self.shapesize(1, PADDLE_SIZE/20)
        self.penup()
        self.setheading(g.UP)
        if loc == g.RIGHT:
            self.goto(g.RIGHT_LIMIT - 30, 0)
        else:
            self.goto(g.LEFT_LIMIT + 30, 0)
        self.color(g.THEME_COLOR[1])

    def get_position(self):
        x = self.xcor()
        ymax = self.ycor() + PADDLE_SIZE/2
        ymin = self.ycor() - PADDLE_SIZE/2
        return (x, ymax, ymin)

    def adapt_y(self, y_target):
        _, ymax, ymin = self.get_position()
        if not g.is_between(y_target, ymin, ymax):
            if y_target < ymin:
                self.down()
            else:
                self.up()

    def up(self):
        if self.get_position()[1] < g.UPPER_LIMIT:
            self.setheading(g.UP)
            self.forward(PADDLE_STEP)

    def down(self):
        if self.get_position()[2] > g.LOWER_LIMIT:
            self.setheading(g.DOWN)
            self.forward(PADDLE_STEP)
