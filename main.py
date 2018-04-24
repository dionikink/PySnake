import pyglet
import pyglet.window.key as key
from pyglet.window import Window

from snake import Snake

LEFT = key.LEFT
RIGHT = key.RIGHT
UP = key.UP
DOWN = key.DOWN
SPACE = key.SPACE
RESET = key.R
FRAME = key.ENTER

WIDTH = 720
HEIGHT = 720
CELL_SIZE = 20
FRAME_RATE = 1 / 12

window = Window(WIDTH, HEIGHT)
snake = Snake(WIDTH, HEIGHT, CELL_SIZE)
running = False
game_over = False
fps_display = pyglet.clock.ClockDisplay()
pyglet.gl.glClearColor(255, 255, 255, 255)
label_paused = pyglet.text.Label("PAUSED",
                                 font_size=50,
                                 color=(0, 0, 0, 255),
                                 x=CELL_SIZE, y=CELL_SIZE,
                                 anchor_x='left', anchor_y='bottom')
label_game_over = pyglet.text.Label("GAME OVER",
                                    font_size=50,
                                    color=(255, 0, 0, 255),
                                    x=WIDTH / 2, y=HEIGHT / 2,
                                    anchor_x='center', anchor_y='center')
label_restart = pyglet.text.Label("Press R to restart",
                                  font_size=30,
                                  color=(0, 0, 0, 255),
                                  x=WIDTH / 2, y=(HEIGHT / 2) - 50,
                                  anchor_x='center', anchor_y='center')
label_score = pyglet.text.Label(text="Score: 0", x=20, y=5, color=(255, 255, 255, 255))


@window.event
def on_draw():
    window.clear()
    snake.draw()
    snake.draw_grid()
    label_score.text = "Score: {}".format(snake.score)
    label_score.draw()

    if not running:
        label_paused.draw()

    if game_over:
        label_game_over.draw()
        label_restart.draw()
        pyglet.clock.unschedule(update)

    fps_display.draw()


@window.event
def on_key_press(symbol, modifiers):
    global game_over
    global running
    global FRAME_RATE

    if symbol == SPACE and running and not game_over:
        pyglet.clock.unschedule(update)
        running = False
    elif symbol == SPACE and not running and not game_over:
        pyglet.clock.schedule_interval(update, FRAME_RATE)
        running = True
    elif symbol == LEFT:
        snake.set_direction("LEFT")
    elif symbol == RIGHT:
        snake.set_direction("RIGHT")
    elif symbol == UP:
        snake.set_direction("UP")
    elif symbol == DOWN:
        snake.set_direction("DOWN")
    elif symbol == RESET:
        snake.reset()
        running = False
        game_over = False
        pyglet.clock.unschedule(update)
    elif symbol == FRAME:
        snake.run_rules()


def update(dt):
    global game_over
    game_over = snake.run_rules()


if __name__ == '__main__':
    pyglet.app.run()
