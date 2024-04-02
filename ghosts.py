import pygame
from pygame.locals import *
from pygame.sprite import Sprite
from vector import Vector
from constants import *
from random import randint


class Ghost(Sprite):
    def __init__(self, game, node, pacman):
        self.name = None
        self.directions = {
            UP: Vector(0, -1),
            DOWN: Vector(0, 1),
            LEFT: Vector(-1, 0),
            RIGHT: Vector(1, 0),
            STOP: Vector(),
        }
        self.game = game
        self.settings = game.settings
        self.screen = game.screen
        self.direction = STOP
        self.set_speed(100)
        self.radius = 10
        self.collideRadius = 5
        self.color = WHITE
        self.node = node
        self.set_position()
        self.target = node
        self.visible = True
        self.disablePortal = False
        self.goal = Vector()
        # change this variable to goal_direction to make the ghost chase pacman
        # self.direction_method = self.random_direction
        self.direction_method = self.goal_direction
        self.pacman = pacman
        self.mode = ModeController(self)

    def set_position(self):
        self.position = self.node.position.copy()

    def reset(self):
        self.set_position()
        self.is_dying = False
        # set timer to regular pacman sprite here

    def validate_direction(self, direction):
        if direction is not STOP:
            if self.node.neighbors[direction] is not None:
                return True
        return False

    def get_new_target(self, direction):
        if self.validate_direction(direction):
            return self.node.neighbors[direction]
        return self.node

    def overshot_target(self):
        if self.target is not None:
            vec1 = self.target.position - self.node.position
            vec2 = self.position - self.node.position
            node2Target = vec1.magnitudeSquared()
            node2Self = vec2.magnitudeSquared()
            return node2Self >= node2Target
        return False

    def reverse_direction(self):
        self.direction *= -1
        temp = self.node
        self.node = self.target
        self.target = temp

    def opposite_direction(self, direction):
        if direction is not STOP:
            if direction == self.direction * -1:
                return True
        return False

    def set_speed(self, speed):
        self.speed = speed * self.settings.tile_width / 16

    def valid_directions(self):
        directions = []
        for key in [UP, DOWN, LEFT, RIGHT]:
            if self.validate_direction(key):
                if key != self.direction * -1:
                    directions.append(key)
        if len(directions) == 0:
            directions.append(self.direction * -1)
        return directions

    def random_direction(self, directions):
        return directions[randint(0, len(directions) - 1)]

    def goal_direction(self, directions):
        distances = []
        for direction in directions:
            vec = (
                self.node.position
                + self.directions[direction] * self.settings.tile_width
                - self.goal
            )
            distances.append(vec.magnitudeSquared())
        index = distances.index(min(distances))
        return directions[index]

    def update(self, dt):
        self.position += self.directions[self.direction] * self.speed * dt

        if self.overshot_target():
            self.node = self.target
            directions = self.valid_directions()
            direction = self.direction_method(directions)
            if not self.disablePortal:
                if self.node.neighbors[PORTAL] is not None:
                    self.node = self.node.neighbors[PORTAL]
            self.target = self.get_new_target(direction)
            if self.target is not self.node:
                self.direction = direction
            else:
                self.target = self.get_new_target(self.direction)

            self.set_position()
        self.draw(self.screen)

    def choose_mode(self, dt):
        self.mode.update(dt)
        if self.mode.current is SCATTER:
            self.scatter()
        elif self.mode.current is CHASE:
            self.chase()
        self.update(dt)

    def scatter(self):
        self.goal = Vector()

    def chase(self):
        self.goal = self.pacman.position

    def draw(self, screen):
        if self.visible:
            p = self.position.asInt()
            pygame.draw.circle(screen, self.color, p, self.radius)


class MainMode:
    def __init__(self):
        self.timer = 0
        self.scatter()

    def update(self, dt):
        self.timer += dt
        if self.timer >= self.time:
            if self.mode is SCATTER:
                self.chase()
            elif self.mode is CHASE:
                self.scatter()

    def scatter(self):
        self.mode = SCATTER
        self.time = 7
        self.timer = 0

    def chase(self):
        self.mode = CHASE
        self.time = 20
        self.timer = 0


class ModeController:
    def __init__(self, ghost):
        self.timer = 0
        self.time = None
        self.mainmode = MainMode()
        self.current = self.mainmode.mode
        self.ghost = ghost

    def update(self, dt):
        self.mainmode.update(dt)
        self.current = self.mainmode.mode
