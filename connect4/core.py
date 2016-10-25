from tkinter import Tk, Frame, Menu, Button, Label, Event
from board import ColumnFullError
from board_display import BoardDisplay
from player import HumanPlayer, ComputerPlayer
from game import Game
from random import uniform
import threading
from copy import deepcopy  # remove


class Application(Frame):
    # Screen settings
    screen_width = 1024
    screen_height = 768
    screen_y_padding = 20
    # Board settings
    board_width = 7
    board_height = 6
    win_seq_length = 4
    # Title settings
    title_str = "Connect {}".format(win_seq_length)
    title_font = "Helvetica, 30"
    title_height = 1
    # Label settings
    label_font = "Helvetica, 25"
    label_height = 1
    default_label_colour = "black"
    default_label_background = "white smoke"
    next_move_str = "{}'s Turn"
    column_full_str = "That column is already full!"
    game_won_str = "Congratulations {}!"
    game_drawn_str = "Unlucky: Game is a draw"
    # Button settings
    button_font = "Helvetica, 16"
    button_height = 1
    # CPU settings
    cpu_min_thinking_time = 200
    cpu_max_thinking_time = 2000

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.parent = master
        self.parent.minsize(width=self.screen_width, height=self.screen_height)
        self.parent.maxsize(width=self.screen_width, height=self.screen_height)
        # self.parent.overrideredirect(1)  # Disables top bar for full-screen

        self.create_menu()

        self.title = self.create_title()
        title_height = self.title.winfo_reqheight()

        button_height = self.create_buttons()

        self.status_label = self.create_status_label()
        label_height = self.status_label.winfo_reqheight()

        self.display = None  # Initialized in self.reset_board(), called in self.start_new_game()
        self.display_height = self.screen_height - title_height - button_height\
                              - label_height - (0 * self.screen_y_padding)
        self.block_size = self.display_height / self.board_height
        self.display_width = self.board_width * self.block_size

        self.screen_x_padding = (self.screen_width - self.display_width) / 2
        self.parent.config(padx=self.screen_x_padding)

        self.block_player_input = True
        self.game = self.start_new_game()

    def create_menu(self) -> None:
        menu_bar = Menu(self.parent)

        game_menu = Menu(self.parent, tearoff=0)
        game_menu.add_command(label="Player 1 vs Player 2", command=lambda: self.start_new_game(False, False))
        game_menu.add_command(label="Player 1 vs Computer", command=lambda: self.start_new_game(False, True))
        game_menu.add_command(label="Computer vs Player 2", command=lambda: self.start_new_game(True, False))
        game_menu.add_command(label="Computer vs Computer", command=lambda: self.start_new_game(True, True))
        game_menu.add_separator()
        game_menu.add_command(label="Exit", command=lambda: self.parent.destroy())
        menu_bar.add_cascade(label="Game", menu=game_menu)

        # options_menu = Menu(self.parent, tearoff=0)
        # options_menu.add_command(label="options", command=lambda: print("option"))
        # menu_bar.add_cascade(label="Settings", menu=options_menu)

        # help_menu = Menu(self.parent, tearoff=0)
        # help_menu.add_command(label="Controls", command=lambda: print("Display Controls"))
        # menu_bar.add_cascade(label="Help", menu=help_menu)

        self.parent.config(menu=menu_bar)

    def create_title(self) -> Label:
        title = Label(self.parent, text=self.title_str, font=self.title_font, height=self.title_height,
                      pady=self.screen_y_padding)
        title.grid(row=0, column=0, columnspan=self.board_width)
        return title

    def create_status_label(self) -> Label:
        label = Label(self.parent, font=self.label_font, height=self.label_height, text="", pady=self.screen_y_padding)
        label.grid(row=3, column=0, columnspan=self.board_width)
        return label

    def create_buttons(self) -> int:
        for column in range(self.board_width):
            button = Button(self.parent, text=str(column + 1), font=self.button_font,
                            width=2, height=self.button_height, bg="white", relief="groove",
                            pady=self.screen_y_padding, command=lambda column=column: self.button_pressed(column))
            # Hack to get current column value instantly
            button.grid(row=2, column=column, sticky="ew")
        height = button.winfo_reqheight()
        return height

    def button_pressed(self, column: int) -> None:
        if not self.block_player_input:
            self.insert_disc(column)

    def display_clicked(self, e: Event) -> None:
        if not self.block_player_input:
            column_width = self.display.width_in_pixels / self.board_width
            column_clicked = self.get_column_clicked(e.x, column_width)
            self.insert_disc(column_clicked)

    @staticmethod
    def get_column_clicked(x_clicked: int, column_width: float) -> int:
        column_clicked = 0
        x_clicked -= column_width
        while x_clicked > 0:
            x_clicked -= column_width
            column_clicked += 1
        return column_clicked

    def insert_disc(self, column: int) -> None:
        try:
            self.game.add(column)
            colour = self.game.current_player.get_colour
            target_row = self.game.get_target_row(column)
            self.display.drop_circle_to(column, colour, target_row)
            if self.game.has_won():
                self.block_player_input = True
                info = self.game.get_win_information()
                self.game_won(info)
            else:
                if self.game.all_columns_full():
                    self.block_player_input = True
                    self.game_drawn()
                else:
                    self.game.switch_player()
                    self.set_next_move_label()
            self.player_manager()
        except ColumnFullError:
            self.set_status_label(self.column_full_str)

    def game_won(self, info) -> None:
        player = info[0]
        player_name = player.get_name
        combination = info[1]
        self.set_status_label(self.game_won_str.format(player_name))
        self.display.flash_circles(combination)

    def game_drawn(self) -> None:
        self.set_status_label(self.game_drawn_str)

    def set_status_label(self, text, text_colour=default_label_colour, bg_colour=default_label_background) -> None:
        self.status_label.config(text=text, fg=text_colour, bg=bg_colour)

    def set_next_move_label(self) -> None:
        current_player = self.game.get_current_player
        player_name = current_player.get_name
        text = self.next_move_str.format(player_name)
        colour = current_player.get_colour
        self.set_status_label(text=text, text_colour=colour)

    def start_new_game(self, p1_is_cpu=False, p2_is_cpu=False) -> Game:
        self.reset_display()
        self.game = Game(self.board_width, self.board_height, self.win_seq_length, p1_is_cpu, p2_is_cpu)
        self.player_manager()
        return self.game

    def player_manager(self) -> None:
        current_player = self.game.get_current_player
        if self.game.in_progress:
            if isinstance(current_player, ComputerPlayer):  # Computer Player
                self.block_player_input = True

                if not self.display.animation_in_progress:  # wait until animation complete
                    column = current_player.get_move(self.game.board)
                    thinking_delay = int(uniform(self.cpu_min_thinking_time, self.cpu_max_thinking_time))
                    thinking_delay = 0 #################################################################################
                    self.parent.after(thinking_delay, lambda: self.insert_disc(column))
                else:
                    self.parent.after(200, self.player_manager)

            elif isinstance(current_player, HumanPlayer):  # Human Player
                self.block_player_input = False
                self.set_next_move_label()
            else:
                raise Exception("Player must be instance of HumanPlayer or ComputerPlayer. Not " +
                                str(type(current_player)))
        else:
            self.block_player_input = True

    def reset_display(self) -> None:
        if self.display:
            self.display.destroy()
        self.display = BoardDisplay(self.parent, self.display_width, self.display_height, self.block_size,
                                    self.board_width, self.board_height, grid_row=1, grid_column=0)
        self.display.bind("<Button-1>", self.display_clicked)

    def change_resolution(self, new_width: int, new_height: int) -> None:
        scale = new_width / self.screen_width
        if new_height / self.screen_height != scale:
            raise ValueError("Unknown aspect ratio")
        else:
            self.display.scale_display(scale)


def main():
    root = Tk()
    app = Application(master=root)
    app.mainloop()

if __name__ == "__main__":
    main()
