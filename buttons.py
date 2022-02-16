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
button_page, button_enter = target.init_buttons()

button_page_press_count = 0
button_enter_press_count = 0

def check(t):
    global button_page_press_count
    global button_enter_press_count
    if button_page.value() == 0:
        if button_page_press_count <=20:   # dead time is 20*5 = 100ms = 0.1s
            button_page_press_count += 1
        else:
            button_page_press_count = 0
            vars.button_page = "pressed"
            print('button_page ', vars.button_page)
            
    else:
        button_page_press_count = 0
    if button_enter.value() == 0:
        if button_enter_press_count <=50:
            button_enter_press_count += 1
        else:
            button_enter_press_count = 0
            vars.button_enter = "pressed"
            print('button_enter ', vars.button_enter)