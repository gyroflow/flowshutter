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

class CRSF:
    def __init__(self):
        print(str(time.ticks_us()) + " [Create] CRSF object")
        self.arm_time       = 0
        self.packets_count  = 0     # number of packets sent 
        self.marker         = 'L'   # marker
        print(str(time.ticks_us()) + " [Create] UART1")
        self.uart           = target.init_crsf_uart()
        print(str(time.ticks_us()) + " [  OK  ] UART1")

        print(str(time.ticks_us()) + " [Create] AJ pin")
        self.audio          = target.init_audio()
        print(str(time.ticks_us()) + " [  OK  ] AJ pin")
        print(str(time.ticks_us()) + " [Create] CRSF Generator")
        self.crsf_gen = CRSF_Generator()
        print(str(time.ticks_us()) + " [  OK  ] CRSF Generator")
        self.disarm_packet  = self.crsf_gen.build_rc_packet(992,992,189,992,189,992,992,992,
                                                            992,992,992,992,992,992,992,992)
        self.arm_packet     = self.crsf_gen.build_rc_packet(992,992,189,992,1800,992,992,992,
                                                            992,992,992,992,992,992,992,992)
        self.marker_packet  = self.crsf_gen.build_rc_packet(992,992,1800,992,1800,992,992,992,
                                                            992,992,992,992,992,992,992,992)
        print(str(time.ticks_us()) + " [  OK  ] CRSF object")

    def _toggle_marker_(self):  #toggle the marker
        if self.marker == 'L':
            self.marker = 'H'
        else:
            self.marker = 'L'

    def _inject_(self):
        if self.marker == "L":
            self.uart.write(self.arm_packet)  # low throttle
            self.audio.value(0)          # low voltage on audio
        elif self.marker == "H":
            self.uart.write(self.marker_packet)# high throttle
            self.audio.value(1)          # high voltage on audio

    def send_packet(self, t):
        if (vram.arm_state == "arm") & (vram.inject_mode == "OFF"):
            self.uart.write(self.arm_packet)  # just ARM the FC 

        elif (vram.arm_state == "arm") & (vram.inject_mode == "ON"):
            self.arm_time = self.arm_time + 5   # 5ms per call

            if self.arm_time < 1000:            # in first second we don't inject
                self.uart.write(self.arm_packet)
            elif self.arm_time >= 1000:         # after that we start to inject
                self._inject_()
                self.packets_count = self.packets_count + 1
                if self.packets_count >= 8:
                    self._toggle_marker_()
                    self.packets_count = 0

        elif vram.arm_state == "disarm":
            self.arm_time = 0
            self.uart.write(self.disarm_packet)
            self.packets_count = 0
            self.marker = "L"


class CRSF_Generator:
    def __init__(self):
        print(str(time.ticks_us()) + " [ Init ] CRSF Generator")
        self._crc_tab = [
                0x00,0xD5,0x7F,0xAA,0xFE,0x2B,0x81,0x54,0x29,0xFC,0x56,0x83,0xD7,0x02,0xA8,0x7D,
                0x52,0x87,0x2D,0xF8,0xAC,0x79,0xD3,0x06,0x7B,0xAE,0x04,0xD1,0x85,0x50,0xFA,0x2F,
                0xA4,0x71,0xDB,0x0E,0x5A,0x8F,0x25,0xF0,0x8D,0x58,0xF2,0x27,0x73,0xA6,0x0C,0xD9,
                0xF6,0x23,0x89,0x5C,0x08,0xDD,0x77,0xA2,0xDF,0x0A,0xA0,0x75,0x21,0xF4,0x5E,0x8B,
                0x9D,0x48,0xE2,0x37,0x63,0xB6,0x1C,0xC9,0xB4,0x61,0xCB,0x1E,0x4A,0x9F,0x35,0xE0,
                0xCF,0x1A,0xB0,0x65,0x31,0xE4,0x4E,0x9B,0xE6,0x33,0x99,0x4C,0x18,0xCD,0x67,0xB2,
                0x39,0xEC,0x46,0x93,0xC7,0x12,0xB8,0x6D,0x10,0xC5,0x6F,0xBA,0xEE,0x3B,0x91,0x44,
                0x6B,0xBE,0x14,0xC1,0x95,0x40,0xEA,0x3F,0x42,0x97,0x3D,0xE8,0xBC,0x69,0xC3,0x16,
                0xEF,0x3A,0x90,0x45,0x11,0xC4,0x6E,0xBB,0xC6,0x13,0xB9,0x6C,0x38,0xED,0x47,0x92,
                0xBD,0x68,0xC2,0x17,0x43,0x96,0x3C,0xE9,0x94,0x41,0xEB,0x3E,0x6A,0xBF,0x15,0xC0,
                0x4B,0x9E,0x34,0xE1,0xB5,0x60,0xCA,0x1F,0x62,0xB7,0x1D,0xC8,0x9C,0x49,0xE3,0x36,
                0x19,0xCC,0x66,0xB3,0xE7,0x32,0x98,0x4D,0x30,0xE5,0x4F,0x9A,0xCE,0x1B,0xB1,0x64,
                0x72,0xA7,0x0D,0xD8,0x8C,0x59,0xF3,0x26,0x5B,0x8E,0x24,0xF1,0xA5,0x70,0xDA,0x0F,
                0x20,0xF5,0x5F,0x8A,0xDE,0x0B,0xA1,0x74,0x09,0xDC,0x76,0xA3,0xF7,0x22,0x88,0x5D,
                0xD6,0x03,0xA9,0x7C,0x28,0xFD,0x57,0x82,0xFF,0x2A,0x80,0x55,0x01,0xD4,0x7E,0xAB,
                0x84,0x51,0xFB,0x2E,0x7A,0xAF,0x05,0xD0,0xAD,0x78,0xD2,0x07,0x53,0x86,0x2C,0xF9
            ]
    
    def _build_11bit_(self, n):
        # convert channel value to a list of 11 bit value
        # channel value is 172 to 1811, mid is 992
        b = []
        while True:
            s = n // 2
            y = n % 2
            b = b + [y]
            if s == 0:
                break
            n = s
        bit_need_be_pad = 11 - len(b)
        if bit_need_be_pad > 0:
            b = b + [0] * bit_need_be_pad
        return b

    def _lsb_bit_list_(self, bits):
        # prepare for the LSB format
        bytes_ = []
        for i in range (0,int(len(bits)/8)):
            r_byte = bits[i*8:(i+1)*8]
            r_byte.reverse()
            # print(r_byte)
            bytes_ = bytes_ + r_byte
        return bytes_

    def _bit_list_to_bytes_(self, bit_list):    # convert bit list to bytes

        bit_list_lsb = bit_list[::-1]
        bit_string_list = []
        bitstream = ''

        bit_list_lsb = self._lsb_bit_list_(bit_list)
        bit_string = [str(x) for x in bit_list_lsb]
        bitstream = ''.join(bit_string)

        byte = bytes(int(bitstream[i:i+8], 2) for i in range(0, len(bitstream), 8))

        return byte

    def _build_payload_(self,
        channel_0, channel_1, channel_2, channel_3,
        channel_4, channel_5, channel_6, channel_7,
        channel_8, channel_9, channel_10,channel_11,
        channel_12,channel_13,channel_14,channel_15
        ):
        payload = []
        payload = payload + self._build_11bit_(channel_0)
        payload = payload + self._build_11bit_(channel_1)
        payload = payload + self._build_11bit_(channel_2)
        payload = payload + self._build_11bit_(channel_3)
        payload = payload + self._build_11bit_(channel_4)
        payload = payload + self._build_11bit_(channel_5)
        payload = payload + self._build_11bit_(channel_6)
        payload = payload + self._build_11bit_(channel_7)
        payload = payload + self._build_11bit_(channel_8)
        payload = payload + self._build_11bit_(channel_9)
        payload = payload + self._build_11bit_(channel_10)
        payload = payload + self._build_11bit_(channel_11)
        payload = payload + self._build_11bit_(channel_12)
        payload = payload + self._build_11bit_(channel_13)
        payload = payload + self._build_11bit_(channel_14)
        payload = payload + self._build_11bit_(channel_15)
        payload_bytes = self._bit_list_to_bytes_(payload)
        return payload_bytes

    def _crsf_crc_(self, data: bytes) -> int:
        crc = 0
        crc_tab = self._crc_tab
        for i in data:
            crc = crc_tab[crc ^ i]
        return crc

    def build_rc_packet(self,
        channel_0, channel_1, channel_2, channel_3,
        channel_4, channel_5, channel_6, channel_7,
        channel_8, channel_9, channel_10,channel_11,
        channel_12,channel_13,channel_14,channel_15
        ):
        print(str(time.ticks_us()) + " [ Run  ] CRSF build_rc_packet")
        address_int = 0xC8  # flight controller
        lenth_int = 0x18    # 26
        type_int = 0x16     # RC_CHANNEL_PACKET

        address = address_int.to_bytes(1, 'big')
        length = lenth_int.to_bytes(1, 'big')
        type_ = type_int.to_bytes(1, 'big')

        payload = self._build_payload_(
            channel_0, channel_1, channel_2, channel_3,
            channel_4, channel_5, channel_6, channel_7,
            channel_8, channel_9, channel_10,channel_11,
            channel_12,channel_13,channel_14,channel_15
            )

        crc_int = self._crsf_crc_(type_ + payload)
        crc = crc_int.to_bytes(1, 'big')

        packet = address + length + type_ + payload + crc

        return packet
