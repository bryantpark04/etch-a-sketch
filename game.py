import pygame
from dataclasses import dataclass, astuple
import sys

pygame.init()

PIXEL_SIZE = 3

DIR_DOWN = pygame.math.Vector2(0, 1)
DIR_RIGHT = pygame.math.Vector2(1, 0)

COLOR_WHITE = pygame.Color(255, 255, 255)
COLOR_BLACK = pygame.Color(0, 0, 0)

COLOR_BACKGROUND = COLOR_WHITE
COLOR_TEXT = COLOR_BLACK

FONT = pygame.font.Font(None, 20)


@dataclass
class GameState:
    cursor: pygame.math.Vector2

state = GameState(pygame.math.Vector2(160, 120))


def handle_events(lcd: pygame.Surface) -> None:
    for event in pygame.event.get():
        if event.type != pygame.KEYDOWN: continue
        if event.key == pygame.K_q: 
            pygame.quit()
            sys.exit(0)
        if event.key == pygame.K_c:
            lcd.fill(COLOR_WHITE)
        if event.key == pygame.K_s:
            file_name: str = f"{state.cursor[0]}_{state.cursor[1]}.bmp"
            pygame.image.save(lcd, file_name)
        if event.key == pygame.K_UP:
            state.cursor -= PIXEL_SIZE * DIR_DOWN
        if event.key == pygame.K_DOWN:
            state.cursor += PIXEL_SIZE * DIR_DOWN
        if event.key == pygame.K_LEFT:
            state.cursor -= PIXEL_SIZE * DIR_RIGHT
        if event.key == pygame.K_RIGHT:
            state.cursor += PIXEL_SIZE * DIR_RIGHT


def render_game(lcd: pygame.Surface) -> None:
    pygame.draw.rect(lcd, COLOR_BLACK, pygame.Rect(state.cursor, (PIXEL_SIZE, PIXEL_SIZE)))

    pygame.display.update()


def main() -> None:
    lcd = pygame.display.set_mode((320, 240))

    lcd.fill(COLOR_BACKGROUND)

    while True:
        handle_events(lcd)
        render_game(lcd)
        


if __name__ == "__main__":
    main()