# Flowshutter
# Copyright (C) 2021  Hugo Chiang

# Flowshutter is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# Flowshutter is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with flowshutter.  If not, see <https://www.gnu.org/licenses/>.
from machine import ADC
from machine import I2C
from machine import Pin
from machine import UART
import time

name = "DIY_FC"
oled_height = 32

def init_adc():
    print(str(time.ticks_us()) + " [ Init ] ADC")
    adc = ADC(Pin(34))
    adc.atten(ADC.ATTN_11DB)
    scale = 1
    offset = 0
    return adc, scale, offset

def init_fc_uart():
    print(str(time.ticks_us()) + " [ Init ] UART1")
    uart1 = UART(1, baudrate=420000, bits = 8, parity = None, stop = 1, tx = 33, rx = 32)
    return uart1

def init_audio():
    print(str(time.ticks_us()) + " [ Init ] AJ pin")
    audio_pin = Pin(18, Pin.OUT)
    return audio_pin

def init_i2c():
    print(str(time.ticks_us()) + " [ Init ] I2C")
    i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq = 1000000)
    return i2c

def init_buttons():
    print(str(time.ticks_us()) + " [ Init ] buttons")
    button_page_up  = Pin(2, Pin.IN, Pin.PULL_UP)
    button_enter    = Pin(27, Pin.IN, Pin.PULL_UP)
    button_page_down= Pin(15, Pin.IN, Pin.PULL_UP)
    return button_page_up, button_enter, button_page_down

def init_mtp_uart():
    print(str(time.ticks_us()) + " [ Init ] UART2 sony mtp")
    uart2 = UART(2, baudrate = 9600,    bits = 8,   parity = 0,     stop = 1,   tx = 25,rx = 26)
    return uart2

def init_zcam_uart():
    print(str(time.ticks_us()) + " [ Init ] UART2 zcam uart")
    uart2 = UART(2, baudrate = 115200,  bits = 8,   parity = None,  stop = 1,   tx = 25,rx = 26)
    return uart2

def init_uart2_tx():
    print(str(time.ticks_us()) + " [ Init ] UART2 TX")
    # uart2_tx = UART(2,baudrate = 9600, bits = 8, parity = None, stop =1, tx = 25)
    uart2_tx = Pin(25, Pin.OUT, value = 1)
    return uart2_tx

def init_lanc_detect_pin():
    print(str(time.ticks_us()) + " [ Init ] LANC detect pin")
    detect = Pin(26, Pin.IN, Pin.PULL_UP)
    return detect

def init_lanc_test_pin():
    print(str(time.ticks_us()) + " [ Init ] LANC text pin")
    test = Pin(2, Pin.OUT, value = 1)
    return test

def init_momentary_ground_pin():
    print(str(time.ticks_us()) + " [ Init ] MMTRY GND pin")
    switch = Pin(25, Pin.OPEN_DRAIN, value = 1)
    return switch

def init_schmitt_3v3_trigger_pin():
    print(str(time.ticks_us()) + " [ Init ] schmitt")
    schmitt_3v3 = Pin(26, Pin.OUT, value = 0)
    return schmitt_3v3
