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
from machine import Pin, Timer
import buttons, crsf, vars, oled, sony_multiport
import uasyncio as asyncio
from time import sleep

oled1 = oled.init()

timer0 = Timer(0)
timer0.init(period=5, mode=Timer.PERIODIC, callback=buttons.check)

timer1 = Timer(1)
timer1.init(period=4, mode=Timer.PERIODIC, callback=crsf.send_packet)

camera_uart_handler = sony_multiport.uart_handler()

loop = asyncio.get_event_loop()
loop.create_task(camera_uart_handler)
loop.run_forever()