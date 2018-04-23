import pyglet
from pyglet.window import BaseWindow
import pyglet.window.key as key
import pyglet.window.mouse as mouse


class SnakeWindow(BaseWindow):
    def __init__(self, width, height, cell_size, frame_rate, title):
        super().__init__(width, height, title)
        self.cell_size = cell_size
        self.frame_rate = frame_rate
        self.snake = Snake(width, height, cell_size)
        self.running = False
        self.fps_display = pyglet.clock.ClockDisplay()
        pyglet.gl.glClearColor(255, 255, 255, 255)

        self.label_paused = pyglet.text.Label("PAUSED",
                                              font_size=50,
                                              color=(0, 0, 0, 255),
                                              x=self.cell_size, y=self.cell_size,
                                              anchor_x='left', anchor_y='bottom')

    def on_draw(self):
        self.clear()
        self.game_of_life.draw()
        self.game_of_life.draw_grid()

        if not self.running:
            self.label_paused.draw()

        self.fps_display.draw()

    def on_key_press(self, symbol, modifiers):
        if symbol == key.SPACE and self.running:
            pyglet.clock.unschedule(self.update)
            self.running = False
        elif symbol == key.SPACE and not self.running:
            pyglet.clock.schedule_interval(self.update, self.frame_rate)
            self.running = True
        elif symbol == key.RIGHT and not self.running:
            self.game_of_life.run_rules()
        elif symbol == key.C:
            self.game_of_life.clear()
        elif symbol == key.F:
            self.game_of_life.fill()
        elif symbol == key.R:
            self.game_of_life.randomize()

    def on_mouse_press(self, x, y, button, modifiers):
        if button == mouse.LEFT:
            row = int(y / self.cell_size)
            col = int(x / self.cell_size)

            self.game_of_life.fill_cell(row, col)

        if button == mouse.RIGHT:
            row = int(y / self.cell_size)
            col = int(x / self.cell_size)

            self.game_of_life.empty_cell(row, col)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if buttons == mouse.LEFT:
            row = int(y / self.cell_size)
            col = int(x / self.cell_size)

            self.game_of_life.fill_cell(row, col)

        if buttons == mouse.RIGHT:
            row = int(y / self.cell_size)
            col = int(x / self.cell_size)

            self.game_of_life.empty_cell(row, col)

    def update(self, dt):
        self.game_of_life.run_rules()

class HelloWorldWindow(pyglet.window.Window):
    def __init__(self):
        super(HelloWorldWindow, self).__init__()

        self.label = pyglet.text.Label('Hello, world!')

    def on_draw(self):
        self.clear()
        self.label.draw()


if __name__ == '__main__':
    window = Window(1280, 720, 20, 1 / 12, "Game of Life")
    pyglet.app.run()
