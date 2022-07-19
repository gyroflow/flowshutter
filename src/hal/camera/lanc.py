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
import target
import time

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
        # self.tx.value(0)
        self.falling_flag = True

    def uart_handler(self):
        print("LANC UART handler running")
        while True:
            if self.falling_flag == True:
                # self.tx.value(1)
                if self.rec_trigger == True:
                    # handle LANC falling events
                    duaration = time.ticks_us() - self.falling_time # calc duaration between two falling events
                    self.falling_time = time.ticks_us()             # update falling timestamp
                    if self.byte_flag == "BYTE1":
                        self.tx.value(0)
                        time.sleep_us(208)
                        self.tx.value(1)
                        time.sleep_us(208)
                        self.tx.value(0)
                        time.sleep_us(208)
                        self.tx.value(1)
                        self.byte_flag = "BYTE0"# next falling event: send byte 0
                        self.rec_repeat -= 1
                        if self.rec_repeat <=0:
                            self.rec_trigger = False
                            self.rec_repeat = 0
                            self.rec_trigger_state = True
                    elif self.byte_flag == "BYTE0" and duaration > 7000:
                        time.sleep_us(302)
                        self.tx.value(0)
                        time.sleep_us(208)
                        self.tx.value(1)
                        self.byte_flag = "BYTE1"# next falling event: send bytes 1
                    else: # elif duaration <= 7000:# LANC is sending other bytes, ignore them
                        self.tx.value(1)
                    self.falling_flag = False   # clear falling flag
                else:
                    self.tx.value(1)                    
                    self.falling_flag = False   # clear falling flag

    def rec(self):
        self.transation_time += 5
        if self.transation_time == 50:
            self.rec_trigger = True  # trigger rec
            self.byte_flag = "BYTE0"
            self.test.value(0)
            self.rec_repeat = 6     # repeat 12 times
            # note that sometimes the first three frames might corrupted,
            # so we repeat for 7 times to make sure the camera recieves at least 4 valid frames
        elif self.transation_time > 50:
            if self.rec_trigger_state == True:
                self.test.value(1)
                self.transation_time = 0
                self.rec_trigger_state = False
                if self.state == True:
                    self.state = False
                    self.oled_update_flag = True
                elif self.state == False:
                    self.state = True
                    self.oled_update_flag = True

    def timeout(self):
        self.transation_time = 0