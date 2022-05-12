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
import target, vram
import time

class Battery:
    def __init__(self):
        print(str(time.ticks_us()) + " [Create] Battery object")
        print(str(time.ticks_us()) + " [Create] ADC")
        self.adc1, self.adc2 = target.init_adc()
        print(str(time.ticks_us()) + " [  OK  ] ADC")
        self.adc_read_time_count = 0
        print(str(time.ticks_us()) + " [  OK  ] Battery object")

    def read_vol(self):
        self.adc_read_time_count += 5
        if self.adc_read_time_count >= 50:
            self.adc_read_time_count = 0
            if self.adc1.read() != 0:
                vram.vol = (vram.vol + self.adc1.read() * 3.3 / 2048)/2
            else:
                vram.vol = (vram.vol + self.adc2.read() * 3.3 / 4096)/2


class Buttons:
    def __init__(self):
        print(str(time.ticks_us()) + " [Create] Buttons object")
        print(str(time.ticks_us()) + " [Create] buttons")
        self.page, self.enter = target.init_buttons()
        print(str(time.ticks_us()) + " [  OK  ] buttons")
        self.page_press_count = 0
        self.enter_press_count = 0
        print(str(time.ticks_us()) + " [  OK  ] Buttons object")
    
    def check(self, t):
        if self.page.value() == 0:
            if self.page_press_count <= 100:
                self.page_press_count += 5
            else:
                self.page_press_count = 0
                vram.button_page = "pressed"
        else:
            self.page_press_count = 0

        if self.enter.value() == 0:
            if self.enter_press_count <= 100:
                self.enter_press_count += 5
            else:
                self.enter_press_count = 0
                vram.button_enter = "pressed"
        else:
            self.enter_press_count = 0
