import pygame
from dataclasses import dataclass, astuple
import glob
import sys
import time
import board
import digitalio
import busio
import adafruit_lis3dh
import smbus
import RPi.GPIO as GPIO

pygame.init()

PIXEL_SIZE = 3

DIR_DOWN = pygame.math.Vector2(0, 1)
DIR_RIGHT = pygame.math.Vector2(1, 0)

COLOR_WHITE = pygame.Color(255, 255, 255)
COLOR_BLACK = pygame.Color(0, 0, 0)

COLOR_BACKGROUND = COLOR_WHITE
COLOR_TEXT = COLOR_BLACK

FONT = pygame.font.Font(None, 20)

i2c = busio.I2C(board.SCL, board.SDA)
int1 = digitalio.DigitalInOut(board.D20)
lis3dh = adafruit_lis3dh.LIS3DH_I2C(i2c, int1=int1)

bus = smbus.SMBus(1)
time.sleep(1)


clk_x = 19
dt_x = 26
clk_y = 21
dt_y = 6

GPIO.setmode(GPIO.BCM)
GPIO.setup(clk_x, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(dt_x, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(clk_y, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(dt_y, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

clkLastState_x = GPIO.input(clk_x)
clkLastState_y = GPIO.input(clk_y)
clkState_x = 0
dtState_x = 0
clkState_y = 0
dtState_y = 0

COLORS = [(0, 0,0), (255,0,0), (0,255,0), (0,0,255)]

@dataclass
class GameState:
    cursor: pygame.math.Vector2
    color = 0
    loaded_image = 0

state = GameState(pygame.math.Vector2(160, 120))


def callback(channel, lcd):
    print(f"Button {channel} was pressed")
    time.sleep(0.001)
    if channel == 17:
        state.color = (state.color + 1) % len(COLORS)
    if channel == 22:
        filename: str = f"{time.time()}_{state.cursor[0]}_{state.cursor[1]}.bmp"
        pygame.image.save(lcd, filename)
    if channel == 23:
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
    if channel == 27:
        pygame.quit()
        sys.exit(0)




def handle_events(lcd: pygame.Surface) -> None:
    global clkLastState_x, clkLastState_y, clkState_x, clkState_y, dtState_x, dtState_y
    ax,ay,az = lis3dh.acceleration
    acceleration = (ax ** 2 + ay ** 2 + az ** 2) / (9.8 ** 2)
    time.sleep(0.001)
    
    if acceleration > 5:        
        lcd.fill(COLOR_WHITE)
        pygame.display.update()
        state.loaded_image = 0

    
    counter_x = 0
    counter_y = 0
    clkState_x = GPIO.input(clk_x)
    dtState_x = GPIO.input(dt_x)
    if clkState_x != clkLastState_x:
        if dtState_x != clkState_x:
            counter_x += 1
        else:
            counter_x -= 1
            

    clkLastState_x = clkState_x
        
    clkState_y = GPIO.input(clk_y)
    dtState_y = GPIO.input(dt_y)
    if clkState_y != clkLastState_y:
        if dtState_y != clkState_y:
            counter_y += 1
        else:
            counter_y -= 1
        
    clkLastState_y = clkState_y
    
    state.cursor += PIXEL_SIZE * DIR_DOWN * counter_y + PIXEL_SIZE * DIR_RIGHT * counter_x

    if counter_x or counter_y:
        state.loaded_image = 0
        
            
    for event in pygame.event.get():
        if event.type != pygame.KEYDOWN: continue
        if event.key == pygame.K_q: 
            pygame.quit()
            sys.exit(0)
        if event.key == pygame.K_c:
            lcd.fill(COLOR_WHITE)
            pygame.display.update()
        if event.key == pygame.K_s:
            pygame.quit()
            sys.exit(0)
            filename: str = f"{time.time()}_{state.cursor[0]}_{state.cursor[1]}.bmp"
            pygame.image.save(lcd, filename)
            filename: str = f"{time.time()}_{state.cursor[0]}_{state.cursor[1]}.bmp"
            pygame.image.save(lcd, filename)
        if event.key == pygame.K_l:
            bmp_files = glob.glob("*.bmp")
            if not bmp_files:
                continue
            filename = sorted(bmp_files, reverse=True)[0]
            img = pygame.image.load(filename)
            pygame.Surface.blit(lcd, img, (0, 0))
            new_cursor_pos = list(map(float, filename[:filename.find(".bmp")].split('_')))
            state.cursor = pygame.math.Vector2(new_cursor_pos[1], new_cursor_pos[2])
            pygame.display.update()
            
        
        if event.key == pygame.K_UP:
            state.cursor -= PIXEL_SIZE * DIR_DOWN
        if event.key == pygame.K_DOWN:
            state.cursor += PIXEL_SIZE * DIR_DOWN
        if event.key == pygame.K_LEFT:
            state.cursor -= PIXEL_SIZE * DIR_RIGHT
        if event.key == pygame.K_RIGHT:
            state.cursor += PIXEL_SIZE * DIR_RIGHT


def render_game(lcd: pygame.Surface) -> None:
    pygame.draw.rect(lcd, COLORS[state.color], pygame.Rect(state.cursor, (PIXEL_SIZE, PIXEL_SIZE)))

    pygame.display.update()
    # ax,ay,az = lis3dh.acceleration


def main() -> None:
    lcd = pygame.display.set_mode((320, 240))
    
    

    channels = [17, 22, 23, 27]
    for channel in channels:
        GPIO.setup(channel, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(channel, GPIO.FALLING, callback=lambda c: callback(c, lcd), bouncetime=300)

    lcd.fill(COLOR_BACKGROUND)

    pygame.mouse.set_visible(False)

    while True:    
        # ax,ay,az = lis3dh.acceleration
        handle_events(lcd)
        render_game(lcd)
        


if __name__ == "__main__":
    main()
