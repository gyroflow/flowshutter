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
def _init_():
    REC_PRESS = b'#7100*'     # record button pressed
    REC_RELEASE = b'#7110*'     # record button released

    HANDSHAKE = b'%000*'
    HANDSHAKE_ACK = b'&00080*'

    REC_START = b'%7610*'
    REC_START_ACK = b'&76100*'

    REC_STOP  = b'%7600*'
    REC_STOP_ACK = b'&76000*'

    return REC_PRESS, REC_RELEASE, HANDSHAKE, HANDSHAKE_ACK, REC_START, REC_START_ACK, REC_STOP, REC_STOP_ACK

REC_PRESS, REC_RELEASE, HANDSHAKE, HANDSHAKE_ACK, REC_START, REC_START_ACK, REC_STOP, REC_STOP_ACK = _init_()

uart2 = target.init_uart2()

async def uart_handler():
    swriter = asyncio.StreamWriter(uart2, {})
    sreader = asyncio.StreamReader(uart2)
    while True:
        res = await sreader.read(n=-1)
        print('Cam sent:', res)

        if res == HANDSHAKE:                    # receive handshake
            await asyncio.sleep_ms(10)
            await swriter.awrite(HANDSHAKE_ACK) # send handshake ack to camera
            tmp = vars.info
            vars.info = "sony mtp ack"
            vars.oled_need_update = "yes"
            await asyncio.sleep_ms(2000)
            vars.info = tmp
            vars.oled_need_update = "yes"

        elif res == REC_START:                  # receive record start
            await asyncio.sleep_ms(9)# I don't know if this timing is good, should look into it later
            vars.arm_state = "arm"              # Arm the FC
            vars.shutter_state = "recording"    # now in recording state
            await swriter.awrite(REC_START_ACK) # send record start ack to camera

        elif res == REC_STOP:                   # receive record stop
            await asyncio.sleep_ms(8)
            vars.arm_state = "disarm"           # disarm the FC
            vars.shutter_state = "idle"         # now in idle state
            await swriter.awrite(REC_STOP_ACK)  # send record stop ack to camera
