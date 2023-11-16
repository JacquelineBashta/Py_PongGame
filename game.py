
import globals as g
from ball import Ball
from score_panel import ScorePanel
from play_ground import PlayGround
from paddle import Paddle


class Game:
    def __init__(self) -> None:
        self.play_ground = PlayGround()
        self.ball = Ball()

        self.comp_panel = ScorePanel(g.LEFT)
        self.comp_paddle = Paddle(g.LEFT)
        self.comp_score = 0

        self.usr_panel = ScorePanel(g.RIGHT)
        self.usr_paddle = Paddle(g.RIGHT)
        self.usr_score = 0

        self.play_ground.refresh()

    def is_paddle_hit(self, a_paddle):
        xb, yb = self.ball.position()
        (x, ymax, ymin) = a_paddle.get_position()
        if abs(xb - x) < 10 and (yb <= (ymax+10) and yb >= (ymin-10)):
            self.ball.bounce(side=True)
            return True
        return False

    def is_ball_missed(self, which_side):
        if abs(which_side - self.ball.xcor()) < 10:
            self.ball.recenter()
            return True
        return False

    def comp_react(self):
        if self.ball.xcor() < -1*g.SCREEN_WIDTH/4 and \
                g.is_between(self.ball.heading(), 90, 270):
            self.comp_paddle.sety(self.ball.ycor())
        else:
            # stand do nothing
            pass

    def usr_react(self):
        if self.play_ground.usr_input == g.UP:
            self.usr_paddle.up()
        elif self.play_ground.usr_input == g.DOWN:
            self.usr_paddle.down()

    def ball_react(self):
        self.ball.move()
        # Handle Upper/lower walls collision
        if (abs(g.SCREEN_HEIGHT/2) - abs(self.ball.ycor())) < 10:
            self.ball.bounce()
        # Handle Side walls / paddle collision
        if self.is_ball_missed(g.RIGHT_LIMIT) or \
                self.is_paddle_hit(self.comp_paddle):
            self.comp_score += 1
            self.comp_panel.write_score(self.comp_score)
        elif self.is_ball_missed(g.LEFT_LIMIT) or  \
                self.is_paddle_hit(self.usr_paddle):
            self.usr_score += 1
            self.usr_panel.write_score(self.usr_score)

    def _make_step(self):
        self.usr_react()
        self.comp_react()
        self.ball_react()

        self.play_ground.refresh()
        self.play_ground.screen.ontimer(fun=self._make_step, t=50)

    def run(self):
        self.play_ground.listen()

        self._make_step()
        self.play_ground.screen.mainloop()
