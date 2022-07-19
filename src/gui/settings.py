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
import vram
import target
import time

class UserSettings:
    def __init__(self):
        print(str(time.ticks_us()) + " [Create] User Settings")
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
            settings = {"version":vram.version,
                        "camera_protocol":vram.camera_protocol,
                        "device_mode":vram.device_mode,
                        "inject_mode":vram.inject_mode,
                        "ota_source":vram.ota_source,
                        "ota_channel":vram.ota_channel,
                        "target":target.target}
            json.dump(settings, f)
            f.close()

    def verify(self,content):
        with open("settings.json", "r") as f:
            settings = json.load(f)

            if content == 'version':
                if vram.version != settings["version"]:
                    print(str(time.ticks_us()) + " [ ERROR] User Settings: Version changed. Overwriting default settings")
                    f.close()
                    self.update()        # here we should write the default settings
                    print(str(time.ticks_us()) + " [ ERROR] User Settings: Default settings overwritten")
                else:
                    vram.version = settings["version"]

            if content == 'rest_settings':
                try:
                    index1              = vram.camera_protocol_range.index( settings["camera_protocol"] )
                    vram.camera_protocol= settings["camera_protocol"]
                    vram.update_camera_preset()
                    index2              = vram.device_mode_range.index(     settings["device_mode"]     )
                    vram.device_mode    = settings["device_mode"]
                    index3              = vram.inject_mode_range.index(     settings["inject_mode"]     )
                    vram.inject_mode    = settings["inject_mode"]
                    index4              = vram.ota_source_range.index(      settings["ota_source"]      )
                    vram.ota_source     = settings["ota_source"]
                    index5              = vram.ota_channel_range.index(     settings["ota_channel"]     )
                    vram.ota_channel    = settings["ota_channel"]
                except ValueError: # one of the current settings is not in the valid range
                    print("settings.json is invalid")
                    f.close()
                    self.update()
                    print("updated settings.json")
                    f = open("settings.json", "r")  # then read again, cuz update() closed the file
                    vram.version        = settings["version"]
                    vram.camera_protocol= settings["camera_protocol"]
                    vram.device_mode    = settings["device_mode"]
                    vram.inject_mode    = settings["inject_mode"]
                    vram.ota_source     = settings["ota_source"]
                    vram.ota_channel    = settings["ota_channel"]
                    target.target       = settings["target"]

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

