from turtle import Turtle
import globals as g

PANEL_POS_X = 80
PANEL_POS_Y = g.UPPER_LIMIT - 80
PANEL_FONT = ("Courier", 50, "bold")


class WritePanel(Turtle):
    def __init__(self, pos):
        super().__init__()
        self.hideturtle()
        self.color(g.THEME_COLOR[1])
        self.penup()
        if pos == g.CENTER:
            pass
        elif pos == g.LEFT:
            self.goto(-PANEL_POS_X, PANEL_POS_Y)
        else:
            self.goto(PANEL_POS_X, PANEL_POS_Y)

    def erase(self):
        self.clear()

    def write_msg(self, msg, font=PANEL_FONT):
        self.clear()
        self.write(str(msg), align="center", font=font)
