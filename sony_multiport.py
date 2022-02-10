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
import vars,target,oled
def init_multiport_packet():
    rcd_prs = b'#7100*'     # record button pressed
    rcd_rls = b'#7110*'     # record button released

    cm_hdsk = b'%000*'
    cm_hdsk_ack = b'&00080*'

    cm_rcd_start = b'%7610*'
    cm_rcd_start_ack = b'&76100*'

    cm_rcd_stop  = b'%7600*'
    cm_rcd_stop_ack = b'&76000*'

    return rcd_prs, rcd_rls, cm_hdsk, cm_hdsk_ack, cm_rcd_start, cm_rcd_start_ack, cm_rcd_stop, cm_rcd_stop_ack

async def uart_handler():
    rcd_prs, rcd_rls, cm_hdsk, cm_hdsk_ack, cm_rcd_start, cm_rcd_start_ack, cm_rcd_stop, cm_rcd_stop_ack = init_multiport_packet()
    uart2 = target.init_uart2()
    oled1 = oled.init()
    swriter = asyncio.StreamWriter(uart2, {})
    sreader = asyncio.StreamReader(uart2)
    while True:
        res = await sreader.read(n=-1)
        print('Cam sent:', res)

        if res == cm_hdsk:                          # receive handshake
            await asyncio.sleep_ms(10)
            await swriter.awrite(cm_hdsk_ack)       # send handshake ack to camera

        elif res == cm_rcd_start:                   # receive record start
            await asyncio.sleep_ms(9)# I don't know if this timing is good, should look into it later
            vars.arm_state = "arm"                  # Arm the FC
            vars.shutter_state = "recording"        # now in recording state
            await swriter.awrite(cm_rcd_start_ack)  # send record start ack to camera
            oled.show_arm_info(oled1)

        elif res == cm_rcd_stop:                    # receive record stop
            await asyncio.sleep_ms(8)
            vars.arm_state = "disarm"               # disarm the FC
            vars.shutter_state = "stopping"         # now in stopping state
            await swriter.awrite(cm_rcd_stop_ack)   # send record stop ack to camera
            oled.show_disarm_info(oled1)

            await asyncio.sleep_ms(3000)
            vars.shutter_state = "idle"             # back to idle state
            oled.show_idle_info(oled1)              # and show idle info
