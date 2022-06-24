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
import target, vram
import time
import uasyncio as asyncio

class Battery:
    def __init__(self):
        print(str(time.ticks_us()) + " [Create] Battery object")
        print(str(time.ticks_us()) + " [Create] ADC")
        self.adc1, self.adc2 = target.init_adc()
        print(str(time.ticks_us()) + " [  OK  ] ADC")
        print(str(time.ticks_us()) + " [  OK  ] Battery object")

    async def adc_handler(self):
        print(str(time.ticks_us()) + " [  OK  ] ADC listener running")
        while True:
            if self.adc1.read() != 0:
                vram.vol = (vram.vol + self.adc1.read() * 3.3 / 2048)/2
            else:
                vram.vol = (vram.vol + self.adc2.read() * 3.3 / 4096)/2
            await asyncio.sleep_ms(50)

class Buttons:
    def __init__(self):
        print(str(time.ticks_us()) + " [Create] Buttons object")
        print(str(time.ticks_us()) + " [Create] buttons")
        self.pgup, self.pgdn, self.enter = target.init_buttons()
        self.state = ["RLS", "RLS", "RLS"]
        # 0 pageup, 1 pagedown, 2 enter
        print(str(time.ticks_us()) + " [  OK  ] buttons")
        print(str(time.ticks_us()) + " [  OK  ] Buttons object")

    async def checker(self, name):
        print(str(time.ticks_us()) + " [  OK  ] "+ name +" checker running")
        if name == 'PAGE UP':
            index, button = 0, self.pgup
        elif name == 'PAGE DOWN':
            index, button = 1, self.pgdn
        elif name == 'ENTER':
            index, button = 2, self.enter
        start,end,dura,flag = 0,0,0,"rls"
        while True:
            if button.value() == 0 and flag == "rls":
                start = time.ticks_ms()
                await asyncio.sleep_ms(30)
                # block value reading for 30ms
                flag = "prs"
            if button.value() == 1 and flag == "prs":
                end = time.ticks_ms()
                await asyncio.sleep_ms(30)
                # block value reading for 30ms
                dura = end - start
                if dura < 100:
                    pass
                elif dura >=100 and dura < 500:
                    # print(name+"short")
                    self.state[index] = "SHORT"
                    flag = "rls"
                elif dura >= 500:
                    # print(name+"long")
                    self.state[index] = "LONG"
                    flag = "rls"
            await asyncio.sleep_ms(0)
