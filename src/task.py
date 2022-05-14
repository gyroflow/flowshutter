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
import camera, crsf, vram, peripherals, ui
import time

class Task:
    def __init__(self):
        print(str(time.ticks_us()) + " [Create] Task schedular")
        self.crsf = crsf.CRSF()
        self.canvas = ui.canvas
        self.battery = peripherals.Battery()
        self.buttons = peripherals.Buttons()
        print(str(time.ticks_us()) + " [  OK  ] Task schedular")

    def schedular(self, t):

        # task1
        self.crsf.send_packet(t)

        # task2
        if vram.oled_tasklist != []:
            # print(vram.oled_tasklist)
            i = vram.oled_tasklist[0]
            self.canvas.show_sub(i)
            del vram.oled_tasklist[0]

        # task3
        self.battery.read_vol()

        # task4
        self.buttons.check(t)

