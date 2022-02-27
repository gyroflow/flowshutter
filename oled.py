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
        display_recording()
    elif state == "stopping":
        _display_stopping_()
    elif state == "menu_battery":
        display_menu_battery()
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
    gyroflow_bytearray = bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\xc0\x00\x00\x00\x00\xf0\x00\xc0\x00\x00\x00\x00\x00\x00\x00\x03@\x00\x00\x00\x01\x98\x01\xc0\x00\x00\x00\x00\x00\x00\x00\x06@\x00\x00\x00\x01\x0c\x01\xe0\x00\x00\x00\x00\x00\x00\x00\x0cA\x80\x00\x00\x03\x06\x03p\x00\x00\x00\x00\x00\x00\x00\x18\xc3\x00\x00\x00\x02\x02G0\x00\x00\x00\x00\x00\x00\x001\x87\x00\x00\x00\x1a\x01\xe68\x00\x00\x00\x00\x00\x00\x00!\x0e\x00\x00\x00r\xc3\xee\x18\x00\x00\x00\x00\x00\x00\x00c\x0c\x00\x00\x00\xc2O|\x1c\x00\x00\x00\x00\x00\x00\x00B\x18\x00\x00\x00\x83<8\x0c\x0f\xe3\x03?\xe0|\x00\xc4\x10\x00\x00\x00\x818\x18\x0e\x1f\xf3\x87?\xf0\xfe\x00\x8c0\x00\x00\x01\xc1\x80\x18\xfe89\xce01\x83\x01\x98`\x00\x00\x01d\x80\x0f\x800\x18\xcc03\x01\x81\xb0\xc0\xff\x80\x016\x80\x0e\x00p\x00x03\x01\x81a\xc1\xe1\x82\x03X\x80\x06\x00p\x00x?\xe3\x01\x83\xc3\x83!\x06\x02l\x00\x07\x00p\xf80?\xc3\x01\x83\xce\x87#\x0e\x06w\x80\x1e\x80p\xf800\xc3\x01\x87\xf8\x86"\x1c\x0c1\xc0x\xc0p\x1800\xe3\x01\x87\x81\x86b4\x188p\xe0@8800q\x83\x0c\x81\x0c\xc3\xe4p\x18>\x00@<x008\xfe\x1c\x81\xbf\x81\x86\xc0\x0c\x07\x90\xc0\x1f\xf000\x18|<\x80\xe2\x00\x03\x80\x0c0\xff\x80\x07\xc0\x00\x00\x00\x00h\x80\x00\x00\x00\x00\x060\x04\x00\x00\x00\x00\x00\x00\x00\x08\x80\x00\x00\x00\x00\x06\x98\x10\x00\x00\x00\x00\x00\x00\x00\x19\x80\x00\x00\x00\x00\x03\x8c\x10\x00\x00\x00\x00\x00\x00\x00\x11\x00\x00\x00\x00\x00\x01\x060\x00\x00\x00\x00\x00\x00\x00\x13\x00\x00\x00\x00\x00\x00\x03`\x00\x00\x00\x00\x00\x00\x00\x1e\x00\x00\x00\x00\x00\x00\x01\xc0\x00\x00\x00\x00\x00\x00\x00\x0c\x00\x00\x00\x00\x00')
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
    _draw_cam_idle_()
    screen.text('FlowShutter', 34, 0, 1)
    screen.text('Powered by', 34, 12, 1)
    screen.text('DusKing', 34, 24, 1)
    screen.text("".join(tuple(vars.version)), 96, 24, 1)
    screen.show()

def _display_starting_():
    screen.fill(0)
    _draw_cam_recording_()
    screen.text('Starting', 34, 0, 1)
    screen.text('FC Disarmed', 34, 12, 1)
    screen.text('Sony start', 34, 24, 1)
    screen.show()

def display_recording():
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

def display_menu_battery():
    _draw_battery_()

    voltage = 3.91 # TODO: later this should be turn to some ADC values
    voltage_str = "%.2fV" % voltage
    for i in range(5):
        for j in range(5):
            screen.text(voltage_str,42+i, 11+j,0)
    screen.text(voltage_str,44,13,1)

    _draw_battery_mask_(voltage)

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
    screen.text('Next Device', 34, 24, 1)
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
    screen.text('Page to MAIN', 34, 24, 1)
    screen.show()

def display_settings_fault():
    screen.fill_rect(20,5,88,22,1)
    screen.fill_rect(21,6,86,20,1)
    screen.text('Settings Fault', 26, 8, 1)
    screen.text('Please Reboot', 26, 20, 1)
    screen.show()
