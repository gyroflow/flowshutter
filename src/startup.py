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
import os, json
import time
print(str(time.ticks_us()) + " [ Boot ] Start")

from machine import Pin, SoftI2C
import framebuf, ssd1306
i2c = SoftI2C(scl=Pin(22), sda=Pin(21),freq = 800000)
screen = ssd1306.SSD1306_I2C(128, 32, i2c, True)
gyroflow_bytearray = bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\xc0\x00\x00\x00\x00\xf0\x00\xc0\x00\x00\x00\x00\x00\x00\x00\x03@\x00\x00\x00\x01\x98\x01\xc0\x00\x00\x00\x00\x00\x00\x00\x06@\x00\x00\x00\x01\x0c\x01\xe0\x00\x00\x00\x00\x00\x00\x00\x0cA\x80\x00\x00\x03\x06\x03p\x00\x00\x00\x00\x00\x00\x00\x18\xc3\x00\x00\x00\x02\x02G0\x00\x00\x00\x00\x00\x00\x001\x87\x00\x00\x00\x1a\x01\xe68\x00\x00\x00\x00\x00\x00\x00!\x0e\x00\x00\x00r\xc3\xee\x18\x00\x00\x00\x00\x00\x00\x00c\x0c\x00\x00\x00\xc2O|\x1c\x00\x00\x00\x00\x00\x00\x00B\x18\x00\x00\x00\x83<8\x0c\x0f\xe3\x03?\xe0|\x00\xc4\x10\x00\x00\x00\x818\x18\x0e\x1f\xf3\x87?\xf0\xfe\x00\x8c0\x00\x00\x01\xc1\x80\x18\xfe89\xce01\x83\x01\x98`\x00\x00\x01d\x80\x0f\x800\x18\xcc03\x01\x81\xb0\xc0\xff\x80\x016\x80\x0e\x00p\x00x03\x01\x81a\xc1\xe1\x82\x03X\x80\x06\x00p\x00x?\xe3\x01\x83\xc3\x83!\x06\x02l\x00\x07\x00p\xf80?\xc3\x01\x83\xce\x87#\x0e\x06w\x80\x1e\x80p\xf800\xc3\x01\x87\xf8\x86"\x1c\x0c1\xc0x\xc0p\x1800\xe3\x01\x87\x81\x86b4\x188p\xe0@8800q\x83\x0c\x81\x0c\xc3\xe4p\x18>\x00@<x008\xfe\x1c\x81\xbf\x81\x86\xc0\x0c\x07\x90\xc0\x1f\xf000\x18|<\x80\xe2\x00\x03\x80\x0c0\xff\x80\x07\xc0\x00\x00\x00\x00h\x80\x00\x00\x00\x00\x060\x04\x00\x00\x00\x00\x00\x00\x00\x08\x80\x00\x00\x00\x00\x06\x98\x10\x00\x00\x00\x00\x00\x00\x00\x19\x80\x00\x00\x00\x00\x03\x8c\x10\x00\x00\x00\x00\x00\x00\x00\x11\x00\x00\x00\x00\x00\x01\x060\x00\x00\x00\x00\x00\x00\x00\x13\x00\x00\x00\x00\x00\x00\x03`\x00\x00\x00\x00\x00\x00\x00\x1e\x00\x00\x00\x00\x00\x00\x01\xc0\x00\x00\x00\x00\x00\x00\x00\x0c\x00\x00\x00\x00\x00')
gyroflow_fb = framebuf.FrameBuffer(gyroflow_bytearray, 128,28, framebuf.MONO_HLSB)
screen.blit(gyroflow_fb, 0, 2)
screen.show_all()

def update_files():
    new_f_flag = False
    del_f_flag = False

    try:
        with open("delete_list.json", "r") as f:
            delete_list = json.load(f)
            f.close()
            print("there are some outdated files")
            for i in range(0,len(delete_list['files'])):
                os.remove(str(delete_list['files'][i]['name']))
                print(str(delete_list['files'][i]['name']) + " deleted")
            os.remove("delete_list.json")
            print("delete_list.json removed")
            del_f_flag = True
    except:
        print("no outdate file")
        pass


    try: # update new files
        with open("update_list.json", "r") as f:
            update_list = json.load(f)
            f.close()
            print("there are new files")
            for i in range(0,len(update_list['files'])):
                os.rename("tmp/"+str(update_list['files'][i]['name']), str(update_list['files'][i]['name']))
                print(str(update_list['files'][i]['name']) + " updated")
            os.remove("update_list.json")
            print("update_list.json removed")
            os.rmdir("tmp")
            print("tmp dir removed")
            new_f_flag = True
    except:
        print("no new file")
        pass


    if new_f_flag == True or del_f_flag == True:
        print("hey we supposed to remove the project.pymakr and old sha.json")

        os.remove("sha.json")
        os.rename("tmp_sha.json","sha.json")
        print("sha.json updated")
        try:
            os.remove("project.pymakr")
        except:
            print("Already removed")

    print(str(time.ticks_us()) + " [ Boot ] Delete flag: " + str(del_f_flag))
    print(str(time.ticks_us()) + " [ Boot ] Update flag: " + str(new_f_flag))


update_files()
try:
    print(os.listdir())
except:
    pass
print(str(time.ticks_us()) + " [ Boot ] Pass")