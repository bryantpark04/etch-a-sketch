import pygame
import sys

COLORS = [(0, 0,0), (255,0,0), (0,255,0), (0,0,255)]
PIXEL_SIZE = 3

DIR_DOWN = pygame.math.Vector2(0, 1)
DIR_RIGHT = pygame.math.Vector2(1, 0)

COLOR_WHITE = pygame.Color(255, 255, 255)
COLOR_BLACK = pygame.Color(0, 0, 0)

COLOR_BACKGROUND = COLOR_WHITE
COLOR_TEXT = COLOR_BLACK

FONT = pygame.font.Font(None, 20)

IS_RUNNING_ON_PI = not ("--no-pi" in sys.argv)