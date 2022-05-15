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
import machine as machine
machine.freq(240000000)

import task, settings
settings.read()
task = task.Task()

from machine import Timer
timer0 = Timer(0) # 200Hz CRSF sender
timer0.init(period=5, mode=Timer.PERIODIC, callback=task.schedular)

import vram
if vram.camera_protocol == "Sony MTP":
    import camera
    import uasyncio as asyncio
    camera_uart_handler = camera.Sony_multi().uart_handler()
    loop = asyncio.get_event_loop()
    loop.create_task(camera_uart_handler)
    loop.run_forever()