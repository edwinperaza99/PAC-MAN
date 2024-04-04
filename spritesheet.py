import pygame as pg
from constants import *
import numpy as np

BASE_TILE_WIDTH = 16
BASE_TILE_HEIGHT = 16


class Spritesheet:
    def __init__(self, game):
        self.game = game
        self.settings = game.settings
        self.tile_width = self.settings.tile_width
        self.tile_height = self.settings.tile_height
        self.sheet = pg.image.load("images/spritesheet.png").convert()
        transparent_color = self.sheet.get_at((0, 0))
        self.sheet.set_colorkey(transparent_color)
        width = int(self.sheet.get_width() / BASE_TILE_WIDTH * self.tile_width)
        height = int(self.sheet.get_height() / BASE_TILE_HEIGHT * self.tile_height)
        self.sheet = pg.transform.scale(self.sheet, (width, height))

    def getImage(self, x, y, width, height):
        x *= self.tile_width
        y *= self.tile_height
        self.sheet.set_clip(pg.Rect(x, y, width, height))
        return self.sheet.subsurface(self.sheet.get_clip())


class PacmanSprites(Spritesheet):
    def __init__(self, game, pacman):
        super().__init__(game)
        self.pacman = pacman
        self.pacman.image = self.getStartImage()

    def getStartImage(self):
        return self.getImage(8, 0)

    def getImage(self, x, y):
        return Spritesheet.getImage(
            self, x, y, 2 * self.tile_width, 2 * self.tile_height
        )


class GhostSprites(Spritesheet):
    def __init__(self, game, ghost):
        super().__init__(game)
        self.x = {BLINKY: 0, PINKY: 2, INKY: 4, CLYDE: 6}
        self.ghost = ghost
        self.ghost.image = self.getStartImage()

    def getStartImage(self):
        return self.getImage(self.x[self.ghost.name], 4)

    def getImage(self, x, y):
        return Spritesheet.getImage(
            self, x, y, 2 * self.tile_width, 2 * self.tile_height
        )


class MazeSprites(Spritesheet):
    def __init__(self, game, mazefile, rotfile):
        super().__init__(game)
        self.data = self.readMazeFile(mazefile)
        self.rotdata = self.readMazeFile(rotfile)

    def getImage(self, x, y):
        return Spritesheet.getImage(self, x, y, self.tile_width, self.tile_height)

    def readMazeFile(self, mazefile):
        return np.loadtxt(mazefile, dtype="<U1")

    def constructBackground(self, background, y):
        for row in list(range(self.data.shape[0])):
            for col in list(range(self.data.shape[1])):
                if self.data[row][col].isdigit():
                    x = int(self.data[row][col]) + 12
                    sprite = self.getImage(x, y)
                    rotval = int(self.rotdata[row][col])
                    sprite = self.rotate(sprite, rotval)
                    background.blit(
                        sprite, (col * self.tile_width, row * self.tile_height)
                    )
                elif self.data[row][col] == "=":
                    sprite = self.getImage(10, 8)
                    background.blit(
                        sprite, (col * self.tile_width, row * self.tile_height)
                    )
        return background

    def rotate(self, sprite, value):
        return pg.transform.rotate(sprite, value * 90)
