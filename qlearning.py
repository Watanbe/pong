import numpy as np
import pygame as pg

import random

class QLearning:
    def __init__(self, game):
        self.env = game
        self.q_values_left = np.zeros((2, 2, 2, 2, 3))
        self.q_values_right = np.zeros((2, 2, 2, 2, 3))

        self.epsilon = 1
        self.epsilon_discount = 0.992
        self.min_epsilon = 0.01

        self.discount_factor = 0.73
        self.learning_rate = 0.04

        self.num_episodes = 10001
        self.actions_left = [
            {"key": pg.K_w, "key_type": pg.KEYDOWN},
            {"key": pg.K_s, "key_type": pg.KEYDOWN},
            {"key": pg.K_w, "key_type": pg.KEYUP}
        ]
        self.actions_right = [
            {"key": pg.K_UP, "key_type": pg.KEYDOWN},
            {"key": pg.K_DOWN, "key_type": pg.KEYDOWN},
            {"key": pg.K_DOWN, "key_type": pg.KEYUP}
        ]

    def get_action_left(self, state):
        if random.random() < self.epsilon:
            return random.choice([0, 1, 2])
        return np.argmax(self.q_values_left[state])
    
    def get_action_right(self, state):
        if random.random() < self.epsilon:
            return random.choice([0, 1, 2])
        return np.argmax(self.q_values_right[state])
    
    def update_epsilon(self):
        self.epsilon = max(self.epsilon * self.epsilon_discount, self.min_epsilon)

    def train(self):
        for i in range(1, self.num_episodes):
            current_state_left, current_state_right = self.env.get_state()
            self.update_epsilon()
            done = False

            while not done:
                action_left = self.get_action_left(current_state_left)
                action_right = self.get_action_right(current_state_right)

                new_state_left, new_state_right, reward_left, reward_right, done = self.env.step(self.actions_left[action_left], self.actions_right[action_right])

                self.q_values_left[current_state_left][action_left] = (1 - self.learning_rate)\
                    * self.q_values_left[current_state_left][action_left] + self.learning_rate\
                    * (reward_left + self.discount_factor * max(self.q_values_left[new_state_left]))
                
                self.q_values_right[current_state_right][action_right] = (1 - self.learning_rate)\
                    * self.q_values_right[current_state_right][action_right] + self.learning_rate\
                    * (reward_right + self.discount_factor * max(self.q_values_right[new_state_right]))
            
            self.env.new_game()