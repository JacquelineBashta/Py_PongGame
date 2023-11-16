
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

RIGHT_LIMIT = SCREEN_WIDTH/2
LEFT_LIMIT = -SCREEN_WIDTH/2
UPPER_LIMIT = SCREEN_HEIGHT/2
LOWER_LIMIT = -SCREEN_HEIGHT/2

THEME_COLOR = ["black", "white"]


STILL = 0
UP = 90
DOWN = 270
LEFT = 180
RIGHT = 0


def is_between(x, num1, num2):
    if x > num1 and x < num2:
        return True
    return False
