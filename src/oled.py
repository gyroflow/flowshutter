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
import vars, ssd1306, target, wlan
import framebuf

def _init_():
    i2c = target.init_i2c()
    screen = ssd1306.SSD1306_I2C(128, 32, i2c)
    return screen

screen = _init_()

def update(info):
    if info == "welcome":
        _display_welcome_()
    elif info == "idle":
        _display_idle_()
    elif info == "starting":
        _display_starting_()
    elif info == "starting_timeout":
        _show_starting_timeout_()
    elif info == "recording":
        _display_recording_()
    elif info == "stopping":
        _display_stopping_()
    elif info == "battery":
        _display_battery_()
    elif info == "menu_internet":
        _display_menu_internet_()
    elif info == "menu_ota_source":
        _display_menu_ota_source_()
    elif info == "menu_ota_channel":
        _display_menu_ota_channel_()
    elif info == "menu_camera_protocol":
        _display_menu_camera_protocol_()
    elif info == "menu_device_mode":
        _display_menu_device_mode_()
    elif info == "menu_inject_mode":
        _display_menu_inject_mode_()
    elif info == "menu_reboot_hint":
        _display_menu_reboot_hint_()
    elif info == "sony mtp ack":
        _show_sony_mtp_ack_()

    else:
        print("Unknown OLED info: "+ info)

def _draw_gyroflow_logo_():
    gyroflow_bytearray = bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\xc0\x00\x00\x00\x00\xf0\x00\xc0\x00\x00\x00\x00\x00\x00\x00\x03@\x00\x00\x00\x01\x98\x01\xc0\x00\x00\x00\x00\x00\x00\x00\x06@\x00\x00\x00\x01\x0c\x01\xe0\x00\x00\x00\x00\x00\x00\x00\x0cA\x80\x00\x00\x03\x06\x03p\x00\x00\x00\x00\x00\x00\x00\x18\xc3\x00\x00\x00\x02\x02G0\x00\x00\x00\x00\x00\x00\x001\x87\x00\x00\x00\x1a\x01\xe68\x00\x00\x00\x00\x00\x00\x00!\x0e\x00\x00\x00r\xc3\xee\x18\x00\x00\x00\x00\x00\x00\x00c\x0c\x00\x00\x00\xc2O|\x1c\x00\x00\x00\x00\x00\x00\x00B\x18\x00\x00\x00\x83<8\x0c\x0f\xe3\x03?\xe0|\x00\xc4\x10\x00\x00\x00\x818\x18\x0e\x1f\xf3\x87?\xf0\xfe\x00\x8c0\x00\x00\x01\xc1\x80\x18\xfe89\xce01\x83\x01\x98`\x00\x00\x01d\x80\x0f\x800\x18\xcc03\x01\x81\xb0\xc0\xff\x80\x016\x80\x0e\x00p\x00x03\x01\x81a\xc1\xe1\x82\x03X\x80\x06\x00p\x00x?\xe3\x01\x83\xc3\x83!\x06\x02l\x00\x07\x00p\xf80?\xc3\x01\x83\xce\x87#\x0e\x06w\x80\x1e\x80p\xf800\xc3\x01\x87\xf8\x86"\x1c\x0c1\xc0x\xc0p\x1800\xe3\x01\x87\x81\x86b4\x188p\xe0@8800q\x83\x0c\x81\x0c\xc3\xe4p\x18>\x00@<x008\xfe\x1c\x81\xbf\x81\x86\xc0\x0c\x07\x90\xc0\x1f\xf000\x18|<\x80\xe2\x00\x03\x80\x0c0\xff\x80\x07\xc0\x00\x00\x00\x00h\x80\x00\x00\x00\x00\x060\x04\x00\x00\x00\x00\x00\x00\x00\x08\x80\x00\x00\x00\x00\x06\x98\x10\x00\x00\x00\x00\x00\x00\x00\x19\x80\x00\x00\x00\x00\x03\x8c\x10\x00\x00\x00\x00\x00\x00\x00\x11\x00\x00\x00\x00\x00\x01\x060\x00\x00\x00\x00\x00\x00\x00\x13\x00\x00\x00\x00\x00\x00\x03`\x00\x00\x00\x00\x00\x00\x00\x1e\x00\x00\x00\x00\x00\x00\x01\xc0\x00\x00\x00\x00\x00\x00\x00\x0c\x00\x00\x00\x00\x00')
    gyroflow_fb = framebuf.FrameBuffer(gyroflow_bytearray, 128,28, framebuf.MONO_HLSB)
    screen.blit(gyroflow_fb, 0, 2)

def _draw_cam_():
    cam_bytearray = bytearray(b'\x00?\xfc\x00\x00`\x06\x00\x00@\x02\x00\x00@\x1a\x00\x00@\x1a\x00\x00@\x1a\x00\x00@\x02\x00\x00`\x06\x00\x00?\xfc\x00\x18\x0c0\x18<\x04 <f\x0f\xf0f\x7f\xf8\x1f\xfe\xff\xe0\x07\xff\xc0\xc7\xe3\x03\xc1\x9c9\x83\xff1\x8c\xff\xc3`6C\xc2@\x1aK\xc6\xc0\x0bk\xc4\x80\x05#\xc4\x80\x05#\xc4\x80\x01#\xc6\xc0\x03c\xc2@\x02C\xc3`\x06\xc3\xff0\x0c\xff\xc1\x9c9\x83\xc0\xc7\xe3\x03\xff\xe0\x07\xff\x7f\xf8\x1f\xfe\x00\x0f\xf0\x00')
    cam_fb = framebuf.FrameBuffer(cam_bytearray, 32,32, framebuf.MONO_HLSB)
    screen.blit(cam_fb, 0, 0)

def _draw_cam_working_():
    cam_working_bytearray = bytearray(b'\x00?\xfc\x00\x00\x7f\xfe\x00\x00\x7f\xfe\x00\x00\x7f\xe6\x00\x00\x7f\xe6\x00\x00\x7f\xe6\x00\x00\x7f\xfe\x00\x00\x7f\xfe\x00\x00?\xfc\x00\x18\x0c0\x18<\x04 <f\x0f\xf0f\x7f\xf8\x1f\xfe\xff\xe0\x07\xff\xc0\xc7\xe3\x03\xc1\x9f\xf9\x83\xff>|\xff\xc3\x7f\xceC\xc2\x7f\xe6K\xc6\xff\xf7k\xc4\xff\xfb#\xc4\xff\xfb#\xc4\xff\xff#\xc6\xff\xffc\xc2\x7f\xfeC\xc3\x7f\xfe\xc3\xff?\xfc\xff\xc1\x9f\xf9\x83\xc0\xc7\xe3\x03\xff\xe0\x07\xff\x7f\xf8\x1f\xfe\x00\x0f\xf0\x00')
    cam_working_fb = framebuf.FrameBuffer(cam_working_bytearray, 32,32, framebuf.MONO_HLSB)
    screen.blit(cam_working_fb, 0, 0)

def _draw_wifi_disconnected_():
    wifi_disconnected_bytearray = bytearray(b"~\x00\x00\x06\xff\xe0\x00\x0f\xff\xfc\x00\x1f\xff\xff\x00>\xff\xff\xc0|\xff\xff\xf0\xf8?\xff\xf9\xf0\x00\xff\xf3\xe0\x00\x1f\xe7\xc0\x00\x07\xcf\x80\x00\x01\x9f\x00\x7f\x00>@\xff\xc0|\xe0\xff\xf0\xf9\xe0\xff\xf9\xf3\xf0\xff\xf3\xe7\xf0\xff\xe7\xc7\xf8\x7f\xcf\x83\xf8\x03\x9f\x03\xfc\x00>A\xfc\x00|\xc1\xfc\x00\xf9\xe0\xfe\x01\xf3\xe0\xfe\x03\xe7\xf0\xfe'\xc7\xf0~O\x87\xf8\x7f\x9f\x03\xf8\x7f>\x03\xf8\x7f|\x03\xf8\x7f\xf9\x03\xf8\x7f\xf2\x03\xf8?d\x01\xf0>")
    wifi_connected_fb = framebuf.FrameBuffer(wifi_disconnected_bytearray, 32,32, framebuf.MONO_HLSB)
    screen.blit(wifi_connected_fb, 0, 0)

def _draw_wifi_connected_():
    wifi_connected_bytearray = bytearray(b'~\x00\x00\x00\xff\xe0\x00\x00\xff\xfc\x00\x00\xff\xff\x00\x00\xff\xff\xc0\x00\xff\xff\xf0\x00?\xff\xf8\x00\x00\xff\xfc\x00\x00\x1f\xfe\x00\x00\x07\xff\x00\x00\x01\xff\x80\x7f\x00\xff\xc0\xff\xc0\x7f\xe0\xff\xf0?\xe0\xff\xfc\x1f\xf0\xff\xfe\x0f\xf0\xff\xff\x07\xf8\x7f\xff\x83\xf8\x03\xff\x83\xfc\x01\xff\xc1\xfc\x00\x7f\xc1\xfc\x00?\xe0\xfe\x00\x1f\xe0\xfe\x00\x0f\xf0\xfe<\x07\xf0~~\x07\xf8\x7f\xff\x03\xf8\x7f\xff\x03\xf8\x7f\xff\x03\xf8\x7f\xff\x03\xf8\x7f~\x03\xf8?<\x01\xf0>')
    wifi_connected_fb = framebuf.FrameBuffer(wifi_connected_bytearray, 32,32, framebuf.MONO_HLSB)
    screen.blit(wifi_connected_fb, 0, 0)

def _draw_github_logo_():
    github_bytearray = bytearray(b'\x01\xc0\x008\x03\xf0\x00\xfc\x03\xf9\xf9\xfc\x03?\xff\xcc\x03\x0f\x0f\x0c\x03\x8c\x03\x1c\x03\x80\x00\x1c\x03\x80\x00\x1c\x07\x00\x00\x1e\x07\x00\x00\x0e\x0e\x00\x00\x0f\x0e\x00\x00\x07\x0e\x00\x00\x07\x0e\x00\x00\x07\x0e\x00\x00\x07\x0e\x00\x00\x07\x0f\x00\x00\x0e\x0f\x00\x00\x0e\x07\x80\x00\x1e\x03\xc0\x00<\x03\xf0\x00\xf8\xc1\xff\x0f\xf0\xf0\x7f\x0f\xe0\xf8\x0f\x0f\x00|\x0e\x07\x00\x1e\x0e\x07\x00\x0f\x9e\x07\x80\x07\xfe\x07\x80\x01\xfe\x07\x80\x00~\x07\x80\x00\x1e\x07\x80\x00\x0c\x03\x00')
    github_fb = framebuf.FrameBuffer(github_bytearray, 32,32, framebuf.MONO_HLSB)
    screen.blit(github_fb, 0, 0)

def _draw_gitee_logo():
    gitee_bytearray = bytearray(b'\x00\x7f\xff\xfe\x01\xff\xff\xff\x07\xff\xff\xff\x0f\xff\xff\xff\x1f\xff\xff\xff?\xff\xff\xff?\xff\xff\xfe\x7f\xc0\x00\x00\x7f\x80\x00\x00\xff\x00\x00\x00\xfe\x00\x00\x00\xfe\x00\x00\x00\xfe\x00\x00\x00\xfe\x07\xff\xfe\xfe\x0f\xff\xff\xfe\x0f\xff\xff\xfe\x0f\xff\xff\xfe\x0f\xff\xff\xfe\x07\xff\xff\xfe\x00\x00\xff\xfe\x00\x00\x7f\xfe\x00\x00\x7f\xfe\x00\x00\x7f\xfe\x00\x00\xff\xff\x00\x01\xfe\xff\xff\xff\xfe\xff\xff\xff\xfc\xff\xff\xff\xf8\xff\xff\xff\xf0\xff\xff\xff\xe0\x7f\xff\xff\xc0?\xff\xff\x00')
    gitee_fb = framebuf.FrameBuffer(gitee_bytearray, 32,32, framebuf.MONO_HLSB)
    screen.blit(gitee_fb, 0, 0)

def _draw_settings_():
    settings_bytearray = bytearray(b'\x00\x07\xe0\x00\x00\x04 \x00\x02\x04 @\x07\x0c0\xe0\r\xbc=\xb0\x18\xe0\x07\x180\x00\x00\x0c\x18\x00\x00\x18\x0c\x00\x000\x04\x00\x00 \x0c\x03\xc00\x08\x0c0\x10\x18\x18\x18\x18\xf8\x10\x08\x1f\x80 \x04\x01\x80 \x04\x01\x80 \x04\x01\x80 \x04\x01\xf8\x10\x08\x1f\x18\x18\x18\x18\x08\x0c0\x10\x0c\x03\xc00\x04\x00\x00 \x0c\x00\x000\x18\x00\x00\x180\x00\x00\x0c\x18\xe0\x07\x18\r\xb0\r\xb0\x07\x1c8\xe0\x02\x0c0@\x00\x04 \x00\x00\x07\xe0\x00')
    settings_fb = framebuf.FrameBuffer(settings_bytearray, 32,32, framebuf.MONO_HLSB)
    screen.blit(settings_fb, 0, 0)

def _draw_audio_off_():
    audio_off_bytearray = bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xdbm\xb6\xdbm\xb6\xdbm\xb6\xdbm\xb6\xdbm\xb6\xdb\xdbm\xb6\xdbm\xb6\xdbm\xb6\xdbm\xb6\xdbm\xb6\xdb\xdbm\xb6\xdbm\xb6\xdbm\xb6\xdbm\xb6\xdbm\xb6\xdb\xdbm\xb6\xdbm\xb6\xdbm\xb6\xdbm\xb6\xdbm\xb6\xdb\xdbm\xb6\xdbm\xb6\xdbm\xb6\xdbm\xb6\xdbm\xb6\xdb\xdbm\xb6\xdbm\xb6\xdbm\xb6\xdbm\xb6\xdbm\xb6\xdb\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
    audio_off_fb = framebuf.FrameBuffer(audio_off_bytearray, 128,24, framebuf.MONO_HLSB)
    screen.blit(audio_off_fb, 0, 8)

def _draw_audio_on_():
    audio_on_bytearray = bytearray(b'\x18\x000\x00`\x00\xc0\x01\x80\x03\x00\x06\x00\x0c\x00\x18\x18\x000\x00`\x00\xc0\x01\x80\x03\x00\x06\x00\x0c\x00\x18\x18\x000\x00`\x00\xc0\x01\x80\x03\x00\x06\x00\x0c\x00\x18\x18\x000\x00`\x00\xc0\x01\x80\x03\x00\x06\x00\x0c\x00\x18\xdb\x01\xb6\x03l\x06\xd8\r\xb0\x1b`6\xc0m\x80\xdb\xdb\x01\xb6\x03l\x06\xd8\r\xb0\x1b`6\xc0m\x80\xdb\xdb\x01\xb6\x03l\x06\xd8\r\xb0\x1b`6\xc0m\x80\xdb\xdb\x01\xb6\x03l\x06\xd8\r\xb0\x1b`6\xc0m\x80\xdb\xdb\x01\xb6\x03l\x06\xd8\r\xb0\x1b`6\xc0m\x80\xdb\xdbm\xb6\xdbm\xb6\xdbm\xb6\xdbm\xb6\xdbm\xb6\xdb\xdbm\xb6\xdbm\xb6\xdbm\xb6\xdbm\xb6\xdbm\xb6\xdb\xdbm\xb6\xdbm\xb6\xdbm\xb6\xdbm\xb6\xdbm\xb6\xdb\xdbm\xb6\xdbm\xb6\xdbm\xb6\xdbm\xb6\xdbm\xb6\xdb\xdbm\xb6\xdbm\xb6\xdbm\xb6\xdbm\xb6\xdbm\xb6\xdb\xdbm\xb6\xdbm\xb6\xdbm\xb6\xdbm\xb6\xdbm\xb6\xdb\xdb\x01\xb6\x03l\x06\xd8\r\xb0\x1b`6\xc0m\x80\xdb\xdb\x01\xb6\x03l\x06\xd8\r\xb0\x1b`6\xc0m\x80\xdb\xdb\x01\xb6\x03l\x06\xd8\r\xb0\x1b`6\xc0m\x80\xdb\xdb\x01\xb6\x03l\x06\xd8\r\xb0\x1b`6\xc0m\x80\xdb\xdb\x01\xb6\x03l\x06\xd8\r\xb0\x1b`6\xc0m\x80\xdb\x18\x000\x00`\x00\xc0\x01\x80\x03\x00\x06\x00\x0c\x00\x18\x18\x000\x00`\x00\xc0\x01\x80\x03\x00\x06\x00\x0c\x00\x18\x18\x000\x00`\x00\xc0\x01\x80\x03\x00\x06\x00\x0c\x00\x18\x18\x000\x00`\x00\xc0\x01\x80\x03\x00\x06\x00\x0c\x00\x18')
    audio_on_fb = framebuf.FrameBuffer(audio_on_bytearray, 128,24, framebuf.MONO_HLSB)
    screen.blit(audio_on_fb, 0, 8)

def _draw_battery_():
    screen.fill(0)

    screen.rect(0,0,118,32,1)# battery's out border
    screen.pixel(0,0,0)
    screen.pixel(0,31,0)
    screen.pixel(117,31,0)
    screen.pixel(117,0,0) # four outer corners

    screen.rect(1,1,116,30,1) # battery's inner border
    screen.rect(2,2,114,28,1)
    screen.pixel(3,3,1)
    screen.pixel(114,3,1)
    screen.pixel(114,28,1)
    screen.pixel(3,28,1) # four inner corners

    screen.fill_rect(118,7,10,18,1) # battery's top
    screen.pixel(127,7,0)
    screen.pixel(127,24,0)

    screen.fill_rect(5,5,20,22,1) # 20% battery
    screen.pixel(5,5,0)
    screen.pixel(24,5,0)
    screen.pixel(24,26,0)
    screen.pixel(5,26,0)

    screen.fill_rect(27,5,20,22,1) # 40% battery
    screen.pixel(27,5,0)
    screen.pixel(46,5,0)
    screen.pixel(46,26,0)
    screen.pixel(27,26,0)

    screen.fill_rect(49,5,20,22,1) # 60% battery
    screen.pixel(49,5,0)
    screen.pixel(68,5,0)
    screen.pixel(68,26,0)
    screen.pixel(49,26,0)

    screen.fill_rect(71,5,20,22,1) # 80% battery
    screen.pixel(71,5,0)
    screen.pixel(90,5,0)
    screen.pixel(90,26,0)
    screen.pixel(71,26,0)

    screen.fill_rect(93,5,20,22,1) # 100% battery
    screen.pixel(93,5,0)
    screen.pixel(112,5,0)
    screen.pixel(112,26,0)
    screen.pixel(93,26,0)

def _draw_battery_mask_(voltage):

    bat_usage = int(100*(4.2 - voltage))
    # % of the battery usage

    if (bat_usage >= 0) & (bat_usage < 20):
        screen.pixel(112-bat_usage,5,0)
        screen.pixel(112-bat_usage,26,0)
        screen.fill_rect(113-bat_usage,5,bat_usage,22,0)
    elif (bat_usage >= 20) & (bat_usage < 40):
        screen.fill_rect(93,5,20,22,0)
        screen.pixel(110-bat_usage,5,0)
        screen.pixel(110-bat_usage,26,0)
        screen.fill_rect(111-bat_usage,5,bat_usage,22,0)
    elif (bat_usage >= 40) & (bat_usage < 60):
        screen.fill_rect(93,5,20,22,0)
        screen.pixel(108-bat_usage,5,0)
        screen.pixel(108-bat_usage,26,0)
        screen.fill_rect(109-bat_usage,5,bat_usage,22,0)
    elif (bat_usage >= 60) & (bat_usage < 80):
        screen.fill_rect(93,5,20,22,0)
        screen.pixel(106-bat_usage,5,0)
        screen.pixel(106-bat_usage,26,0)
        screen.fill_rect(107-bat_usage,5,bat_usage,22,0)
    elif (bat_usage >= 80) & (bat_usage < 100):
        screen.fill_rect(93,5,20,22,0)
        screen.pixel(104-bat_usage,5,0)
        screen.pixel(104-bat_usage,26,0)
        screen.fill_rect(105-bat_usage,5,bat_usage,22,0)
    elif (bat_usage>=100): # more than 100%
        screen.fill_rect(5,5,108,22,0)
    # else: # less than 0%, then do nothing
        

def _display_welcome_():
    screen.fill(0)
    _draw_gyroflow_logo_()
    # screen.invert(1)
    screen.show()

def _display_idle_():
    # screen.invert(0)
    screen.fill(0)
    _draw_cam_()
    screen.text('FlowShutter', 34, 0, 1)
    screen.text('Powered by', 34, 12, 1)
    screen.text('DusKing', 34, 24, 1)
    screen.text("".join(tuple(vars.version)), 96, 24, 1)
    screen.show()

def _display_starting_():
    screen.fill(0)
    _draw_cam_()
    screen.text('Starting', 34, 0, 1)
    screen.text('FC Disarmed', 34, 12, 1)
    screen.text('Camera start', 34, 24, 1)
    screen.show()

def _display_recording_():
    screen.fill(0)
    _draw_cam_working_()
    screen.text('FlowShutter', 34, 0, 1)
    screen.text('FC Armed', 34, 12, 1)
    screen.text('Recording', 34, 24, 1)
    screen.show()

def _display_stopping_():
    screen.fill(0)
    _draw_cam_()
    screen.text('Stopping', 34, 0, 1)
    screen.text('FC Armed', 34, 12, 1)
    screen.text('Camera stop', 34, 24, 1)
    screen.show()

def _display_battery_():
    _draw_battery_()
    _draw_battery_mask_(vars.vol)
    voltage_str = "%.2fV" % vars.vol
    for i in range(5):
        for j in range(5):
            screen.text(voltage_str,42+i, 11+j,0)
    screen.text(voltage_str,44,13,1)
    screen.show()

def _display_menu_internet_():
    screen.fill(0)
    screen.text('Internet', 34, 0, 1)

    if vars.wlan_state == "DISCONNECTED":
        _draw_wifi_disconnected_()
        screen.text('Disconnected', 34, 12, 1)
        screen.text('NEXT Battery', 34, 24, 1)
    elif vars.wlan_state == "CONNECTED":
        _draw_wifi_connected_()
        screen.text('Connected', 34, 12, 1)
        screen.text('NEXT Source', 34, 24, 1)

    screen.show()

def _display_menu_ota_source_():
    screen.fill(0)
    screen.text('OTA Source', 34, 0, 1)

    if vars.ota_source == 'GitHub':
        _draw_github_logo_()
        screen.text('GitHub', 34, 12, 1)
    elif vars.ota_source == 'Gitee':
        _draw_gitee_logo()
        screen.text('Gitee', 34, 12, 1)

    screen.text('NEXT Channel', 34, 24, 1)
    screen.show()

def _display_menu_ota_channel_():
    screen.fill(0)
    screen.text('OTA Channel', 34, 0, 1)
    screen.text("".join(tuple(vars.ota_channel)), 34, 12, 1)
    screen.text('NEXT Battery', 34, 24, 1)
    screen.show()

def _display_menu_camera_protocol_():
    screen.fill(0)
    _draw_settings_()
    screen.text('Cam Protocol', 34, 0, 1)
    screen.text("".join(tuple(vars.camera_protocol)), 34, 12, 1)
    screen.text('Next Device', 34, 24, 1)
    screen.show()

def _display_menu_reboot_hint_():
    screen.fill(0)
    screen.fill_rect(2,1,124,30,1)
    screen.fill_rect(6,4,116,24,0)
    screen.text('Please reboot', 9, 6, 1)
    screen.text('to apply', 32, 16, 1)
    screen.show()

def _display_menu_device_mode_():
    screen.fill(0)
    _draw_settings_()
    screen.text('Device Mode', 34, 0, 1)
    screen.text("".join(tuple(vars.device_mode)), 34, 12, 1)
    screen.text('Next Marker', 34, 24, 1)
    screen.show()

def _display_menu_inject_mode_():
    screen.fill(0)
    screen.text('Audio Injection', 0, 0, 1)
    if vars.inject_mode == "ON":
        _draw_audio_on_()
    elif vars.inject_mode == "OFF":
        _draw_audio_off_()
    screen.show()

def show_settings_fault():
    screen.fill_rect(20,5,88,22,1)
    screen.fill_rect(21,6,86,20,1)
    screen.text('Settings Fault', 26, 8, 1)
    screen.text('Please Reboot', 26, 20, 1)
    screen.show()

def show_wlan_connecting():
    screen.fill_rect(18,3,92,26,1)
    screen.fill_rect(19,4,90,24,0)
    screen.text('Connecting', 21, 6, 1)
    screen.text('Please wait', 21, 16, 1)
    screen.show()

def show_ap_info():
    screen.fill_rect(0,3,128,26,1)
    screen.fill_rect(1,4,126,24,0)
    screen.text('SSID:'+ wlan.ap_ssid, 3, 6, 1)
    screen.text('Pswd:'+ wlan.ap_password, 3, 16, 1)
    screen.show()

def _show_sony_mtp_ack_():
    screen.fill_rect(18,3,92,26,1)
    screen.fill_rect(19,4,90,24,0)
    screen.text('Sony Remote', 21, 6, 1)
    screen.text('Registered', 21, 16, 1)
    screen.show()

def _show_starting_timeout_():
    screen.fill_rect(10,1,108,30,1)
    screen.fill_rect(14,4,98,24,0)
    screen.text('No ACK back', 17, 6, 1)
    screen.text('Start failed', 17, 16, 1)
    screen.show()
