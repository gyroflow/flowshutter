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
import oled, vars, json
oled1 = oled.init()

def update(t):
    
    if vars.shutter_state == "idle":
        ## idle ==> battery
        if vars.button_page == "pressed":
            vars.button_page = "released"
            oled.display_menu_battery(oled1)
            vars.shutter_state = "menu_battery"
            print("show battery")
    

    elif vars.shutter_state == "menu_battery":
        ## battery ==> device mode
        if vars.button_page == "pressed":
            vars.button_page = "released"
            oled.display_menu_device_mode(oled1)
            vars.shutter_state = "menu_device_mode"
    

    elif vars.shutter_state == "menu_device_mode":
        if vars.button_enter == "pressed":
            vars.button_enter = "released"

            vars.device_mode = vars.next(vars.device_mode_range, vars.device_mode)
            oled.display_menu_device_mode(oled1)

        ## device mode ==> inject mode
        if vars.button_page == "pressed":
            vars.button_page = "released"
            oled.display_menu_inject_mode(oled1)
            vars.shutter_state = "menu_inject_mode"


    elif vars.shutter_state == "menu_inject_mode":
        if vars.button_enter == "pressed":
            vars.button_enter = "released"

            vars.inject_mode = vars.next(vars.inject_mode_range, vars.inject_mode)
            oled.display_menu_inject_mode(oled1)

        ## inject mode ==> camera protocol
        if vars.button_page == "pressed":
            vars.button_page = "released"
            oled.display_menu_camera_protocol(oled1)
            vars.shutter_state = "menu_camera_protocol"


    elif vars.shutter_state == "menu_camera_protocol":
        if vars.button_enter == "pressed":
            vars.button_enter = "released"

            vars.camera_protocol = vars.next(vars.camera_protocol_range, vars.camera_protocol)
            oled.display_menu_camera_protocol(oled1)
            
        if vars.button_page == "pressed":
            vars.button_page = "released"

            print("show idle")##save settings
            with open("settings.json", "w") as f:
                settings = {
                    "version": vars.version,
                    "device_mode": vars.device_mode,
                    "inject_mode": vars.inject_mode,
                    "camera_protocol": vars.camera_protocol
                    }
                json.dump(settings, f)
                f.close()
            ## test
            f=open("settings.json", "r")
            print("".join(f.read()))
            ## test end
            oled.display_idle_info(oled1)
            vars.shutter_state = "idle"