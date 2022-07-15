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
import uasyncio as asyncio
import vram, target
import time
from camera.common import Camera

class Sony_multi(Camera):
    def __init__(self):
        print(str(time.ticks_us()) + " [Create] SONY MTP object")
        self.REC_PRESS      = b'#7100*'    # record button pressed
        self.REC_RELEASE    = b'#7110*'    # record button released

        self.HANDSHAKE      = b'%000*'
        self.HANDSHAKE_ACK  = b'&00080*'

        self.REC_START      = b'%7610*'
        self.REC_START_ACK  = b'&76100*'

        self.REC_STOP       = b'%7600*'
        self.REC_STOP_ACK   = b'&76000*'

        print(str(time.ticks_us()) + " [Create] UART2")
        self.uart = target.init_mtp_uart()
        print(str(time.ticks_us()) + " [  OK  ] UART2")
        super().__init__("ASYNC")
        print(str(time.ticks_us()) + " [  OK  ] SONY MTP object")

    def rec_button(self,argv):
        if argv == "press":
            self.uart.write(self.REC_PRESS)
        elif argv == "release":
            self.uart.write(self.REC_RELEASE)
        print("shutter send: ", self.REC_PRESS)

    def rec(self):
        self.rec_event(self.rec_button, 'press', self.rec_button, 'release')

    async def uart_handler(self):
        print(str(time.ticks_us()) + " [  OK  ] Async SONY MTP UART handler")
        swriter = asyncio.StreamWriter(self.uart, {})
        sreader = asyncio.StreamReader(self.uart)
        while True:
            data = await sreader.read(n=-1)
            print("Cam sent:", data)

            if data == self.HANDSHAKE:
                await asyncio.sleep_ms(8)
                await swriter.awrite(self.HANDSHAKE_ACK)
                tmp = vram.info
                vram.info = 'hint'
                vram.sub_hint = 'SONY_MTP_ACK'
                vram.oled_need_update = "yes"
                await asyncio.sleep_ms(2000)
                vram.info = tmp
                vram.oled_need_update = "yes"

            elif data == self.REC_START:
                await asyncio.sleep_ms(8)
                vram.arm_state = "arm"
                await swriter.awrite(self.REC_START_ACK)
                vram.shutter_state,vram.sub_state = 'home',"RECORDING"
                vram.oled_need_update = 'yes'
                self.transation_time = 0

            elif data == self.REC_STOP:
                await asyncio.sleep_ms(8)
                vram.arm_state = "disarm"
                await swriter.awrite(self.REC_STOP_ACK)
                vram.shutter_state,vram.sub_state = 'home',"HOME"
                vram.oled_need_update = 'yes'
                self.transation_time = 0
