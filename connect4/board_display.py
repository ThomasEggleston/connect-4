from tkinter import Tk, Canvas
import threading


class BoardDisplay(Canvas):
    board_colour = "yellow2"
    background_colour = "white"
    drop_delay = 30
    win_animation_iterations = 20
    win_animation_colour = "white"
    win_animation_delay = 50

    def __init__(self, parent: Tk, width_in_pixels: int, height_in_pixels: int, block_size: int,
                 board_width: int, board_height: int, grid_row: int, grid_column: int):
        self.parent = parent

        self.width_in_pixels = width_in_pixels
        self.height_in_pixels = height_in_pixels

        Canvas.__init__(self, parent, width=self.width_in_pixels, height=self.height_in_pixels, bg=self.board_colour)

        self.num_circles_horizontal = board_width
        self.num_circles_vertical = board_height

        self.circle_diameter = (8 / 10) * block_size
        self.padding = (1 / 10) * block_size
        self.drop_distance = block_size

        self.grid(row=grid_row, column=grid_column, columnspan=self.num_circles_horizontal)
        self.draw_bg_circles()

        self.animation_in_progress = False  # Used to tell parent that it should wait until animation over

    def scale_display(self, scale: int) -> None:
        self.width_in_pixels *= scale
        self.height_in_pixels *= scale
        self.circle_diameter *= scale
        self.padding *= scale
        self.drop_distance *= scale
        self.config(width=self.width_in_pixels, height=self.height_in_pixels)
        self.scale("all", 0, 0, scale, scale)

    def draw_circle(self, col: int, row: int, colour: str) -> int:
        coord = self.get_circle_coord(col, row)
        x = coord[0]
        y = coord[1]
        circle = self.create_oval(x, y, x + self.circle_diameter, y + self.circle_diameter, fill=colour, width=0)
        return circle

    def draw_bg_circles(self) -> None:
        colour = self.background_colour
        for col in range(self.num_circles_horizontal):
            for row in range(self.num_circles_vertical):
                self.draw_circle(col, row, colour)

    def get_circle_coord(self, col: int, row: int) -> tuple:
        padding = self.padding
        circle_diameter = self.circle_diameter
        x = padding + ((circle_diameter + 2 * padding) * col)
        y = padding + ((circle_diameter + 2 * padding) * row)
        coord = (x, y)
        return coord

    def drop_circle_to(self, column: int, colour: int, target_row: int) -> None:
        self.animation_in_progress = True

        start_row = 0
        circle = self.draw_circle(column, start_row, colour)
        drop_delay = self.drop_delay
        drop_distance = self.drop_distance
        '''threading.Timer(drop_delay, self.drop_circle,
                        args=[circle, start_row, target_row, drop_distance, drop_delay]).start()'''
        self.parent.after(drop_delay,
                          lambda: self.drop_circle(circle, start_row, target_row, drop_distance, drop_delay))

    def drop_circle(self, circle: int, current_row: int, target_row: int,
                    drop_distance: int, drop_delay: float) -> None:
        if current_row == 0:
            self.animation_in_progress = False

        if current_row < target_row:
            self.move(circle, 0, drop_distance)
            current_row += 1
            '''threading.Timer(drop_delay, self.drop_circle,
                            args=[circle, current_row, target_row, drop_distance, drop_delay]).start()'''
            self.parent.after(drop_delay,
                              lambda: self.drop_circle(circle, current_row, target_row, drop_distance, drop_delay))

    def flash_circles(self, combination: list):
        iterations = self.win_animation_iterations
        self.parent.after(self.win_animation_delay, lambda: self.flash_on(iterations, combination))

    def flash_on(self, iterations: int, combination: list):
        if iterations > 0:
            colour = self.win_animation_colour
            circles = []
            for pos in combination:
                column = pos[0]
                row = pos[1]
                circle = self.draw_circle(column, row, colour)
                circles.append(circle)
            self.parent.after(self.win_animation_delay, lambda: self.flash_off(iterations, combination, circles))

    def flash_off(self, iterations: int, combination: list, circles: int) -> None:
        for circle in circles:
            self.delete(circle)
        iterations -= 1
        self.parent.after(self.win_animation_delay, lambda: self.flash_on(iterations, combination))
