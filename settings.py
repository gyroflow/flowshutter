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
import vars

def _load_():
    with open("settings.json", "r") as f:
        settings = json.load(f)

        if vars.version != settings["version"]:
            print("settings.json is outdated")
            f.close()
            update()        # here we should write the default settings
            print("updated settings.json")
            f = open("settings.json", "r") # then read again, cuz update() closed the file
            vars.version = vars.version
        else:
            vars.version = settings["version"]

        vars.device_mode = settings["device_mode"]
        vars.inject_mode = settings["inject_mode"]
        vars.camera_protocol = settings["camera_protocol"]
        print("settings.json loaded")
        f.close()

def default():
    with open("settings.json", "w") as f:
        settings = {"version":vars.version,"device_mode":"SLAVE", "inject_mode":"OFF", "camera_protocol":"Sony MTP"}
        json.dump(settings, f)
        f.close()

def update():
    with open("settings.json", "w") as f:
        settings = {"version":vars.version,"device_mode":vars.device_mode, "inject_mode":vars.inject_mode, "camera_protocol":vars.camera_protocol}
        json.dump(settings, f)
        f.close()

def read():
    try:
        _load_()
    except KeyError:    # settings.json has new member(s)
        print("New members. Overwriting default settings")
        ## test
        f=open("settings.json", "r")
        print("".join(f.read()))
        ## test end
        update()        # here we should write the default settings
        _load_()
    except OSError:     # settings.json does not exist
        print("no settings.json was found. Creating default settings")
        update()        # here we should write the default settings
        _load_()
    ## test
    f=open("settings.json", "r")
    print("".join(f.read()))
    ## test end

def update_camera_preset():# per camera protocol
    if vars.camera_protocol == "Sony MTP":
        vars.device_mode = "SLAVE"
        vars.device_mode_range = ["SLAVE", "MASTER/SLAVE"]
    elif vars.camera_protocol == "NO":
        vars.device_mode = "MASTER"
        vars.device_mode_range = ["MASTER"]
