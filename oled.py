from machine import Pin, I2C
import ssd1306, time, target

def oled_init():
    _,_,i2c,_ = target.init_pins()
    display = ssd1306.SSD1306_I2C(128, 32, i2c)
    display.fill(0)
    # we need to replace flowshutter logo later
    display.fill_rect(0, 0, 32, 32, 1)
    display.fill_rect(2, 2, 28, 28, 0)
    display.vline(9, 8, 22, 1)
    display.vline(16, 2, 22, 1)
    display.vline(23, 8, 22, 1)
    display.fill_rect(26, 24, 2, 4, 1)
    # end logo
    display.text('FlowShutter', 40, 0, 1)
    display.text('Powered by', 40, 12, 1)
    display.text('DusKing 1.4', 40, 24, 1)
    display.show()
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