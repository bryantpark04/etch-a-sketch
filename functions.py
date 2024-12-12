import time
import pygame
import glob
import sys

from common import *

def save_image(lcd, state):
    filename: str = f"{time.time()}_{state.cursor[0]}_{state.cursor[1]}.bmp"
    pygame.image.save(lcd, filename)

def cycle_color(state):
    state.color = (state.color + 1) % len(COLORS)

def load_previous_image(lcd, state):
    bmp_files = glob.glob("*.bmp")
    if not bmp_files:
        return
    filename = sorted(bmp_files, reverse=True)[state.loaded_image]
    state.loaded_image = (state.loaded_image + 1) % len(bmp_files)
    img = pygame.image.load(filename)
    pygame.Surface.blit(lcd, img, (0, 0))
    new_cursor_pos = list(map(float, filename[:filename.find(".bmp")].split('_')))
    state.cursor = pygame.math.Vector2(new_cursor_pos[1], new_cursor_pos[2])
    pygame.display.update()

def clear_screen(lcd, state):
    lcd.fill(COLOR_WHITE)
    pygame.display.update()
    state.loaded_image = 0

def quit():
    pygame.quit()
    sys.exit(0)