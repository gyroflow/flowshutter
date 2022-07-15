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
import vram, target
import time
from camera.common import Camera

class Schmitt_3v3(Camera):
    def __init__(self):
        print(str(time.ticks_us()) + " [Create] Schmitt 3v3 object")
        self.pin = target.init_schmitt_3v3_trigger_pin()
        super().__init__("NO")
        print(str(time.ticks_us()) + " [  OK  ] Schmitt 3v3 object")

    def toggle_cc_voltage_level(self, argv):
        if argv == "pass":
            pass
        elif vram.sub_state == "STOPPING":
            vram.sub_state = "HOME"
            self.pin.value(0)
            vram.arm_state = "disarm"
        elif vram.sub_state == "STARTING":
            vram.sub_state = "RECORDING"
            self.pin.value(1)
            vram.arm_state = "arm"

    def rec(self):
        self.rec_event(self.toggle_cc_voltage_level, 'pass', self.toggle_cc_voltage_level,'react')
