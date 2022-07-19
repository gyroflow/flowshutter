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
import target
import time
from hal.camera.common import Camera

class ZCAM_UART(Camera):
    def __init__(self):
        print(str(time.ticks_us()) + " [Create] Zcam UART object")
        self.ASYNC_MSG_ENABLE = (0xEA02022A01).to_bytes(5, 'big')
        self.ASYNC_MSG_DISABLE= (0xEA02022A00).to_bytes(5, 'big')

        self.START_REC      = (0xEA020105).to_bytes(4, 'big')
        self.START_REC_ACK  = (0xEA02028500).to_bytes(5, 'big')
        self.STOP_REC       = (0xEA020106).to_bytes(4, 'big')
        self.STOP_REC_ACK   = (0xEA02028600).to_bytes(5, 'big')

        print(str(time.ticks_us()) + " [Create] UART2")
        self.uart = target.init_zcam_uart()
        print(str(time.ticks_us()) + " [  OK  ] UART2")
        super().__init__("ASYNC")
        print(str(time.ticks_us()) + " [  OK  ] Zcam UART object")

    async def uart_handler(self):
        import ubinascii
        print(str(time.ticks_us()) + " [  OK  ] Async ZCAM UART handler")
        swriter = asyncio.StreamWriter(self.uart, {})
        sreader = asyncio.StreamReader(self.uart)
        while True:
            data = await sreader.read(n=-1)
            data_hex = ubinascii.hexlify(data)
            print("ZCam sent:", data_hex)

            if data == self.START_REC_ACK:
                print("START_REC_ACK")
                self.state = True
                self.arm_flag = True
                self.oled_update_flag = True
                self.transation_time = 0
            elif data == self.STOP_REC_ACK:
                print("STOP_REC_ACK")
                self.state = False
                self.arm_flag = False
                self.oled_update_flag = True
                self.transation_time = 0
            elif data == (0xEA02112900000001000000090000000900000000).to_bytes(20, 'big'):
                print("REC MSG")
            else:
                _type = data[4:8]
                if _type    == (0x00_00_00_00).to_bytes(4, 'big'):
                    print("type:", "EVENT")
                elif _type  == (0x00_00_00_01).to_bytes(4, 'big'):
                    print("type:", "MSG")
                else:
                    print("type:", ubinascii.hexlify(_type))

                what = data[8:12]
                print("what:", ubinascii.hexlify(what))

                ext1 = data[12:16]
                print("ext1:", ubinascii.hexlify(ext1))

                ext2 = data[16:20]
                print("ext2:", ubinascii.hexlify(ext2))

    def set_mode(self):
        self.uart.write(self.ASYNC_MSG_ENABLE)
        # self.uart.write(self.ASYNC_MSG_DISABLE)

    def toggle_rec(self, argv):
        if argv == "pass":
            pass
        elif self.state == False:
            self.uart.write(self.START_REC)
        elif self.state == True:
            self.uart.write(self.STOP_REC)

    def rec(self):
        self.rec_event(self.toggle_rec, "pass", self.toggle_rec, "react")