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
from micropython import const
import framebuf
import vram
import time

SET_CONTRAST        = const(0x81)
SET_ENTIRE_ON       = const(0xA4)
SET_NORM_INV        = const(0xA6)
SET_DISP            = const(0xAE)
SET_MEM_ADDR        = const(0x20)
SET_COL_ADDR        = const(0x21)
SET_PAGE_ADDR       = const(0x22)
SET_DISP_START_LINE = const(0x40)
SET_SEG_REMAP       = const(0xA0)
SET_MUX_RATIO       = const(0xA8)
SET_IREF_SELECT     = const(0xAD)
SET_COM_OUT_DIR     = const(0xC0)
SET_DISP_OFFSET     = const(0xD3)
SET_COM_PIN_CFG     = const(0xDA)
SET_DISP_CLK_DIV    = const(0xD5)
SET_PRECHARGE       = const(0xD9)
SET_VCOM_DESEL      = const(0xDB)
SET_CHARGE_PUMP     = const(0x8D)

class SSD1306_I2C:
    def __init__(self, width, height, i2c, reflash, addr=0x3c, external_vcc=False):
        print(str(time.ticks_us()) + " [Create] SSD1306_I2C object")
        self.width = width
        self.height = height
        self.i2c = i2c
        self.reflash = reflash
        self.addr = addr
        self.external_vcc = external_vcc
        self.pages = self.height // 8
        self.buffer = bytearray(self.pages * self.width)
        self.framebuf = framebuf.FrameBuffer(self.buffer, self.width, self.height, framebuf.MONO_VLSB)
        self.temp = bytearray(2)
        self.write_list = [b"\x40", None]  # Co=0, D/C#=1
        self.poweron()
        self.init_display()
        print(str(time.ticks_us()) + " [  OK  ] SSD1306_I2C object")
    def init_display(self):
        for cmd in (
            SET_DISP, # off
            # address setting
            SET_MEM_ADDR, 0x00, # horizontal
            # resolution and layout
            SET_DISP_START_LINE,
            SET_SEG_REMAP | 0x01, # column addr 127 mapped to SEG0
            SET_MUX_RATIO, self.height - 1,
            SET_COM_OUT_DIR | 0x08, # scan from COM[N] to COM0
            SET_DISP_OFFSET, 0x00,
            SET_COM_PIN_CFG, 0x02 if self.height == 32 else 0x12,
            # timing and driving scheme
            SET_DISP_CLK_DIV, 0x80,
            SET_PRECHARGE, 0x22 if self.external_vcc else 0xf1,
            SET_VCOM_DESEL, 0x30, # 0.83*Vcc
            # display
            SET_CONTRAST, 0xff,
            SET_ENTIRE_ON,
            SET_NORM_INV,
            SET_IREF_SELECT, 0x30, # enable internal IREF during display on
            # charge pump
            SET_CHARGE_PUMP, 0x10 if self.external_vcc else 0x14,
            SET_DISP | 0x01, # display on
        ):
            self.write_cmd(cmd)
        if self.reflash == True:
            self.fill(0)
            for i in range(self.pages):
                self.show_sub(i)
        else:
            pass

    def show(self):
        for i in range(int(self.pages)):
            vram.oled_tasklist.append(i)

    def show_sub(self,i):
        x0 = 0
        x1 = self.width - 1
        if self.width == 64:
            # displays with width of 64 pixels are shifted by 32
            x0 += 32
            x1 += 32
        self.write_cmd(SET_COL_ADDR)
        self.write_cmd(x0)
        self.write_cmd(x1)
        self.write_cmd(SET_PAGE_ADDR)
        self.write_cmd(i)
        self.write_cmd(i)
        self.write_data(self.buffer[int(i*self.width):int((i+1)*(self.width))])
   
    def show_all(self):
        x0 = 0
        x1 = self.width - 1
        if self.width == 64:
            # displays with width of 64 pixels are shifted by 32
            x0 += 32
            x1 += 32
        self.write_cmd(SET_COL_ADDR)
        self.write_cmd(x0)
        self.write_cmd(x1)
        self.write_cmd(SET_PAGE_ADDR)
        self.write_cmd(0)
        self.write_cmd(self.pages - 1)
        self.write_data(self.buffer)

    def write_cmd(self, cmd):
        self.temp[0] = 0x80 # Co=1, D/C#=0
        self.temp[1] = cmd
        self.i2c.writeto(self.addr, self.temp)
    def write_data(self, buf):
        self.write_list[1] = buf
        self.i2c.writevto(self.addr, self.write_list)

    def poweroff(self):
        self.write_cmd(SET_DISP)
    def poweron(self):
        self.write_cmd(SET_DISP | 0x01)
    def contrast(self, contrast):
        self.write_cmd(SET_CONTRAST)
        self.write_cmd(contrast)
    def invert(self, invert):
        self.write_cmd(SET_NORM_INV | (invert & 1))
    def rotate(self, rotate):
        self.write_cmd(SET_COM_OUT_DIR | ((rotate & 1) << 3))
        self.write_cmd(SET_SEG_REMAP | (rotate & 1))

    def fill(self, col):
        self.framebuf.fill(col)
    def pixel(self, x, y, col):
        self.framebuf.pixel(x, y, col)
    def scroll(self, dx, dy):
        self.framebuf.scroll(dx, dy)
    def text(self, string, x, y, col=1):
        self.framebuf.text(string, x, y, col)
    def hline(self, x, y, w, col):
        self.framebuf.hline(x, y, w, col)
    def vline(self, x, y, h, col):
        self.framebuf.vline(x, y, h, col)
    def line(self, x1, y1, x2, y2, col):
        self.framebuf.line(x1, y1, x2, y2, col)
    def rect(self, x, y, w, h, col):
        self.framebuf.rect(x, y, w, h, col)
    def fill_rect(self, x, y, w, h, col):
        self.framebuf.fill_rect(x, y, w, h, col)
    def blit(self, fbuf, x, y):
        self.framebuf.blit(fbuf, x, y)
