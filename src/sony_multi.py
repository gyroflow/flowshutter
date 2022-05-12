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
import vars,target

class Sony_multi:
    def __init__(self):
        self.REC_PRESS = b'#7100*'      # record button pressed
        self.REC_RELEASE = b'#7110*'    # record button released

        self.HANDSHAKE = b'%000*'
        self.HANDSHAKE_ACK = b'&00080*'

        self.REC_START = b'%7610*'
        self.REC_START_ACK = b'&76100*'

        self.REC_STOP  = b'%7600*'
        self.REC_STOP_ACK = b'&76000*'

        self.uart = target.init_uart2()
    
    def rec_press(self):
        self.uart.write(self.REC_PRESS)
        print("shutter send: ", self.REC_PRESS)

    def rec_release(self):
        self.uart.write(self.REC_RELEASE)
        print("shutter send: ", self.REC_RELEASE)

    async def uart_handler(self):
        swriter = asyncio.StreamWriter(self.uart, {})
        sreader = asyncio.StreamReader(self.uart)
        while True:
            data = await sreader.read(n=-1)
            print("Cam sent:", data)

            if data == self.HANDSHAKE:
                await asyncio.sleep_ms(8)
                await swriter.awrite(self.HANDSHAKE_ACK)
                tmp = vars.info
                vars.info = "sony mtp ack"
                vars.oled_need_update = "yes"
                await asyncio.sleep_ms(2000)
                vars.info = tmp
                vars.oled_need_update = "yes"

            elif data == self.REC_START:
                await asyncio.sleep_ms(8)
                vars.arm_state = "arm"
                await swriter.awrite(self.REC_START_ACK)
                vars.shutter_state = "recording"

            elif data == self.REC_STOP:
                await asyncio.sleep_ms(8)
                vars.arm_state = "disarm"
                await swriter.awrite(self.REC_STOP_ACK)
                vars.shutter_state = "idle"
