import pygame as pg
import numpy as np

vec2 = pg.math.Vector2

class Ball:
    def __init__(self, game):
        self.game = game   
        self.radius = 5
        self.center = vec2(self.game.WINDOW_WIDTH//2, self.game.WINDOW_HEIGHT//2)
        self.direction = vec2(np.random.choice([-1, 1]), np.random.choice([-1, 1]))
        self.done = False


    def draw(self):
        self.circle = pg.draw.circle(
            surface=self.game.screen, 
            color=(255, 255, 255), 
            center=self.center,
            radius=self.radius
        )

    def check_borders(self):
        if (self.center[0] <= 0 or self.center[0] > self.game.WINDOW_WIDTH):
            self.done = True

    def check_direction(self):
        dire = self.direction

        if self.center[0] == self.game.left.rect.right and self.center[1] >= self.game.left.rect.top and self.center[1] <= self.game.left.rect.bottom:
            dire[0] = 1

        if self.center[0] == self.game.right.rect.left and self.center[1] >= self.game.right.rect.top and self.center[1] <= self.game.right.rect.bottom:
            dire[0] = -1
            
        if self.center[1] < 0:
            dire[1] = 1
            
        if self.center[1] > self.game.WINDOW_HEIGHT:
            dire[1] = -1

        self.direction = dire

    def move(self):
        self.center[0] += self.direction[0]
        self.center[1] += self.direction[1]

    def update(self):
        self.check_borders()
        self.check_direction()
        self.move()
        
    
class Raquete:
    def __init__(self, game, side):
        self.game = game
        self.height = 100
        self.direction = vec2(0, 0)
        self.side = side
        
        if side == "left":
            self.rect = pg.rect.Rect([20, (self.game.WINDOW_HEIGHT//2) - (self.height//2), 20, self.height])
        else:
            self.rect = pg.rect.Rect([self.game.WINDOW_WIDTH - 40, (self.game.WINDOW_HEIGHT//2) - (self.height//2), 20, self.height])

    def control(self, event):
        if (event.type == pg.KEYDOWN):
            if self.side == 'left':
                if event.key == pg.K_w:
                    self.direction = vec2(0, -3)
                elif event.key == pg.K_s:
                    self.direction = vec2(0, 3)
            else:
                if event.key == pg.K_UP:
                    self.direction = vec2(0, -3)
                elif event.key == pg.K_DOWN:
                    self.direction = vec2(0, 3)

        elif event.type == pg.KEYUP:
            self.direction = vec2(0, 0)

    def move(self):
        self.rect.move_ip(self.direction)

    def draw(self):
        pg.draw.rect(self.game.screen, 'white', self.rect)

    def update(self):
        if (self.rect.top <= 0 and self.direction == vec2(0, 3)) or (self.rect.bottom >= self.game.WINDOW_HEIGHT and self.direction == vec2(0, -3)) or (self.rect.top > 0 and self.rect.bottom < self.game.WINDOW_HEIGHT):
            self.move()
