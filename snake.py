import random

import pyglet

DIRECTIONS = {"LEFT": [-1, 0],
              "RIGHT": [1, 0],
              "UP": [0, 1],
              "DOWN": [0, -1]}


class Snake:
    def __init__(self, window_width, window_height, cell_size):
        self.grid_width = int(window_width / cell_size)
        self.grid_height = int(window_height / cell_size)
        self.cell_size = cell_size
        self.head = (int(self.grid_width / 2), int(self.grid_height / 2))
        self.snake = [(int(self.grid_width / 2), int(self.grid_height / 2) - 1),
                      (int(self.grid_width / 2), int(self.grid_height / 2) - 2),
                      (int(self.grid_width / 2), int(self.grid_height / 2) - 3)]
        self.direction = "UP"

        self.food = self.generate_coords()
        self.updated = True

        self.score = 0

        pyglet.gl.glClearColor(255, 255, 255, 255)

    @property
    def head_x(self):
        return self.head[0]

    @property
    def head_y(self):
        return self.head[1]

    @property
    def food_x(self):
        return self.food[0]

    @property
    def food_y(self):
        return self.food[1]

    def draw_grid(self):
        main_batch = pyglet.graphics.Batch()

        for row in range(self.grid_height):
            line_coords = [0, row * self.cell_size,
                           self.grid_width * self.cell_size, row * self.cell_size]

            main_batch.add(2, pyglet.gl.GL_LINES, None,
                           ('v2i', line_coords),
                           ('c3B', [0, 0, 0, 0, 0, 0]))

        for col in range(self.grid_width):
            line_coords = [col * self.cell_size, 0,
                           col * self.cell_size, self.grid_height * self.cell_size]

            main_batch.add(2, pyglet.gl.GL_LINES, None,
                           ('v2i', line_coords),
                           ('c3B', [0, 0, 0, 0, 0, 0]))

        for row in range(self.grid_height):
            for col in range(self.grid_width):
                if row == 0 or row == self.grid_height - 1 or col == 0 or col == self.grid_width - 1:
                    square_coords = [row * self.cell_size, col * self.cell_size,
                                     row * self.cell_size, col * self.cell_size + self.cell_size,
                                     row * self.cell_size + self.cell_size, col * self.cell_size,
                                     row * self.cell_size + self.cell_size, col * self.cell_size + self.cell_size]

                    main_batch.add_indexed(4, pyglet.gl.GL_TRIANGLES, None,
                                           [0, 1, 2, 1, 2, 3],
                                           ('v2i', square_coords),
                                           ('c3B', [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]))

        main_batch.draw()

    def draw(self):
        main_batch = pyglet.graphics.Batch()

        square_coords = [self.head_x * self.cell_size, self.head_y * self.cell_size,
                         self.head_x * self.cell_size, self.head_y * self.cell_size + self.cell_size,
                         self.head_x * self.cell_size + self.cell_size, self.head_y * self.cell_size,
                         self.head_x * self.cell_size + self.cell_size, self.head_y * self.cell_size + self.cell_size]

        main_batch.add_indexed(4, pyglet.gl.GL_TRIANGLES, None,
                               [0, 1, 2, 1, 2, 3],
                               ('v2i', square_coords),
                               ('c3B', [0, 255, 0, 0, 255, 0, 0, 255, 0, 0, 255, 0]))

        for (row, col) in self.snake:
            square_coords = [row * self.cell_size, col * self.cell_size,
                             row * self.cell_size, col * self.cell_size + self.cell_size,
                             row * self.cell_size + self.cell_size, col * self.cell_size,
                             row * self.cell_size + self.cell_size, col * self.cell_size + self.cell_size]

            main_batch.add_indexed(4, pyglet.gl.GL_TRIANGLES, None,
                                   [0, 1, 2, 1, 2, 3],
                                   ('v2i', square_coords),
                                   ('c3B', [0, 255, 0, 0, 255, 0, 0, 255, 0, 0, 255, 0]))

        square_coords = [self.food_x * self.cell_size, self.food_y * self.cell_size,
                         self.food_x * self.cell_size, self.food_y * self.cell_size + self.cell_size,
                         self.food_x * self.cell_size + self.cell_size, self.food_y * self.cell_size,
                         self.food_x * self.cell_size + self.cell_size, self.food_y * self.cell_size + self.cell_size]

        main_batch.add_indexed(4, pyglet.gl.GL_TRIANGLES, None,
                               [0, 1, 2, 1, 2, 3],
                               ('v2i', square_coords),
                               ('c3B', [0, 0, 255, 0, 0, 255, 0, 0, 255, 0, 0, 255]))

        main_batch.draw()

    def set_direction(self, direction):
        if self.updated:
            correct_move = False
            if self.direction == "LEFT" and direction is not "RIGHT":
                correct_move = True
            elif self.direction == "RIGHT" and direction is not "LEFT":
                correct_move = True
            elif self.direction == "UP" and direction is not "DOWN":
                correct_move = True
            elif self.direction == "DOWN" and direction is not "UP":
                correct_move = True

            if correct_move:
                self.direction = direction
                self.updated = False

    def run_rules(self):
        new_head = tuple([sum(x) for x in zip(self.head, DIRECTIONS[self.direction])])

        # Check for collisions
        if new_head[0] <= 0 or new_head[0] >= self.grid_width - 1 or new_head[1] <= 0 or new_head[1] >= self.grid_height - 1:
            return True

        if new_head in self.snake[:-1]:
            return True

        # Check for food
        if new_head == self.food:
            self.snake = [self.head] + self.snake
            self.food = self.generate_coords()
            self.score += 1
        else:
            old_snake = self.snake
            self.snake = [self.head]
            for i in range(1, len(old_snake)):
                self.snake.append(old_snake[i - 1])

        self.head = new_head
        self.updated = True

        return False

    def generate_coords(self):
        x = random.randint(2, self.grid_width - 2)
        y = random.randint(2, self.grid_height - 2)

        while (x, y) in self.head or (x, y) in self.snake:
            x = random.randint(2, self.grid_width - 2)
            y = random.randint(2, self.grid_height - 2)

        return x, y

    def reset(self):
        self.head = [int(self.grid_width / 2), int(self.grid_height / 2)]
        self.snake = [(int(self.grid_width / 2), int(self.grid_height / 2) - 1),
                      (int(self.grid_width / 2), int(self.grid_height / 2) - 2),
                      (int(self.grid_width / 2), int(self.grid_height / 2) - 3)]
        self.direction = "UP"
        self.food = self.generate_coords()
