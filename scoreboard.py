import pygame as pg
import pygame.font
from pygame.sprite import Group

# from ship import Ship TODO: import pacman


class Scoreboard:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.screen_rect = game.screen.get_rect()
        self.settings = game.settings
        self.stats = game.stats
        self.text_color = (255, 255, 255)  # white color
        # self.text_color = (30, 30, 30) # dark color
        # might change font to 'couriernew' or 'courier'
        self.font = pg.font.SysFont(None, 24)
        self.prep()
        self.prep_high_score()

    def prep(self):
        self.prep_score()
        self.prep_level()
        # self.prep_lives()

    def prep_score(self):
        rounded_score = round(self.stats.score, -1)
        s = f"CURRENT"

        self.score_image = self.font.render(
            s, True, self.text_color, self.settings.bg_color
        )
        self.score_rect = self.score_image.get_rect()
        self.score_rect.left = self.screen_rect.left + 15
        self.score_rect.top += 10

        score = f"{rounded_score:,}"
        self.score_value_image = self.font.render(
            score, True, self.text_color, self.settings.bg_color
        )
        self.score_value_rect = self.score_value_image.get_rect()
        self.score_value_rect.left = self.score_rect.left
        self.score_value_rect.top = self.score_rect.bottom + 5

    def prep_high_score(self):
        high_score = round(self.stats.high_score, -1)
        high_score_str = f"HIGH SCORE"

        self.high_score_image = self.font.render(
            high_score_str, True, self.text_color, self.settings.bg_color
        )

        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

        high_score_value = f"{high_score:,}"

        self.high_score_value_image = self.font.render(
            high_score_value, True, self.text_color, self.settings.bg_color
        )

        self.high_score_value_rect = self.high_score_value_image.get_rect()
        self.high_score_value_rect.centerx = self.screen_rect.centerx
        self.high_score_value_rect.top = self.high_score_rect.bottom + 5

    def prep_level(self):
        level_str = f"LEVEL: {self.stats.level}"
        self.level_image = self.font.render(
            level_str, True, self.text_color, self.settings.bg_color
        )

        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.screen_rect.right - 15
        self.level_rect.bottom = self.screen_rect.bottom - 10

    def prep_lives(self):
        self.lives = Group()
        for live_number in range(self.stats.lives_left):
            # TODO: change ship to PAC-MAN
            # TODO: draw ships at the bottom of the screen on left hand side. same height as level
            ship = Ship(self.game)
            ship.rect.x = 10 + live_number * ship.rect.width
            ship.rect.y = 10
            # TODO: test if the next line works when pacman class is done
            # ship.rect.y = self.level_rect.top
            self.lives.add(ship)

    def check_high_score(self):
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.stats.save_high_score()
            self.prep_high_score()

    def update(self):
        self.draw()

    def draw(self):
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.score_value_image, self.score_value_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.high_score_value_image, self.high_score_value_rect)
        self.screen.blit(self.level_image, self.level_rect)
        # self.ships.draw(self.screen) TODO: change ships


if __name__ == "__main__":
    print("\nERROR: scoreboard.py is the wrong file! Run play from game.py\n")
