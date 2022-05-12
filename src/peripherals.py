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
import target, vars

class Battery:
    def __init__(self):
        print("peri battery")
        self.adc1, self.adc2 = target.init_adc()
        self.adc_read_time_count = 0

    def read_vol(self):
        self.adc_read_time_count += 5
        if self.adc_read_time_count >= 50:
            self.adc_read_time_count = 0
            if self.adc1.read() != 0:
                vars.vol = (vars.vol + self.adc1.read() * 3.3 / 2048)/2
            else:
                vars.vol = (vars.vol + self.adc2.read() * 3.3 / 4096)/2


class Buttons:
    def __init__(self):
        print("peri button")
        self.page, self.enter = target.init_buttons()
        self.page_press_count = 0
        self.enter_press_count = 0
    
    def check(self, t):
        if self.page.value() == 0:
            if self.page_press_count <= 100:
                self.page_press_count += 5
            else:
                self.page_press_count = 0
                vars.button_page = "pressed"
        else:
            self.page_press_count = 0

        if self.enter.value() == 0:
            if self.enter_press_count <= 100:
                self.enter_press_count += 5
            else:
                self.enter_press_count = 0
                vars.button_enter = "pressed"
        else:
            self.enter_press_count = 0
