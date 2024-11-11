import pygame


pygame.init()

COLOR_WHITE = pygame.Color(255, 255, 255)
COLOR_BLACK = pygame.Color(0, 0, 0)

COLOR_BACKGROUND = COLOR_WHITE
COLOR_TEXT = COLOR_BLACK

FONT = pygame.font.Font(None, 20)

state = {'key': ''} # TODO replace with dataclass


def handle_events() -> None:
    for event in pygame.event.get():
        if (event.type != pygame.KEYDOWN): continue
        if (event.key == ord('q')): pygame.quit()
        state['key'] = chr(event.key)


def render_game(lcd: pygame.Surface) -> None:
    lcd.fill(COLOR_BACKGROUND)
    lcd.blit(FONT.render(state['key'], True, COLOR_TEXT), (0, 0))
    pygame.display.update()



def main() -> None:
    lcd = pygame.display.set_mode((320, 240))

    while True:
        handle_events()
        render_game(lcd)
        


if __name__ == "__main__":
    main()