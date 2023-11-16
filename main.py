
import turtle
import time
import random as r


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
USER_SIDE = SCREEN_WIDTH/2
COMP_SIDE = -SCREEN_WIDTH/2
THEME_COLOR = ["black", "white"]
PADDLE_SIZE = 3  # number of paddle parts, more is easier
# PADDLE_SHAPE_SIZE = 100
PADDLE_STEP = 20
BALL_STEP = 20
PADDLE_DELAY = 0.03  # inverse of speed less is faster
UP = 90
DOWN = 270
STILL = 0

LEFT = 180
RIGHT = 0


class Ball(turtle.Turtle):
    def __init__(self):
        super().__init__()
        self.shape("circle")
        self.color(THEME_COLOR[1])
        self.penup()
        self.setheading(r.randint(0, 15))

    def move(self):
        self.forward(BALL_STEP)

    def bounce(self, side=False):
        heading = self.heading()
        if side:
            radomness = r.randint(0, 20)
            heading = (360 - heading+radomness + 180) % 360
        else:
            if heading <= 180:
                heading = 360 - heading
            else:
                heading = 90-(360 - heading)
        self.setheading(heading)

    def recenter(self):
        self.goto(0, 0)
        self.setheading(r.randint(0, 15))


class ScorePanel(turtle.Turtle):
    def __init__(self, pos):
        super().__init__()
        self.hideturtle()
        self.color(THEME_COLOR[1])
        self.penup()
        if pos == LEFT:
            self.goto(-50, SCREEN_HEIGHT/2 - 80)
        else:
            self.goto(50, SCREEN_HEIGHT/2 - 80)
        self.write_score(0)

    def write_score(self, score):
        score = str(score)
        self.clear()
        self.write(score, align="center", font=("Courier", 50, "bold"))


class PlayGround:
    def __init__(self):
        self.screen = turtle.Screen()
        self.screen.bgcolor(THEME_COLOR[0])
        self.screen.setup(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.screen.title("Pong")
        self.screen.tracer(0)
        self._create_dash_line()
        self.usr_input = STILL

    def _create_dash_line(self):
        dash_line = turtle.Turtle()
        dash_line.pensize(5)
        dash_line.hideturtle()
        dash_line.goto(0, SCREEN_HEIGHT/2)
        dash_line.setheading(DOWN)

        for _ in range(round(SCREEN_HEIGHT/20)):
            dash_line.forward(10)
            dash_line.color(THEME_COLOR[1])
            dash_line.forward(10)
            dash_line.color(THEME_COLOR[0])

    def _create_score_panel(self, pos):
        score_panel = turtle.Turtle()
        score_panel.hideturtle()
        score_panel.color(THEME_COLOR[1])
        score_panel.penup()
        if pos == LEFT:
            score_panel.goto(-50, SCREEN_HEIGHT/2 - 80)
        else:
            score_panel.goto(50, SCREEN_HEIGHT/2 - 80)
        return score_panel

    def exit_on_click(self):
        self.screen.exitonclick()

    def refresh(self):
        self.screen.update()

    def usr_up(self):
        self.usr_input = UP

    def usr_down(self):
        self.usr_input = DOWN

    def usr_still(self):
        self.usr_input = STILL

    def listen(self):
        self.screen.onkeypress(fun=self.usr_up, key="Up")
        self.screen.onkeyrelease(fun=self.usr_still, key="Up")
        self.screen.onkeypress(fun=self.usr_down, key="Down")
        self.screen.onkeyrelease(fun=self.usr_still, key="Down")

        self.screen.listen()


class Paddle:
    def __init__(self, loc) -> None:
        self.paddle: list[turtle.Turtle] = []
        self._create_paddle_parts(PADDLE_SIZE, loc)

    def _create_paddle_parts(self, num_parts, location):

        part = turtle.Turtle("square")
        part.penup()
        if location == RIGHT:
            part.goto(SCREEN_WIDTH/2 - 50, 0)
        else:
            part.goto(-SCREEN_WIDTH/2 + 50, 0)
        part.color(THEME_COLOR[1])
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
        if not is_between(y_target, ymin, ymax):
            if y_target < ymin:
                self.down()
            else:
                self.up()

    def up(self):
        if self.get_position()[1] < SCREEN_HEIGHT/2:
            for part in self.paddle:
                part.setheading(UP)
                part.forward(PADDLE_STEP)

    def down(self):
        if self.get_position()[2] > -SCREEN_HEIGHT/2:
            for part in self.paddle:
                part.setheading(DOWN)
                part.forward(PADDLE_STEP)


class Game:
    def __init__(self) -> None:
        self.play_ground = PlayGround()
        self.ball = Ball()

        self.comp_panel = ScorePanel(LEFT)
        self.comp_paddle = Paddle(LEFT)
        self.comp_score = 0

        self.usr_panel = ScorePanel(RIGHT)
        self.usr_paddle = Paddle(RIGHT)
        self.usr_score = 0

        self.play_ground.refresh()

    def comp_think(self):
        if self.ball.xcor() < -1*SCREEN_WIDTH/4 and \
                is_between(self.ball.heading(), 90, 270):
            self.comp_paddle.sety(self.ball.ycor())
        else:
            # stand do nothing
            pass

    def handle_upper_wall(self):
        if (abs(SCREEN_HEIGHT/2) - abs(self.ball.ycor())) < 10:
            self.ball.bounce()

    def is_paddle_hit(self, a_paddle):
        xb, yb = self.ball.position()
        (x, ymax, ymin) = a_paddle.get_position()
        if abs(xb - x) < 10 and (yb <= (ymax+10) and yb >= (ymin-10)):
            self.ball.bounce(side=True)
            return True
        return False

    def is_ball_miss(self, which_side):
        if abs(which_side - self.ball.xcor()) < 10:
            self.ball.recenter()
            return True
        return False

    def _make_step(self):

        if self.play_ground.usr_input == UP:
            self.usr_paddle.up()
        elif self.play_ground.usr_input == DOWN:
            self.usr_paddle.down()

        self.comp_think()
        self.ball.move()

        self.handle_upper_wall()
        if self.is_ball_miss(USER_SIDE) or \
                self.is_paddle_hit(self.comp_paddle):
            self.comp_score += 1
            self.comp_panel.write_score(self.comp_score)
        elif self.is_ball_miss(COMP_SIDE) or  \
                self.is_paddle_hit(self.usr_paddle):
            self.usr_score += 1
            self.usr_panel.write_score(self.usr_score)

        self.play_ground.refresh()
        self.play_ground.screen.ontimer(fun=self._make_step, t=50)

    def run(self):
        self.play_ground.listen()

        self._make_step()
        self.play_ground.screen.mainloop()


def is_between(x, num1, num2):
    if x > num1 and x < num2:
        return True
    return False


game = Game()
game.run()
