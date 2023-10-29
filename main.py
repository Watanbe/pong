import pygame as pg
from game import Game
from qlearning import QLearning

if __name__ == '__main__':
    QLearning(Game()).train()