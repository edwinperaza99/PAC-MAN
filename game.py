import sys, time
import pygame as pg

from settings import Settings
from vector import Vector
from game_stats import GameStats
from scoreboard import Scoreboard
from graph import NodeGroup

# from board import Board
from sound import Sound
from pacman import Pacman
from pellets import PelletGroup
from ghosts import Ghosts

# TODO: implement classes that are commented out

# from button import Button
from launch_screen import LaunchScreen
from constants import *


class Game:
    key_velocity = {
        pg.K_RIGHT: Vector(1, 0),
        pg.K_LEFT: Vector(-1, 0),
        pg.K_UP: Vector(0, -1),
        pg.K_DOWN: Vector(0, 1),
    }

    def __init__(self):
        pg.init()
        self.settings = Settings()
        self.screen = pg.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height)
        )
        pg.display.set_caption("PAC-MAN")
        self.nodes = NodeGroup(game=self, level="maze_1.txt")
        self.nodes.setPortalPair((0, 17), (27, 17))
        home_key = self.nodes.createHomeNodes(11.5, 14)
        self.nodes.connectHomeNodes(home_key, (12, 14), LEFT)
        self.nodes.connectHomeNodes(home_key, (15, 14), RIGHT)
        self.sound = Sound(game=self)
        self.stats = GameStats(game=self)
        # self.board = Board(game=self)
        self.sb = Scoreboard(game=self)
        self.launch_screen = LaunchScreen(game=self)
        self.game_active = False  # MUST be before Button is created
        self.first = True
        # TODO: pacman is added here
        self.pacman = Pacman(game=self, node=self.nodes.getNodeFromTiles(15, 26))
        nodes = list(self.nodes.nodesLUT.values())
        self.ghosts = Ghosts(game=self, node=nodes[10], pacman=self.pacman)
        self.ghosts.blinky.set_start_node(self.nodes.getNodeFromTiles(2 + 11.5, 0 + 14))
        self.ghosts.pinky.set_start_node(self.nodes.getNodeFromTiles(2 + 11.5, 3 + 14))
        self.ghosts.inky.set_start_node(self.nodes.getNodeFromTiles(0 + 11.5, 3 + 14))
        self.ghosts.clyde.set_start_node(self.nodes.getNodeFromTiles(4 + 11.5, 3 + 14))
        self.ghosts.set_spawn_node(self.nodes.getNodeFromTiles(2 + 11.5, 3 + 14))

        # self.ghost = Ghost(game=self, node=self.nodes.getStartTempNode())
        self.pellets = PelletGroup(game=self, pelletfile="maze_1.txt")
        # self.play_button = Button(game=self, text="Play")
        self.clock = pg.time.Clock()
        self.goal = Vector()

    def check_events(self):
        for event in pg.event.get():
            type = event.type
            if type == pg.KEYUP:
                key = event.key
                # if key == pg.K_SPACE:
                #     self.ship.cease_fire()
                # if key in Game.key_velocity:
                #     self.pacman.all_stop()
            elif type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif type == pg.KEYDOWN:
                key = event.key
                if key == pg.K_p:
                    pass
                    # self.play_button.select(True)
                    # self.play_button.press()
                # elif key in Game.key_velocity:
                #     self.pacman.add_speed(Game.key_velocity[key])
                #     pass
                # self.ship.add_speed(Game.key_velocity[key])
            elif type == pg.MOUSEBUTTONDOWN:
                pass
                # b = self.play_button
                # x, y = pg.mouse.get_pos()
                # if b.rect.collidepoint(x, y):
                # b.press()
            elif type == pg.MOUSEMOTION:
                pass
                # b = self.play_button
                # x, y = pg.mouse.get_pos()
                # b.select(b.rect.collidepoint(x, y))

    def restart(self):
        self.screen.fill(self.settings.bg_color)
        # self.ship.reset()
        # self.aliens.reset()
        # self.settings.initialize_dynamic_settings()

    def game_over(self):
        print("Game Over !")
        pg.mouse.set_visible(True)
        self.sound.play_game_over()
        self.first = True
        self.game_active = False
        self.stats.reset()
        self.sound.reset()
        self.restart()
        # self.launch_screen.run()  # kinda works but there is a bug

    def activate(self):
        self.game_active = True
        self.first = False
        # TODO: add music later
        self.sound.stop_music()
        # self.sound.play_start_up()
        # TODO: ADD MUSIC
        # self.sound.play_music(self.sound.select_song())

    def next_level(self):
        # TODO: probably add a pause for a smoother transition between levels
        # maybe even play a sound
        self.restart()
        self.stats.level += 1
        self.sb.prep_level()
        self.sb.prep_score()
        self.pellets = PelletGroup(game=self, pelletfile="maze_1.txt")
        self.pacman.reset()
        self.ghosts.reset()
        self.ghosts.blinky.set_start_node(self.nodes.getNodeFromTiles(2 + 11.5, 0 + 14))
        self.ghosts.pinky.set_start_node(self.nodes.getNodeFromTiles(2 + 11.5, 3 + 14))
        self.ghosts.inky.set_start_node(self.nodes.getNodeFromTiles(0 + 11.5, 3 + 14))
        self.ghosts.clyde.set_start_node(self.nodes.getNodeFromTiles(4 + 11.5, 3 + 14))
        self.ghosts.set_spawn_node(self.nodes.getNodeFromTiles(2 + 11.5, 3 + 14))

    # def show_high_scores_screen(self):
    #     high_score_screen = HighScoreScreen(self)
    #     high_score_screen.run()

    def play(self):
        self.launch_screen.run()
        finished = False
        self.screen.fill(self.settings.bg_color)

        while not finished:
            self.check_events()  # exits if Cmd-Q on macOS or Ctrl-Q on other OS

            if self.game_active or self.first:
                self.first = False
                self.screen.fill(self.settings.bg_color)
                self.sb.update()
                self.nodes.update()
                # self.board.update()
                dt = self.clock.tick(30) / 1000.0
                self.pacman.update(dt=dt)
                self.pellets.update(dt=dt, pacman=self.pacman)
                self.ghosts.update(dt=dt)
            else:
                pass
                # self.play_button.update()

            pg.display.flip()
            time.sleep(0.02)


if __name__ == "__main__":
    g = Game()
    g.play()
