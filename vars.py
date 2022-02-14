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
## ARM and DISARM global flag
arm_state = "disarm"
# "arm"

## flowshutter working state
shutter_state = "idle"
# "starting"
# "recording"
# "stopping"

button_page = "released"
button_enter = "released"
## Other settings is coming soon!

# user_settings:
version = "0.42" # this should be update firstly!
device_mode = "SLAVE"
inject_mode = "OFF"
camera_protocol = "Sony MTP"

device_mode_range = ["SLAVE", "MASTER/SLAVE"]
inject_mode_range = ["OFF", "ON"]
camera_protocol_range = ["Sony MTP", "New protocol"]

def next(range, current):
    try:
        index = range.index(current)
        if index == len(range) - 1:
            return range[0]
        else:
            return range[index + 1]
    except ValueError:
        import settings, oled
        settings.write_default()
        print("Error: settings.json is corrupted. Overwritten a new one.")
        print("Please reboot the device.")
        ## later there should implenment an error message on the OLED
        settings.read()
