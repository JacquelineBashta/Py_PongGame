from turtle import Turtle
import globals as g

PADDLE_SIZE = 3  # number of paddle parts, more is easier
# PADDLE_SHAPE_SIZE = 100
PADDLE_STEP = 20


class Paddle:
    def __init__(self, loc) -> None:
        self.paddle: list[Turtle] = []
        self._create_paddle_parts(PADDLE_SIZE, loc)

    def _create_paddle_parts(self, num_parts, location):

        part = Turtle("square")
        part.penup()
        if location == g.RIGHT:
            part.goto(g.RIGHT_LIMIT - 50, 0)
        else:
            part.goto(g.LEFT_LIMIT + 50, 0)
        part.color(g.THEME_COLOR[1])
        self.paddle.append(part)
        for _ in range(num_parts-1):
            part = self.paddle[-1].clone()
            part.sety(part.ycor() - 20)  # parts added under first part
            self.paddle.append(part)

    def get_position(self):
        pos_1 = self.paddle[0].position()
        pos_2 = self.paddle[-1].position()
        # x1,     ymax,       ymin
        return (pos_1[0], pos_1[1], pos_2[1])

    def sety(self, y_target):
        _, ymax, ymin = self.get_position()
        if not g.is_between(y_target, ymin, ymax):
            if y_target < ymin:
                self.down()
            else:
                self.up()

    def up(self):
        if self.get_position()[1] < g.UPPER_LIMIT:
            for part in self.paddle:
                part.setheading(g.UP)
                part.forward(PADDLE_STEP)

    def down(self):
        if self.get_position()[2] > g.LOWER_LIMIT:
            for part in self.paddle:
                part.setheading(g.DOWN)
                part.forward(PADDLE_STEP)
