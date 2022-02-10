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
import vars, target
button1, button2 = target.init_buttons()

button1_press_count = 0
button2_press_count = 0

def check(t):
    global button1_press_count
    global button2_press_count
    if button1.value() == 0:
        if button1_press_count <=100:   # dead time is 100*5 = 500ms = 0.5s
            button1_press_count += 1
        else:
            button1_press_count = 0
            vars.button1_trigger = "yes"
            print('button1 tiggered', vars.button1_trigger)
    else:
        button1_press_count = 0
    if button2.value() == 0:
        if button2_press_count <=100:
            button2_press_count += 1
        else:
            button2_press_count = 0
            vars.button2_trigger = "yes"
            print('button2 triggered', vars.button2_trigger)