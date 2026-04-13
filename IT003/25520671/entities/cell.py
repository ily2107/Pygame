import pygame
from setting import *

class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.type = "Wall"    