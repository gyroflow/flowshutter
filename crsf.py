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
import target, vars
def init():

    # 420000 baud rate
    # 8 bit per byte
    # Big endian
    # 1 stop bit
    # LSB first
    # each frame has a same structure:
    # [device address][length][type][data][crc]

    # for RC => FC, device address should be 0xC8, target device is FC
    # length should be the result of (type+data+crc), which is 0x18
    # type is 0x16
    # so here comes the header:
    header = 0xC81816 # Header for the data
    # then we create two data packets manually:
    # first is throttle low, AUX1 low, else mid:
    l_payload = 0xE0035F2FC0D70BF0810F7CE0031FF8C0073EF0810F7C
    l_crc = 0x9D

    # second is throttle low, AUX1 high, else mid:
    h_payload = 0xE0035F2FC0D765F0810F7CE0031FF8C0073EF0810F7C
    h_crc = 0x72

    header =header.to_bytes(3, 'big')
    l_payload = l_payload.to_bytes(22, 'big')
    l_crc = l_crc.to_bytes(1, 'big')
    h_payload = h_payload.to_bytes(22, 'big')
    h_crc = h_crc.to_bytes(1, 'big')

    fc_disarm_frame = header + l_payload + l_crc
    fc_arm_frame = header + h_payload + h_crc
    uart1 = target.init_crsf_uart()
    return fc_arm_frame, fc_disarm_frame, uart1

fc_arm_packet, fc_disarm_packet, uart1 = init()
def send_packet(t):
    if vars.arm_state == "arm":
        uart1.write(fc_arm_packet)
    elif vars.arm_state == "disarm":
        uart1.write(fc_disarm_packet)