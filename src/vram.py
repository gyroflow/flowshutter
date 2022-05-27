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
## battery voltage
vol = 4.0
## ARM and DISARM global flag
arm_state = "disarm" #the state of the ARM/DISARM
oled_tasklist = []
# "arm"

## flowshutter working state
previous_state = "blank"
shutter_state = "welcome"
# "starting"
# "recording"
# "stopping"
# "battery"
# "menu_internet"
# "menu_ota_source"
# "menu_ota_channel"
# "menu_ota_check"
# "menu_camera_protocol"
# "menu_device_mode"
# "menu_inject_mode"
info = "welcome"
# this is the canvas state
# basically just shutter_state

## button state
button_page = "released"
button_enter = "released"

## WLAN state
wlan_state = "DISCONNECTED"
# "CONNECTED"

## OLED state
oled_need_update = "no"
# "yes"
## Other settings is coming soon!


# user_settings:
version = "0.61" # when new user settings added, this should be update firstly!
device_mode = "SLAVE"
inject_mode = "OFF"
camera_protocol = "Sony MTP"
ota_source = "GitHub"
ota_channel = "stable"

camera_protocol_range = ["Sony MTP","MMTRY GND", "3V3 Schmitt", "NO"]
device_mode_range = ["SLAVE", "MASTER/SLAVE"]
inject_mode_range = ["OFF", "ON"]
ota_source_range = ["GitHub", "Gitee"]
ota_channel_range = ["stable", "beta", "dev"]

def update_camera_preset():# per camera protocol
    global camera_protocol
    global device_mode
    global device_mode_range
    if camera_protocol == "Sony MTP":
        device_mode = "SLAVE"
        device_mode_range = ["SLAVE", "MASTER/SLAVE"]
    elif camera_protocol == "NO" or camera_protocol == "MMTRY GND" or camera_protocol == "3V3 Schmitt":
        device_mode = "MASTER"
        device_mode_range = ["MASTER"]

def next(range, current):
    index = range.index(current)
    if index == len(range) - 1:
        return range[0]
    else:
        return range[index + 1]
