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

class No_Cam:
    def __init__(self):
        print(str(time.ticks_us()) + " [Create] No camera object")
        self.task_mode = "NO"
        self.transation_time = 0
        print(str(time.ticks_us()) + " [  OK  ] No camera object")

    def rec(self):
        self.transation_time += 5
        if self.transation_time <= 1000:
            pass
        elif self.transation_time == 1000:
            pass
        elif self.transation_time >= 1000:
            self.no_cam()
            print(vram.shutter_state)
            self.transation_time = 0

    def timeout(self):
        self.transation_time = 0


    def no_cam(self):
        if vram.shutter_state == "starting":
            vram.shutter_state = "recording"
            vram.arm_state = "arm"
        elif vram.shutter_state == "stopping":
            vram.shutter_state = "idle"
            vram.arm_state = "disarm"


class Momentary_ground:
    def __init__(self):
        print(str(time.ticks_us()) + " [Create] Momentary ground object")
        self.task_mode = "NO"
        self.pin = target.init_momentary_ground_pin()
        self.transation_time = 0
        print(str(time.ticks_us()) + " [  OK  ] Momentary ground object")

    def rec(self):
        self.transation_time += 5
        if self.transation_time == 100:
            self.momentary_ground(0) # ground
        elif self.transation_time > 100 and self.transation_time < 1000:
            pass
        elif self.transation_time >= 1000:
            self.momentary_ground(1) # OD
            print(vram.shutter_state)
            self.transation_time = 0

    def timeout(self):
        self.transation_time = 0

    def momentary_ground(self,value):
        # 1 High impedance (open drain)
        # 0 Low voltage (tied to ground)
        self.pin.value(value)
        if value == 1:
            if vram.shutter_state == "stopping":
                vram.shutter_state = "idle"
                vram.arm_state = "disarm"
            elif vram.shutter_state == "starting":
                vram.shutter_state = "recording"
                vram.arm_state = "arm"


class Schmitt_3v3:
    def __init__(self):
        print(str(time.ticks_us()) + " [Create] Schmitt 3v3 object")
        self.task_mode = "NO"
        self.pin = target.init_schmitt_3v3_trigger_pin()
        self.transation_time = 0
        print(str(time.ticks_us()) + " [  OK  ] Schmitt 3v3 object")

    def rec(self):
        self.transation_time += 5
        if self.transation_time >= 1000:
            self.transation_time = 0
            toggle_cc_voltage_level()

    def timeout(self):
        self.transation_time = 0

    def toggle_cc_voltage_level(self):
        if vram.shutter_state == "stopping":
            vram.shutter_state = "idle"
            self.pin.value(0)
            vram.arm_state = "disarm"
        elif vram.shutter_state == "starting":
            vram.shutter_state = "recording"
            self.pin.value(1)
            vram.arm_state = "arm"


class Sony_multi:
    def __init__(self):
        print(str(time.ticks_us()) + " [Create] Sony MTP object")
        self.task_mode      = "ASYNC"
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
        self.transation_time = 0
        print(str(time.ticks_us()) + " [  OK  ] Sony MTP object")

    def rec(self):
        self.transation_time += 5
        if self.transation_time == 500:
            self.rec_press()
        elif self.transation_time > 500 and self.transation_time < 1000:
            pass
        elif self.transation_time >= 1000:
            self.rec_release()
            self.transation_time = 0

    def timeout(self):
        self.transation_time = 0

    def rec_press(self):
        self.uart.write(self.REC_PRESS)
        print("shutter send: ", self.REC_PRESS)

    def rec_release(self):
        self.uart.write(self.REC_RELEASE)
        print("shutter send: ", self.REC_RELEASE)

    async def uart_handler(self):
        print("Sony MTP UART handler running")
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
                self.transation_time = 0

            elif data == self.REC_STOP:
                await asyncio.sleep_ms(8)
                vram.arm_state = "disarm"
                await swriter.awrite(self.REC_STOP_ACK)
                vram.shutter_state = "idle"
                self.transation_time = 0


class ZCAM_UART:
    def __init__(self):
        print(str(time.ticks_us()) + " [Create] Zcam UART object")
        self.task_mode = "ASYNC"
        self.ASYNC_MSG_ENABLE = (0xEA02022A01).to_bytes(5, 'big')
        self.ASYNC_MSG_DISABLE = (0xEA02022A00).to_bytes(5, 'big')

        self.START_REC      = (0xEA020105).to_bytes(4, 'big')
        self.START_REC_ACK  = (0xEA02028500).to_bytes(5, 'big')
        self.STOP_REC       = (0xEA020106).to_bytes(4, 'big')
        self.STOP_REC_ACK   = (0xEA02028600).to_bytes(5, 'big')

        print(str(time.ticks_us()) + " [Create] UART2")
        self.uart = target.init_zcam_uart()
        print(str(time.ticks_us()) + " [  OK  ] UART2")
        self.transation_time = 0
        print(str(time.ticks_us()) + " [  OK  ] Zcam UART object")

    async def uart_handler(self):
        import ubinascii
        print("ZCAM UART handler running")
        swriter = asyncio.StreamWriter(self.uart, {})
        sreader = asyncio.StreamReader(self.uart)
        while True:
            data = await sreader.read(n=-1)
            data_hex = ubinascii.hexlify(data)
            print("ZCam sent:", data_hex)

            if data == self.START_REC_ACK:
                print("START_REC_ACK")
                vram.shutter_state = "recording"
                vram.arm_state = "arm"
                self.transation_time = 0
            elif data == self.STOP_REC_ACK:
                print("STOP_REC_ACK")
                vram.shutter_state = "idle"
                vram.arm_state = "disarm"
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
        # print("FS send: ", self.ASYNC_MSG_ENABLE.from_bytes())

    def rec(self):
        self.transation_time += 5
        if self.transation_time == 500:
            if vram.shutter_state == "starting":
                self.uart.write(self.START_REC)
                print("shutter send: ", self.START_REC)
            elif vram.shutter_state == "stopping":
                self.uart.write(self.STOP_REC)
                print("shutter send: ", self.STOP_REC)
        elif self.transation_time > 500:
            pass

    def timeout(self):
        self.transation_time = 0


class LANC:
    def __init__(self):
        print(str(time.ticks_us()) + " [Create] LANC object")
        self.task_mode = "THREAD"
        from machine import Pin
        self.test = target.init_lanc_test_pin()
        self.tx = target.init_uart2_tx()
        self.detect = target.init_lanc_detect_pin()
        self.detect.irq(trigger=Pin.IRQ_FALLING, handler=self.lanc_falling)
        self.falling_flag = False
        self.falling_time = time.ticks_us()

        self.byte_flag = "BYTE0"
        self.rec_trigger = False
        self.rec_trigger_state = False
        self.rec_repeat = 0

        self.transation_time = 0
        print(str(time.ticks_us()) + " [  OK  ] LANC object")

    def lanc_falling(self, pin):
        self.tx.value(0)
        self.falling_flag = True

    def uart_handler(self):
        print("LANC UART handler running")
        while True:
            if self.falling_flag == True:
                if self.rec_trigger == True:
                    # handle LANC falling events
                    duaration = time.ticks_us() - self.falling_time # calc duaration between two falling events
                    self.falling_time = time.ticks_us()             # update falling timestamp
                    if self.byte_flag == "BYTE1":
                        self.byte_flag = "BYTE0"# next falling event: send byte 0
                        time.sleep_us(240)
                        self.tx.value(1)
                        time.sleep_us(207)
                        self.tx.value(0)
                        time.sleep_us(208)
                        self.tx.value(1)
                        self.rec_repeat -= 1
                        if self.rec_repeat <=0:
                            self.rec_trigger = False
                            self.rec_repeat = 0
                            self.rec_trigger_state = True
                    elif self.byte_flag == "BYTE0" and duaration > 7000:
                        self.byte_flag = "BYTE1"# next falling event: send byte 1
                        self.tx.value(1)
                        time.sleep_us(314)
                        self.tx.value(0)
                        time.sleep_us(208)
                        self.tx.value(1)
                    else: # elif duaration <= 7000:# LANC is sending other bytes, ignore them
                        self.tx.value(1)
                    self.falling_flag = False   # clear falling flag
                else:
                    self.tx.value(1)                    
                    self.falling_flag = False   # clear falling flag

    def rec(self):
        self.transation_time += 5
        if self.transation_time == 800:
            self.rec_trigger = True  # trigger rec
            self.byte_flag = "BYTE0"
            self.test.value(0)
            self.rec_repeat = 7     # repeat 7 times
            # note that sometimes the first three frames might corrupted,
            # so we repeat for 7 times to make sure the camera recieves at least 4 valid frames
        elif self.transation_time > 800:
            if self.rec_trigger_state == True:
                self.test.value(1)
                self.transation_time = 0
                self.rec_trigger_state = False
                if vram.shutter_state == "stopping":
                    vram.arm_state = "disarm"
                    vram.shutter_state = "idle"
                elif vram.shutter_state == "starting":
                    vram.arm_state = "arm"
                    vram.shutter_state = "recording"

    def timeout(self):
        self.transation_time = 0
