from turtle import Turtle, Screen
import globals as g


class PlayGround:
    def __init__(self):
        self.screen = Screen()
        self.screen.tracer(0)
        self.screen.bgcolor(g.THEME_COLOR[0])
        self.screen.setup(g.SCREEN_WIDTH, g.SCREEN_HEIGHT)
        self.screen.title("Pong")
        self._create_dash_line()
        self.usr_input = g.STILL

    def _create_dash_line(self):
        dash_line = Turtle()
        dash_line.pensize(5)
        dash_line.hideturtle()
        dash_line.goto(0, g.UPPER_LIMIT)
        dash_line.setheading(g.DOWN)

        for _ in range(round(g.SCREEN_HEIGHT/20)):
            dash_line.forward(10)
            dash_line.color(g.THEME_COLOR[1])
            dash_line.forward(10)
            dash_line.color(g.THEME_COLOR[0])

    def exit_on_click(self):
        self.screen.exitonclick()

    def refresh(self):
        self.screen.update()

    def get_usr_input(self):
        return self.usr_input

    def usr_up(self):
        self.usr_input = g.UP

    def usr_down(self):
        self.usr_input = g.DOWN

    def usr_still(self):
        self.usr_input = g.STILL

    def listen(self):
        self.screen.onkeypress(fun=self.usr_up, key="Up")
        self.screen.onkeyrelease(fun=self.usr_still, key="Up")
        self.screen.onkeypress(fun=self.usr_down, key="Down")
        self.screen.onkeyrelease(fun=self.usr_still, key="Down")

        self.screen.listen()
