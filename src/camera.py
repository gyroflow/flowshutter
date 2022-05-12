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

class Sony_multi:
    def __init__(self):
        print(str(time.time_ns()) + " [Create] Sony MTP object")
        self.REC_PRESS = b'#7100*'      # record button pressed
        self.REC_RELEASE = b'#7110*'    # record button released

        self.HANDSHAKE = b'%000*'
        self.HANDSHAKE_ACK = b'&00080*'

        self.REC_START = b'%7610*'
        self.REC_START_ACK = b'&76100*'

        self.REC_STOP  = b'%7600*'
        self.REC_STOP_ACK = b'&76000*'

        print(str(time.time_ns()) + " [Create] UART2")
        self.uart = target.init_uart2()
        print(str(time.time_ns()) + " [  OK  ] UART2")
        print(str(time.time_ns()) + " [Create] Sony MTP object")
    
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
                tmp = vram.info
                vram.info = "sony mtp ack"
                vram.oled_need_update = "yes"
                await asyncio.sleep_ms(2000)
                vram.info = tmp
                vram.oled_need_update = "yes"

            elif data == self.REC_START:
                await asyncio.sleep_ms(8)
                vram.arm_state = "arm"
                await swriter.awrite(self.REC_START_ACK)
                vram.shutter_state = "recording"

            elif data == self.REC_STOP:
                await asyncio.sleep_ms(8)
                vram.arm_state = "disarm"
                await swriter.awrite(self.REC_STOP_ACK)
                vram.shutter_state = "idle"


class Momentary_ground:
    def __init__(self):
        self.pin = target.init_momentary_ground_pin()
    
    def momentary_ground(self,value):
        # 1 High impedance (open drain)
        # 0 Low voltage (tied to ground)    
        self.pin.value(value)


class Schmitt_3v3:
    def __init__(self):
        self.pin = target.init_schmitt_3v3_trigger_pin()
    
    def toggle_cc_voltage_level(self):
        if vram.shutter_state == "recording":
            self.pin.value(1)
            print("high voltarge level")
        else:
            self.pin.value(0)
            print("low voltage level")
