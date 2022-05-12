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
import camera, crsf, vars, oled, peripherals

crsf = crsf.CRSF()
oled = oled.screen
battery = peripherals.Battery()
buttons = peripherals.Buttons()

def schedular(t):
    # task1
    crsf.send_packet(t)

    # task2
    if vars.oled_tasklist != []:
        # print("oled task not empty!")
        # print(vars.oled_tasklist)
        i = vars.oled_tasklist[0]
        oled.show_sub(i)
        del vars.oled_tasklist[0]
    else:
        pass
        # print("no oled task")

    # task3
    battery.read_vol()  # read the battery voltage

    # task4
    buttons.check(t)    # check the buttons
