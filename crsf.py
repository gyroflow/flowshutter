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

# two private variables
packets_count = 0   # control the injection frequency
marker = "L"        # control the injection logic high/low

def _toggle_marker_():# toggle the marker
    global marker
    if marker == "L":
        marker = "H"
    else:
        marker = "L"

def _init_():
    disarm_packet = crsf_gen.build_rc_packet(   992,992,189,992,189,992,992,992,
                                                992,992,992,992,992,992,992,992)
    arm_packet = crsf_gen.build_rc_packet(      992,992,189,992,1800,992,992,992,
                                                992,992,992,992,992,992,992,992)
    marker_packet = crsf_gen.build_rc_packet(   992,992,1800,992,1800,992,992,992,
                                                992,992,992,992,992,992,992,992)

    uart1 = target.init_crsf_uart()
    return disarm_packet, arm_packet, marker_packet, uart1

fc_disarm_packet, fc_arm_packet, fc_marker_packet, uart1 = _init_()
audio_pin = target.init_audio()

def _inject_():
    global marker
    if marker == "L":
        uart1.write(fc_arm_packet)  # low throttle
        audio_pin.value(0)          # low voltage on audio
    elif marker == "H":
        uart1.write(fc_marker_packet)# high throttle
        audio_pin.value(1)          # high voltage on audio

def send_packet(t):
    global packets_count
    global marker

    if (vars.arm_state == "arm") & (vars.inject_mode == "OFF"):
        uart1.write(fc_arm_packet)  # just ARM the FC 

    elif (vars.arm_state == "arm") & (vars.inject_mode == "ON"):
        vars.arm_time = vars.arm_time + 5   # 5ms per call

        if vars.arm_time < 1000:            # in first second we don't inject
            uart1.write(fc_arm_packet)
        elif vars.arm_time >= 1000:         # after that we start to inject
            _inject_()
            packets_count = packets_count + 1
            if packets_count >= 8:
                _toggle_marker_()
                packets_count = 0

    elif vars.arm_state == "disarm":
        vars.arm_time = 0
        uart1.write(fc_disarm_packet)
        packets_count = 0
        marker = "L"
