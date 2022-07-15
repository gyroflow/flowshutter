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

class Momentary_ground(Camera):
    def __init__(self):
        print(str(time.ticks_us()) + " [Create] Momentary ground object")
        self.pin = target.init_momentary_ground_pin()
        super().__init__("NO")
        print(str(time.ticks_us()) + " [  OK  ] Momentary ground object")

    def momentary_ground(self,value):
        # 1 High impedance (open drain)
        # 0 Low voltage (tied to ground)
        self.pin.value(value)
        if value == 1:
            if vram.sub_state == "STOPPING":
                vram.sub_state = "HOME"
                vram.arm_state = "disarm"
            elif vram.sub_state == "STARTING":
                vram.sub_state = "RECORDING"
                vram.arm_state = "arm"

    def rec(self):
        self.rec_event(self.momentary_ground, 0, self.momentary_ground, 1)
