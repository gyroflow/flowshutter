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
import json, os
import target
import time

class UserSettings:
    def __init__(self):
        print(str(time.ticks_us()) + " [Create] User Settings")
        self.settings = {
            'version':          '0.66',# when new user settings added, this should be update firstly!
            'camera_protocol':  'NO',
            'device_mode':      'MASTER',
            'inject_mode':      'OFF',
            'ota_source':       'GitHub',
            'ota_channel':      'stable',
            'target_name':      target.name
        }
        self.camera_protocol_range = ["NO", "MMTRY GND", "3V3 Schmitt", "SONY MTP", "ZCAM UART"]
        # camera_protocol_range = ["NO", "MMTRY GND", "3V3 Schmitt", "SONY MTP", "ZCAM UART", "LANC"]
        self.device_mode_range = ["MASTER"]
        self.inject_mode_range = ["OFF", "ON"]
        self.ota_source_range = ["GitHub", "Gitee"]
        self.ota_channel_range = ["stable", "beta", "dev"]
        self.read()
        print(str(time.ticks_us()) + " [  OK  ] User Settings")

    def read(self):
        print(str(time.ticks_us()) + " [ Read ] User Settings")
        try:
            self.load_json('read')
        except KeyError:   # new member(s)
            print(str(time.ticks_us()) + " [ ERROR] User Settings: New members. Overwriting default settings")
            self.load_json('force')
        except OSError:     # settings.json does not exist
            print(str(time.ticks_us()) + " [ ERROR] User Settings: No user setting exists.")
            self.load_json('force')
        print(str(time.ticks_us()) + " [  OK  ] User Settings Loaded")

    def update(self):
        with open("settings.json", "w") as f:
            json.dump(self.settings, f)
            f.close()

    def verify(self,content):
        with open("settings.json", "r") as f:
            local_settings = json.load(f)

            if content == 'version':
                if self.settings['version'] != local_settings["version"]:
                    print(str(time.ticks_us()) + " [ ERROR] User Settings: Version changed. Overwriting default settings")
                    f.close()
                    self.update()        # here we should write the default settings
                    print(str(time.ticks_us()) + " [ ERROR] User Settings: Default settings overwritten")
                else:
                    self.settings['version'] = local_settings["version"]

            if content == 'rest_settings':
                try:
                    index1              = self.camera_protocol_range.index( local_settings["camera_protocol"] )
                    self.settings['camera_protocol'] = local_settings["camera_protocol"]
                    self.update_camera_preset()
                    index2              = self.device_mode_range.index(     local_settings["device_mode"]     )
                    self.settings['device_mode']     = local_settings["device_mode"]
                    index3              = self.inject_mode_range.index(     local_settings["inject_mode"]     )
                    self.settings['inject_mode']     = local_settings["inject_mode"]
                    index4              = self.ota_source_range.index(      local_settings["ota_source"]      )
                    self.settings['ota_source']      = local_settings["ota_source"]
                    index5              = self.ota_channel_range.index(     local_settings["ota_channel"]     )
                    self.settings['ota_channel']     = local_settings["ota_channel"]
                except ValueError: # one of the current settings is not in the valid range
                    print("settings.json is invalid")
                    f.close()
                    self.update()
                    print("updated settings.json")
                    f = open("settings.json", "r")  # then read again, cuz update() closed the file
                    local_settings = json.load(f)
                    self.settings['version']        = local_settings["version"]
                    self.settings['camera_protocol']= local_settings["camera_protocol"]
                    self.settings['device_mode']    = local_settings["device_mode"]
                    self.settings['inject_mode']    = local_settings["inject_mode"]
                    self.settings['ota_source']     = local_settings["ota_source"]
                    self.settings['ota_channel']    = local_settings["ota_channel"]
                    self.settings['target_name']    = local_settings["target_name"]

    def load_json(self,argv):
        if argv == 'force':
            self.update()
        elif argv == 'read':
            pass
        else:
            print(str(time.ticks_us()) + " [ ERROR] User Settings: Invalid argument: " + str(argv))
        self.verify('version')
        self.verify('rest_settings')
        print("settings.json loaded")

    def update_camera_preset(self):# per camera protocol
        if self.settings['camera_protocol'] == "SONY MTP":
            self.settings['device_mode'] = "SLAVE"
            self.device_mode_range = ["SLAVE", "MASTER/SLAVE"]
        # if camera_protocol == "ZCAM UART":
        #     device_mode = "MASTER"
        #     device_mode_range = ["MASTER", "TEST"]
        # elif camera_protocol == "NO" or camera_protocol == "MMTRY GND" or camera_protocol == "3V3 Schmitt" or camera_protocol == "LANC":
        elif self.settings['camera_protocol'] == ("NO" or  "MMTRY GND" or "3V3 Schmitt" or "ZCAM UART"):
            self.settings['device_mode'] = "MASTER"
            self.device_mode_range = ["MASTER"]

    def cycle(self,direction,range,current):
        index = range.index(current)
        if direction == 'nxt':
            if index == len(range) - 1:
                return range[0]
            else:
                return range[index + 1]
        elif direction == 'prv':
            if index == 0:
                return range[len(range) - 1]
            else:
                return range[index - 1]
