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
import target, vram

def _load_():
    with open("settings.json", "r") as f:
        settings = json.load(f)

        if vram.version != settings["version"]:
            print("settings.json is outdated")
            f.close()
            update()        # here we should write the default settings
            print("updated settings.json")
            f = open("settings.json", "r") # then read again, cuz update() closed the file
            vram.version = vram.version
        else:
            vram.version = settings["version"]
        
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
            update()
            print("updated settings.json")
            f = open("settings.json", "r")  # then read again, cuz update() closed the file
            vram.version        = settings["version"]
            vram.camera_protocol= settings["camera_protocol"]
            vram.device_mode    = settings["device_mode"]
            vram.inject_mode    = settings["inject_mode"]
            vram.ota_source     = settings["ota_source"]
            vram.ota_channel    = settings["ota_channel"]
            
        print("settings.json loaded")
        f.close()

def update(): # update settings.json
    with open("settings.json", "w") as f:
        settings = {"version":vram.version,
                    "device_mode":vram.device_mode,
                    "inject_mode":vram.inject_mode,
                    "camera_protocol":vram.camera_protocol,
                    "ota_source":vram.ota_source,
                    "ota_channel":vram.ota_channel}
        json.dump(settings, f)
        f.close()

def read(): # read settings.json and set vram
    try:
        _load_()
    except KeyError:    # settings.json has new member(s)
        print("New members. Overwriting default settings")
        ## test
        f=open("settings.json", "r")
        print("".join(f.read()))
        ## test end
        update()        # write current settings to settings.json
        _load_()
    except OSError:     # settings.json does not exist
        print("no settings.json was found. Creating default settings")
        update()        # create default settings
        _load_()
    ## test
    f=open("settings.json", "r")
    print("".join(f.read()))
    ## test end
