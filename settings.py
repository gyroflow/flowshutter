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
        vars.device_mode = settings["device_mode"]
        vars.inject_mode = settings["inject_mode"]
        vars.camera_protocol = settings["camera_protocol"]
        print("settings.json loaded")
        test = f.read()
        f.close()

def write_default():
    with open("settings.json", "w") as f:
        settings = {"device_mode":"SLAVE", "inject_mode":"OFF", "camera_protocol":"Sony MTP"}
        json.dump(settings, f)
        f.close()
    _load_()
def read():
    try:
        _load_()
    except KeyError: # settings.json has new member(s)
        print("overwrite default settings")
        write_default()
    except OSError: # settings.json does not exist
        print("create default settings")
        write_default()
