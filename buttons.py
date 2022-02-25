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
button_start = target.init_buttons()

#private variable
button_start_press_count = 0


def check(t):
    global button_start_press_count
        
    if button_start.value() == 0:
        if button_start_press_count <=50:
            button_start_press_count += 1
        else:
            button_start_press_count = 0
            vars.button_start = "pressed"
            print('button_start ', vars.button_start)
