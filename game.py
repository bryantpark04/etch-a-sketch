import pygame

def game_loop() -> None:
    while True:
        for event in pygame.event.get():
            if (event.type != pygame.KEYDOWN): continue
            print(chr(event.key))
            if (event.key == ord('q')):
                return

def main() -> None:
    lcd = pygame.display.set_mode((320, 240))
    pygame.init()

    try:
        game_loop()
    finally:
        pygame.quit()


if __name__ == "__main__":
    main()