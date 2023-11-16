from turtle import Turtle
import globals as g

PANEL_POS_X = 50
PANEL_POS_Y = g.UPPER_LIMIT - 80
PANEL_FONT = ("Courier", 50, "bold")


class ScorePanel(Turtle):
    def __init__(self, pos):
        super().__init__()
        self.hideturtle()
        self.color(g.THEME_COLOR[1])
        self.penup()
        if pos == g.LEFT:
            self.goto(-PANEL_POS_X, PANEL_POS_Y)
        else:
            self.goto(PANEL_POS_X, PANEL_POS_Y)
        self.write_score(0)

    def write_score(self, score):
        self.clear()
        self.write(str(score), align="center", font=PANEL_FONT)
