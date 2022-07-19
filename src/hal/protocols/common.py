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
from hal.protocols.crsf import CRSF_RC_Generator
import target
import time
import uasyncio as asyncio

class CRSF:
    def __init__(self):
        print(str(time.ticks_us()) + " [Create] CRSF object")
        self.arm_time       = 0
        self.packets_count  = 0     # number of packets sent 
        self.marker         = 'L'   # marker
        self.arm_state      = False # disarm, True = arm
        self.inject_mode = "OFF"    # OFF, ON
        self.erase_flag     = False # do nothing, True = erase
        print(str(time.ticks_us()) + " [Create] UART1")
        self.uart           = target.init_fc_uart()
        print(str(time.ticks_us()) + " [  OK  ] UART1")

        print(str(time.ticks_us()) + " [Create] AJ pin")
        self.audio          = target.init_audio()
        print(str(time.ticks_us()) + " [  OK  ] AJ pin")
        print(str(time.ticks_us()) + " [Create] CRSF Generator")
        self.crsf_gen = CRSF_RC_Generator()
        print(str(time.ticks_us()) + " [  OK  ] CRSF Generator")
        self.disarm_packet  = self.crsf_gen.build_rc_packet(992,992,189,992,189,992,992,992,
                                                            992,992,992,992,992,992,992,992)
        self.arm_packet     = self.crsf_gen.build_rc_packet(992,992,189,992,1800,992,992,992,
                                                            992,992,992,992,992,992,992,992)
        self.marker_packet  = self.crsf_gen.build_rc_packet(992,992,1800,992,1800,992,992,992,
                                                            992,992,992,992,992,992,992,992)
        self.erase_packet   = self.crsf_gen.build_rc_packet(992,992,189,992,189,1800,992,992,
                                                            992,992,992,992,992,992,992,992)
        print(str(time.ticks_us()) + " [  OK  ] CRSF object")

    async def uart_handler(self):
        print(str(time.ticks_us()) + " [  OK  ] Async CRSF listener")
        swriter = asyncio.StreamWriter(self.uart, {})
        sreader = asyncio.StreamReader(self.uart)
        while True:
            data = await sreader.read(n=-1)
            print("FC sent:", data)

    def _toggle_marker_(self):  #toggle the marker
        if self.marker == 'L':
            self.marker = 'H'
        else:
            self.marker = 'L'

    def _inject_(self):
        if self.marker == "L":
            self.uart.write(self.arm_packet)  # low throttle
            self.audio.value(0)          # low voltage on audio
        elif self.marker == "H":
            self.uart.write(self.marker_packet)# high throttle
            self.audio.value(1)          # high voltage on audio

    def send_packet(self, t):
        if (self.arm_state == True) & (self.inject_mode == "OFF"):
            self.uart.write(self.arm_packet)  # just ARM the FC 

        elif (self.arm_state == True) & (self.inject_mode == "ON"):
            self.arm_time = self.arm_time + 5   # 5ms per call

            if self.arm_time < 1000:            # in first second we don't inject
                self.uart.write(self.arm_packet)
            elif self.arm_time >= 1000:         # after that we start to inject
                self._inject_()
                self.packets_count = self.packets_count + 1
                if self.packets_count >= 8:
                    self._toggle_marker_()
                    self.packets_count = 0

        elif self.arm_state == False:
            self.arm_time = 0
            if self.erase_flag == False:
                self.uart.write(self.disarm_packet)
            elif self.erase_flag == True:
                self.uart.write(self.erase_packet)
            self.packets_count = 0
            self.marker = "L"
