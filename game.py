import pygame
import time

pygame.init()

from functions import *
from common import *

state = GameState(pygame.math.Vector2(160, 120))

if IS_RUNNING_ON_PI:
    import board
    import digitalio
    import busio
    import adafruit_lis3dh
    import smbus
    import RPi.GPIO as GPIO

    i2c = busio.I2C(board.SCL, board.SDA)
    int1 = digitalio.DigitalInOut(board.D20)
    lis3dh = adafruit_lis3dh.LIS3DH_I2C(i2c, int1=int1)
    bus = smbus.SMBus(1)
    time.sleep(1)


    GPIO.setmode(GPIO.BCM)
    for i in range(2):
        GPIO.setup(clks[i], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(dts[i], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        state.clk_last_state[i] = GPIO.input(clks[i])


def callback(channel, lcd):
    print(f"Button {channel} was pressed")
    time.sleep(0.001)
    if channel == 17:
        cycle_color(state)
    if channel == 22:
        save_image(lcd, state)
    if channel == 23:
        load_previous_image(lcd, state)
    if channel == 27:
        quit()

def read_rotary_encoders(i, state):
    clk_state = GPIO.input(clks[i])
    dt_state = GPIO.input(dts[i])
    direction = 0
    if clk_state != state.clk_last_state[i]:
        if dt_state != clk_state:
            direction = 1
        else:
            direction = -1
    state.clk_last_state[i] = clk_state
    if direction != 0:
        state.loaded_image = 0
    return direction

def handle_events(lcd: pygame.Surface) -> None:
    if IS_RUNNING_ON_PI:
        global clkLastState_x, clkLastState_y, clkState_x, clkState_y, dtState_x, dtState_y
        ax,ay,az = lis3dh.acceleration
        acceleration = (ax ** 2 + ay ** 2 + az ** 2) / (9.8 ** 2)
        time.sleep(0.001)
        
        if acceleration > 5:
            clear_screen(lcd, state)
        
        state.cursor += PIXEL_SIZE * DIR_DOWN * read_rotary_encoders(1, state) + PIXEL_SIZE * DIR_RIGHT * read_rotary_encoders(0, state)        
            
    for event in pygame.event.get():
        if event.type != pygame.KEYDOWN: continue
        if event.key == pygame.K_q: 
            quit()
        if event.key == pygame.K_c:
            clear_screen(lcd, state)
        if event.key == pygame.K_s:
            save_image(lcd, state)
        if event.key == pygame.K_l:
            load_previous_image(lcd, state)
            
        
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


def main() -> None:
    lcd = pygame.display.set_mode((320, 240))

    if IS_RUNNING_ON_PI:
        channels = [17, 22, 23, 27]
        for channel in channels:
            GPIO.setup(channel, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            GPIO.add_event_detect(channel, GPIO.FALLING, callback=lambda c: callback(c, lcd), bouncetime=300)

    clear_screen(lcd, state)

    pygame.mouse.set_visible(False)

    while True:    
        handle_events(lcd)
        render_game(lcd)


if __name__ == "__main__":
    main()
