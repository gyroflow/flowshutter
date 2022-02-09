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
from machine import Pin, UART, Timer
import crsf, oled, target, sony_multiport
import uasyncio as asyncio
from time import sleep

oled1 = oled.oled_init()

uart1, _, _, button1, button2 = target.init_pins()
fc_arm_packet, fc_disarm_packet = crsf.init_packet()
state = ['idle', 'starting', 'recording', 'stopping', 'stopped']

button1_press_count = 0
button1_trigger = 0
button2_press_count = 0
button2_trigger = 0
arm_flag=0
switching_flag = 0
def check_button(t):
    global button1_press_count
    global button1_trigger
    global button2_press_count
    global button2_trigger
    global switching_flag
    if button1.value() == 0:
        if button1_press_count <=100:
            button1_press_count += 1
        else:
            button1_press_count = 0
            button1_trigger = 1
            if current_state == state[0]:
                switching_flag = 1
            print('button1 tiggered', button1_trigger)
            print('switching_flag', switching_flag)
    else:
        button1_press_count = 0
    if button2.value() == 0:
        if button2_press_count <=100:
            button2_press_count += 1
        else:
            button2_press_count = 0
            button2_trigger = 1

timer0 = Timer(0)
timer0.init(period=5, mode=Timer.PERIODIC, callback=check_button)

def send_crsf_packet(t):
    global arm_flag
    if arm_flag == 1:
        uart1.write(fc_arm_packet)
    else:
        uart1.write(fc_disarm_packet)
timer1 = Timer(1)
timer1.init(period=4, mode=Timer.PERIODIC, callback=send_crsf_packet)

camera_uart_handler = sony_multiport.uart_handler()

loop = asyncio.get_event_loop()
loop.create_task(camera_uart_handler)
loop.run_forever()