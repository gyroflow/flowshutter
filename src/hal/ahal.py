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
import hal.peripherals as peripherals
import hal.protocols.common as fc_link


class AsnycPeripherals:
    def __init__(self, camera = None):
        self.buttons = peripherals.Buttons()
        self.battery = peripherals.Battery()
        self.init_camera(camera)
        # self.fc_link = fc_link.uart_handler()

    def init_camera(self, camera):
        if camera == "NO":
            from hal.camera.no import No_Cam as camera
        elif camera == "SONY MTP":
            from hal.camera.sony import Sony_multi as camera
        elif camera == "LANC":
            from hal.camera.lanc import LANC as camera
        elif camera == "ZCAM UART":
            from hal.camera.zcam import ZCAM_UART as camera
        elif camera == "MMTRY GND":
            from hal.camera.momentary_ground import Momentary_ground as camera
        elif camera == "3V3 Schmitt":
            from hal.camera.schmitt_3v3 import Schmitt_3v3 as camera
        self.camera = camera()
