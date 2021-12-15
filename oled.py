from machine import Pin, I2C
import ssd1306, time

def oled_init():
    i2c = I2C(-1, scl=Pin(22), sda=Pin(21)) #For ESP32: pin initializing
    display = ssd1306.SSD1306_I2C(128, 64, i2c)
    display.fill(0)
    display.fill_rect(0, 0, 32, 32, 1)
    display.fill_rect(2, 2, 28, 28, 0)
    display.vline(9, 8, 22, 1)
    display.vline(16, 2, 22, 1)
    display.vline(23, 8, 22, 1)
    display.fill_rect(26, 24, 2, 4, 1)
    display.text('MicroPython', 40, 0, 1)
    display.text('SSD1306', 40, 12, 1)
    display.text('OLED 128x64', 40, 24, 1)
    display.text('Hacked by', 0, 36, 1)
    display.text('DusKing 1.4', 0, 48, 1)
    display.show()
    time.sleep(1)
    return display

def show_arm_info(display):
    display.fill(0)
    display.text('Armed', 0, 0, 1)
    display.show()

def show_disarm_info(display):
    display.fill(0)
    display.text('Disarmed', 0, 0, 1)
    display.show()

def show_cam_press_info(display):
    display.fill(0)
    display.text('Cam Pressed', 0, 0, 1)
    display.show()

def show_cam_release_info(display):
    display.fill(0)
    display.text('Cam Released', 0, 0, 1)
    display.show()