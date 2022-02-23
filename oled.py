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
import vars, ssd1306, target
import framebuf

def _init_():
    i2c = target.init_i2c()
    screen = ssd1306.SSD1306_I2C(128, 32, i2c)
    return screen

screen = _init_()

def update(state):
    if state == "welcome":
        _display_welcome_()
    elif state == "idle":
        _display_idle_()
    elif state == "starting":
        _display_starting_()
    elif state == "recording":
        _display_recording_()
    elif state == "stopping":
        _display_stopping_()
    elif state == "menu_battery":
        _display_menu_battery_()
    elif state == "menu_ap_mode":
        _display_menu_ap_mode_()
    elif state == "menu_camera_protocol":
        _display_menu_camera_protocol_()
    elif state == "menu_device_mode":
        _display_menu_device_mode_()
    elif state == "menu_inject_mode":
        _display_menu_inject_mode_()
    else:
        print("Unknown state: "+ state)

def _draw_gyroflow_logo_():
    gyroflow_bytearray = bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\xc0\x00\x00\x00\x00\xf0\x00\xc0\x00\x00\x00\x00\x00\x00\x00\x03@\x00\x00\x00\x01\x18\x01\xc0\x00\x00\x00\x00\x00\x00\x00\x04@\x00\x00\x00\x01\x0c\x01\xe0\x00\x00\x00\x00\x00\x00\x00\x08\xc1\x00\x00\x00\x01\x04\x03`\x00\x00\x00\x00\x00\x00\x00\x18\x83\x00\x00\x00\x00\x02G0\x00\x00\x00\x00\x00\x00\x00\x11\x87\x00\x00\x00\x02\x01\xe68\x00\x00\x00\x00\x00\x00\x00!\x0e\x00\x00\x00~\xc3\xec\x18\x00\x00\x00\x00\x00\x00\x00b\x0c\x00\x00\x00\x80/<\x0c\x00\x00\x00\x00\x00\x00\x00B\x1c\x00\x00\x00\x81<8\x0c\x07\xe3\x01\xbf\xc0|\x00\xc4\x18\x00\x00\x00\x81\xf0\x19\xfe\x1cq\x830`\xc7\x00\x880\x00\x00\x03A`\x1f\xfe\x18\x10\x8601\x81\x80\x98 \x00\x00\x01e\x00\x0c\x000\x18\xc603\x01\x810@\xff\x80\x017\x00\x0e\x000\x00l03\x00\x81a\xc1\xf9\x02\x03\x18\x80\x06\x00 \x00(?\xe3\x00\x83C\xc3\xe1\x06\x02l\x80\x07\x00 \xf88?\x83\x00\x83\xdc\x87b\x0c\x06s\x00\x1e\x800\x18\x100\xc3\x00\x83\xf0\x86B\x1c\x0c1\x80x\x800\x18\x100c\x01\x86\x80\x84B4\x18\x18`\xe0@\x18\x18\x100a\x81\x84\x80\x8c\x83\xe40\x18\\\xd0@\x1c8\x1001\xc7\x1c\x81\xb7\x00\x07\xc0\x0c#\x80\xc0\x07\xe0\x100\x10~8\x80\xe0\x00\x03\x00\x0c<\x7f\x80\x00\x00\x00\x00\x00\x00H\x80\x00\x00\x00\x00\x06\xd0\x00\x00\x00\x00\x00\x00\x00\x00\t\x80\x00\x00\x00\x00\x07\xe8\x10\x00\x00\x00\x00\x00\x00\x00\t\x00\x00\x00\x00\x00\x03\x8c\x10\x00\x00\x00\x00\x00\x00\x00\x19\x00\x00\x00\x00\x00\x00\x04 \x00\x00\x00\x00\x00\x00\x00\x1b\x00\x00\x00\x00\x00\x00\x03 \x00\x00\x00\x00\x00\x00\x00\x0e\x00\x00\x00\x00\x00\x00\x01\xc0\x00\x00\x00\x00\x00\x00\x00\x0c\x00\x00\x00\x00\x00')
    gyroflow_fb = framebuf.FrameBuffer(gyroflow_bytearray, 128,28, framebuf.MONO_HLSB)
    screen.blit(gyroflow_fb, 0, 2)

def _draw_cam_():
    # start flowshutter logo
    # first is the "cam"
    screen.hline(7,0,18,1)

    screen.hline(6,1,6,1)
    screen.hline(20,1,6,1)

    screen.hline(5,2,6,1)
    screen.hline(21,2,6,1)

    screen.hline(4,3,6,1)
    screen.hline(22,3,6,1)

    screen.hline(3,4,7,1)
    screen.hline(22,4,7,1)

    screen.hline(2,5,8,1)
    screen.hline(22,5,8,1)

    screen.hline(1,6,10,1)
    screen.hline(21,6,10,1)

    screen.hline(1,7,30,1)
    screen.hline(0,8,32,1)

    screen.hline(0,9,4,1)
    screen.hline(28,9,4,1)

    screen.hline(0,10,3,1)
    screen.hline(29,10,3,1)

    screen.vline(0,11,17,1)
    screen.vline(1,11,17,1)
    screen.vline(30,11,17,1)
    screen.vline(31,11,17,1)

    screen.hline(0,28,3,1)
    screen.hline(29,28,3,1)

    screen.hline(0,29,4,1)
    screen.hline(28,29,4,1)

    screen.hline(1,30,30,1)
    screen.hline(2,31,28,1)

    screen.hline(12,10,7,1)
    screen.hline(10,11,11,1)
    
    screen.hline(9,12,3,1)
    screen.hline(19,12,3,1)

    screen.hline(8,13,2,1)
    screen.hline(21,13,2,1)

    screen.hline(7,14,2,1)
    screen.hline(22,14,2,1)

    screen.hline(6,15,2,1)
    screen.hline(23,15,2,1)

    screen.vline(4,18,5,1)
    screen.vline(5,16,9,1)
    screen.vline(6,16,2,1)
    screen.vline(6,23,2,1)

    screen.vline(24,16,2,1)
    screen.vline(24,23,2,1)
    screen.vline(25,16,9,1)
    screen.vline(26,18,5,1)

    screen.hline(6,25,2,1)
    screen.hline(23,25,2,1)
    screen.hline(7,26,2,1)
    screen.hline(22,26,2,1)

    screen.hline(8,27,2,1)
    screen.hline(21,27,2,1)

    screen.hline(9,28,3,1)
    screen.hline(19,28,3,1)
    screen.hline(10,29,11,1)

    # now the "status" led
    screen.hline(26,11,3,1)
    screen.hline(26,15,3,1)
    screen.vline(25,12,3,1)
    screen.vline(29,12,3,1)

def _draw_cam_idle_():
    
    _draw_cam_()
    # now the "shutter"
    screen.hline(13,15,5,1)
    screen.hline(13,25,5,1)

    screen.vline(9,19,3,1)
    screen.vline(21,19,3,1)

    screen.line(12,15,9,18,1)
    screen.line(9,22,12,25,1)
    screen.line(18,15,21,18,1)
    screen.line(21,22,18,25,1)
    # end logo

def _draw_cam_recording_():

    _draw_cam_()
    # change the "status"
    screen.fill_rect(26,12,3,3,1)
    # now "open" the "shutter"
    screen.hline(12,15,7,1)
    screen.hline(11,16,9,1)
    screen.hline(10,17,11,1)
    screen.fill_rect(9,18,13,5,1)
    screen.hline(10,23,11,1)
    screen.hline(11,24,9,1)
    screen.hline(12,25,7,1)

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


def _display_welcome_():
    screen.fill(0)
    _draw_gyroflow_logo_()
    # screen.invert(1)
    screen.show()

def _display_idle_():
    # screen.invert(0)
    screen.fill(0)
    _draw_cam_idle_()
    screen.text('FlowShutter', 34, 0, 1)
    screen.text('Powered by', 34, 12, 1)
    screen.text('DusKing', 34, 24, 1)
    screen.text("".join(tuple(vars.version)), 98, 24, 1)
    screen.show()

def _display_starting_():
    screen.fill(0)
    _draw_cam_recording_()
    screen.text('Starting', 34, 0, 1)
    screen.text('FC Disarmed', 34, 12, 1)
    screen.text('Sony start', 34, 24, 1)
    screen.show()

def _display_recording_():
    screen.fill(0)
    _draw_cam_recording_()
    screen.text('FlowShutter', 34, 0, 1)
    screen.text('FC Armed', 34, 12, 1)
    screen.text('Sony recording', 34, 24, 1)
    screen.show()

def _display_stopping_():
    screen.fill(0)
    _draw_cam_idle_()
    screen.text('Stopping', 34, 0, 1)
    screen.text('FC Armed', 34, 12, 1)
    screen.text('Sony ending', 34, 24, 1)
    screen.show()

def _display_menu_battery_():
    _draw_battery_()

    voltage = '4.0V' # later this should be turn to some ADC values
    for i in range(5):
        for j in range(5):
            screen.text(voltage,42+i, 11+j,0)
    screen.text(voltage,44,13,1)

    # TODO: also here should be some math to calculate the battery recct

    screen.show()

def _display_menu_ap_mode_():
    screen.fill(0)
    _draw_cam_idle_()
    screen.text('Access Point', 34, 0, 1)
    screen.text("".join(tuple(vars.ap_state)), 34, 12, 1)
    screen.text('NEXT Battery', 34, 24, 1)
    screen.show()

def _display_menu_camera_protocol_():
    screen.fill(0)
    _draw_cam_idle_()
    screen.text('Cam Protocol', 34, 0, 1)
    screen.text("".join(tuple(vars.camera_protocol)), 34, 12, 1)
    screen.text('PAGE to save', 34, 24, 1)
    screen.show()

def _display_menu_device_mode_():
    screen.fill(0)
    _draw_cam_idle_()
    screen.text('Device Mode', 34, 0, 1)
    screen.text("".join(tuple(vars.device_mode)), 34, 12, 1)
    screen.text('Next Marker', 34, 24, 1)
    screen.show()

def _display_menu_inject_mode_():
    screen.fill(0)
    _draw_cam_idle_()
    screen.text('Injection', 34, 0, 1)
    screen.text("".join(tuple(vars.inject_mode)), 34, 12, 1)
    screen.text('Next Camera', 34, 24, 1)
    screen.show()

def display_settings_fault():
    screen.fill_rect(20,5,88,22,1)
    screen.fill_rect(21,6,86,20,1)
    screen.text('Settings Fault', 26, 8, 1)
    screen.text('Please Reboot', 26, 20, 1)
    screen.show()
