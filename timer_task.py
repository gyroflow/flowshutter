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
from machine import Timer


button1_press_count = 0
button1_trigger = 0
button2_press_count = 0
button2_trigger = 0

def check_button(t):
    global button1_press_count
    global button1_trigger
    global button2_press_count
    global button2_trigger
    if button1.value() == 0:
        if button1_press_count <=100:
            button1_press_count += 1
        else:
            button1_press_count = 0
            button1_trigger = 1
            print('button1 tiggered', button1_trigger)
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