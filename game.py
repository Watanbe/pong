import pygame as pg
import sys

from game_objects import Ball, Raquete

class Game:
    def __init__(self):
        self.WINDOW_WIDTH = 1080
        self.WINDOW_HEIGHT = 900

        self.screen = pg.display.set_mode([self.WINDOW_WIDTH, self.WINDOW_HEIGHT])
        self.new_game()

    def new_game(self):
        self.ball = Ball(self)
        self.left = Raquete(self, 'left')
        self.right = Raquete(self, 'right')

    def update(self):
        self.ball.update()
        self.left.update()
        self.right.update()
        pg.display.flip()

    def check_event(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

            self.left.control(event)
            self.right.control(event)

    def get_state(self):
        state_left = []
        state_right = []

        state_left.append(int(self.ball.center[1] < self.left.rect.top))
        state_left.append(int(self.ball.center[1] > self.left.rect.bottom))
        state_left.append(int(self.ball.direction[0] < 0))
        state_left.append(int(self.ball.direction[1] < 0))

        state_right.append(int(self.ball.center[1] < self.right.rect.top))
        state_right.append(int(self.ball.center[1] > self.right.rect.bottom))
        state_right.append(int(self.ball.direction[0] > 0))
        state_right.append(int(self.ball.direction[1] < 0))

        return tuple(state_left), tuple(state_right)
    
    def get_reward(self):
        reward_left = -1
        reward_right = -1

        if self.ball.center[0] == self.left.rect.right and self.ball.center[1] >= self.left.rect.top and self.ball.center[1] <= self.left.rect.bottom:
            reward_left = 1

        if self.ball.center[0] == self.right.rect.left and self.ball.center[1] >= self.right.rect.top and self.ball.center[1] <= self.right.rect.bottom:
            reward_right = 1

        if self.ball.center[0] <= 0:
            reward_left = -10
            
        if self.ball.center[0] >= self.WINDOW_WIDTH:
            reward_right = -10

        return reward_left, reward_right

    def draw(self):
        self.screen.fill('black')
        self.ball.draw()
        self.left.draw()
        self.right.draw()

    def create_event(self, key):
        new_event = pg.event.Event(key['key_type'], key=key['key'])
        pg.event.post(new_event)

    def step(self, event_left, event_right):
        self.create_event(event_left)
        self.create_event(event_right)
        self.check_event()
        self.update()
        self.draw()

        state = self.get_state()
        rewards = self.get_reward()

        return state[0], state[1], rewards[0], rewards[1], self.ball.done