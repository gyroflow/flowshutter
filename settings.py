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

def read():
    import os
    import json
    import vars
    try:
        os.stat("settings.json")
        with open("settings.json", "r") as f:
            settings = json.load(f)
            vars.device_mode = settings["device_mode"]
            vars.inject_mode = settings["inject_mode"]
            vars.camera_protocol = settings["camera_protocol"]
            # print("settings loaded, value", vars.test)
    except KeyError:
        with open("settings.json", "w") as f:
            settings = {
                "device_mode": "slave",
                "inject_mode": "off",
                "camera_protocol": "mtp"
                }
            json.dump(settings, f)
    except OSError:
        with open("settings.json", "w") as f:
            settings = {"device_mode":"slave","inject_mode":"off","camera_protocol":"mtp"}
            # IDK what makes such difference here, but if I use the code above, then first two settings will be blocked.
            json.dump(settings, f)
