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
import crsf_gen,target, vars
def init():
    disarm_packet = crsf_gen.build_rc_packet(   992,992,189,992,189,992,992,992,
                                                992,992,992,992,992,992,992,992)
    arm_packet = crsf_gen.build_rc_packet(      992,992,189,992,1800,992,992,992,
                                                992,992,992,992,992,992,992,992)

    uart1 = target.init_crsf_uart()
    return disarm_packet, arm_packet, uart1

fc_disarm_packet, fc_arm_packet, uart1 = init()
# audio_pin = target.init_audio()

# def _toggle_():
#     if audio_pin.value() == 1:
#         audio_pin.value(0)
#     else:
#         audio_pin.value(1)

def send_packet(t):
    if vars.arm_state == "arm":
        uart1.write(fc_arm_packet)
        # vars.arm_time = vars.arm_time + 4   # 4ms per call
        # if vars.arm_time >= 1000:           # 4s after arming
        #     if vars.inject_mode == "ON":
        #         _toggle_()
    elif vars.arm_state == "disarm":
        # vars.arm_time = 0
        uart1.write(fc_disarm_packet)