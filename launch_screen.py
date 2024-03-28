import sys, time
import pygame as pg

# from button import Button


class LaunchScreen:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.stats = game.stats
        self.sound = game.sound
        self.screen_rect = self.screen.get_rect()
        self.settings = game.settings
        self.text_color = (255, 255, 255)
        self.font = pg.font.SysFont(None, 48)
        self.logo = pg.image.load("images/pac-man-logo.png")

    def check_events(self):
        pass

    def display_logo(self):
        self.logo_rect = self.logo.get_rect()
        self.logo_rect.centerx = self.screen_rect.centerx
        self.logo_rect.top = self.screen_rect.top + 50
        self.screen.blit(self.logo, self.logo_rect)

    def display_high_score(self):
        high_score = round(self.stats.high_score, -1)
        high_score_str = f"HIGH SCORE"

        self.high_score_image = self.font.render(
            high_score_str, True, self.text_color, self.settings.bg_color
        )

        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.logo_rect.top + 20

        high_score_value = f"{high_score:,}"

        self.high_score_value_image = self.font.render(
            high_score_value, True, self.text_color, self.settings.bg_color
        )

        self.high_score_value_rect = self.high_score_value_image.get_rect()
        self.high_score_value_rect.centerx = self.screen_rect.centerx
        self.high_score_value_rect.top = self.high_score_rect.bottom + 5

        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.high_score_value_image, self.high_score_value_rect)

    def draw(self):
        self.screen.fill(self.settings.bg_color)
        self.display_logo()
        self.display_high_score()
        # self.draw_play_button()
        pg.display.flip()

    def run(self):
        # if not pg.mixer.music.get_busy():
        # self.sound.play_music("sounds/space_invaders.wav")
        while not self.game.game_active:
            self.draw()
            self.check_events()
