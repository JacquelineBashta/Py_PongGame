import time
import globals as g
from ball import Ball
from write_panel import WritePanel
from play_ground import PlayGround
from paddle import Paddle


class Game:
    def __init__(self) -> None:
        self.play_ground = PlayGround()
        self.ball = Ball()
        self.ball_panel = WritePanel(g.CENTER)

        self.comp_score = 0
        self.comp_panel = WritePanel(g.LEFT)
        self.comp_panel.write_msg(self.comp_score)

        self.comp_paddle = Paddle(g.LEFT)

        self.usr_score = 0
        self.usr_panel = WritePanel(g.RIGHT)
        self.comp_panel.write_msg(self.usr_score)

        self.usr_paddle = Paddle(g.RIGHT)

        self.play_ground.refresh()

    def is_paddle_hit(self, a_paddle):
        xb, yb = self.ball.position()
        (x, ymax, ymin) = a_paddle.get_position()
        if abs(xb - x) < 30 and (abs(x) > abs(xb)) and \
                (yb <= ymax and yb >= ymin):
            self.ball.bounce(side=True)
            return True
        return False

    def is_ball_missed(self, which_side):
        if abs(which_side - self.ball.xcor()) < 10:
            self.ball_panel.write_msg("BALL MISSED")
            time.sleep(0.2)
            self.ball_panel.erase()
            time.sleep(0.1)
            self.ball.recenter()
            return True
        return False

    def comp_react(self):
        if self.ball.xcor() < -1*g.SCREEN_WIDTH/4 and \
                g.is_between(self.ball.heading(), 90, 270):
            self.comp_paddle.adapt_y(self.ball.ycor())
        else:
            # stand do nothing
            pass

    def usr_react(self):
        usr_request = self.play_ground.get_usr_input()
        if usr_request == g.UP:
            self.usr_paddle.up()
        elif usr_request == g.DOWN:
            self.usr_paddle.down()

    def ball_react(self):

        # Handle Upper/lower walls collision
        if (abs(g.UPPER_LIMIT) - abs(self.ball.ycor())) < 30:
            self.ball.bounce()
        # Handle Side walls / paddle collision
        if self.is_ball_missed(g.RIGHT_LIMIT) or \
                self.is_paddle_hit(self.comp_paddle):
            self.comp_score += 1
            self.comp_panel.write_msg(self.comp_score)
        elif self.is_ball_missed(g.LEFT_LIMIT) or  \
                self.is_paddle_hit(self.usr_paddle):
            self.usr_score += 1
            self.usr_panel.write_msg(self.usr_score)
        self.ball.move()

    def _make_step(self):
        self.ball_react()
        self.usr_react()
        self.comp_react()

        self.play_ground.refresh()
        self.play_ground.screen.ontimer(fun=self._make_step, t=50)

    def run(self):
        self.play_ground.listen()

        self._make_step()
        self.play_ground.screen.mainloop()
