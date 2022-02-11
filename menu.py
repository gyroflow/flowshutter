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
import oled, vars
oled1 = oled.init()

def update(t):
    if vars.shutter_state == "idle":
        if vars.button1_trigger == "yes":
            vars.button1_trigger = "no"
            oled.display_menu_battery(oled1)
            vars.shutter_state = "menu_battery"
            print("show battery")
    elif vars.shutter_state == "menu_battery":
        if vars.button1_trigger == "yes":
            vars.button1_trigger = "no"
            oled.display_menu_settings(oled1)
            vars.shutter_state = "menu_test"
    elif vars.shutter_state == "menu_test":
        if vars.button2_trigger == "yes":
            vars.button2_trigger = "no"


        if vars.button1_trigger == "yes":
            vars.button1_trigger = "no"
            oled.display_idle_info(oled1)
            vars.shutter_state = "idle"
            print("show idle")