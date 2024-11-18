import pygame
from dataclasses import dataclass, astuple
import sys

pygame.init()

COLOR_WHITE = pygame.Color(255, 255, 255)
COLOR_BLACK = pygame.Color(0, 0, 0)

COLOR_BACKGROUND = COLOR_WHITE
COLOR_TEXT = COLOR_BLACK

FONT = pygame.font.Font(None, 20)

@dataclass
class Coords:
    x: int
    y: int

@dataclass
class GameState:
    cursor: Coords

state = GameState(Coords(160, 120))


def handle_events() -> None:
    for event in pygame.event.get():
        if (event.type != pygame.KEYDOWN): continue
        if (event.key == pygame.K_q): 
            pygame.quit()
            sys.exit(0)
        match event.key:
            case pygame.K_UP:
                state.cursor.y -= 1
            case pygame.K_DOWN:
                state.cursor.y += 1
            case pygame.K_LEFT:
                state.cursor.x -= 1
            case pygame.K_RIGHT:
                state.cursor.x += 1


def render_game(lcd: pygame.Surface) -> None:
    lcd.set_at(astuple(state.cursor), COLOR_BLACK)

    pygame.display.update()


def main() -> None:
    lcd = pygame.display.set_mode((320, 240))

    lcd.fill(COLOR_BACKGROUND)

    while True:
        handle_events()
        render_game(lcd)
        


if __name__ == "__main__":
    main()