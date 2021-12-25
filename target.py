from machine import UART, Pin, I2C

def init_pins():
    uart1 = UART(1, baudrate=420000, bits = 8, parity = None, stop = 1, tx = 33, rx = 32)
    uart2 = UART(2, baudrate = 9600, bits = 8, parity = 0,    stop = 1, tx = 25, rx = 26)
    i2c = I2C(-1, scl=Pin(22), sda=Pin(21))
    button1 = Pin(19, Pin.IN, Pin.PULL_UP)
    button2 = Pin(18, Pin.IN, Pin.PULL_UP)

    return uart1, uart2, i2c, button1, button2