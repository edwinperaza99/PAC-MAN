class Settings:
    def __init__(self):
        self.bg_color = (10, 10, 10)
        self.lives = 3

        # NEW: constants
        self.tile_width = 16
        self.tile_height = 16
        self.board_cols = 28
        self.board_rows = 36
        self.pacman_speed = 100 * self.tile_width / 16

        # was using 600 x 750
        self.screen_width = self.tile_width * self.board_cols
        self.screen_height = self.tile_height * self.board_rows


if __name__ == "__main__":
    print("\nERROR: settings.py is the wrong file! Run play from game.py\n")
