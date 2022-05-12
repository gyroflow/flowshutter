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
import crsf_gen,target, vram

class CRSF:
    def __init__(self):
        print("[Create] CRSF object")
        self.arm_time       = 0
        self.packets_count  = 0     # number of packets sent 
        self.marker         = 'L'   # marker
        print("[Create] UART1")
        self.uart           = target.init_crsf_uart()
        print("[  OK  ] UART1")

        print("[Create] AJ pin")
        self.audio          = target.init_audio()
        print("[  OK  ] AJ pin")
        self.disarm_packet  = crsf_gen.build_rc_packet( 992,992,189,992,189,992,992,992,
                                                        992,992,992,992,992,992,992,992)
        self.arm_packet     = crsf_gen.build_rc_packet( 992,992,189,992,1800,992,992,992,
                                                        992,992,992,992,992,992,992,992)
        self.marker_packet  = crsf_gen.build_rc_packet( 992,992,1800,992,1800,992,992,992,
                                                        992,992,992,992,992,992,992,992)
        print("[  OK  ] CRSF object")

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
        if (vram.arm_state == "arm") & (vram.inject_mode == "OFF"):
            self.uart.write(self.arm_packet)  # just ARM the FC 

        elif (vram.arm_state == "arm") & (vram.inject_mode == "ON"):
            self.arm_time = self.arm_time + 5   # 5ms per call

            if self.arm_time < 1000:            # in first second we don't inject
                self.uart.write(self.arm_packet)
            elif self.arm_time >= 1000:         # after that we start to inject
                self._inject_()
                self.packets_count = self.packets_count + 1
                if self.packets_count >= 8:
                    self._toggle_marker_()
                    self.packets_count = 0

        elif vram.arm_state == "disarm":
            self.arm_time = 0
            self.uart.write(self.disarm_packet)
            self.packets_count = 0
            self.marker = "L"
