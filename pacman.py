from pygame.sprite import Sprite
from vector import Vector
from sound import Sound


class Pacman(Sprite):
    def __init__(self, game):
        super().__init__()
        self.screen = game.screen
        self.settings = game.settings
        self.sound = game.sound
        self.screen_rect = self.screen.get_rect()
