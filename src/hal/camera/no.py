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
import time
from hal.camera.common import Camera

class No_Cam(Camera):
    def __init__(self):
        print(str(time.ticks_us()) + " [Create] No camera object")
        super().__init__("NO")
        print(str(time.ticks_us()) + " [  OK  ] No camera object")

    def no_cam(self, argv):
        if argv == "pass":
            pass
        else:
            if self.state == True:
                self.state = False
            elif self.state == False:
                self.state = True

    def rec(self):
        self.rec_event(self.no_cam, 'pass', self.no_cam, 'react')
