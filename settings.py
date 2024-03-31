class Settings:
    def __init__(self):
        self.bg_color = (10, 10, 10)
        self.lives = 3

        # NEW: constants
        self.tile_width = 16
        self.tile_height = 16
        self.board_cols = 28
        self.board_rows = 36
        # was using 600 x 750
        self.screen_width = self.tile_width * self.board_cols
        self.screen_height = self.tile_height * self.board_rows

        # placeholder
        self.YELLOW = (255, 255, 0)
        self.STOP = 0
        self.UP = 1
        self.DOWN = -1
        self.LEFT = 2
        self.RIGHT = -2
        self.PACMAN = 0


if __name__ == "__main__":
    print("\nERROR: settings.py is the wrong file! Run play from game.py\n")
