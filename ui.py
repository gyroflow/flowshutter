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
import ap, oled, vars, json, settings
oled1 = oled.init()

def update(t):
    
    if vars.shutter_state == "idle":
        idle()
    elif vars.shutter_state == "starting":
        starting()
    elif vars.shutter_state == "recording":
        recording()
    elif vars.shutter_state == "stopping":
        stopping()
    elif vars.shutter_state == "menu_battery":
        menu_battery()
    elif vars.shutter_state == "menu_ap_mode":
        menu_ap_mode() 
    elif vars.shutter_state == "menu_device_mode":
        menu_device_mode()
    elif vars.shutter_state == "menu_inject_mode":
        menu_inject_mode()
    elif vars.shutter_state == "menu_camera_protocol":
        menu_camera_protocol()

def idle():
    oled.display_idle_info(oled1)

    # enter to start recording if in master or master/slave mode
    if vars.button_enter == "pressed":
        vars.button_enter = "released"

        if vars.device_mode == "MASTER/SLAVE":
            oled.display_recording_info(oled1)
            vars.arm_state = "arm"
            vars.shutter_state = "recording"

    ## page to battery menu
    if vars.button_page == "pressed":
        vars.button_page = "released"
        
        vars.shutter_state = "menu_battery"
        print("show battery")

def recording():
    oled.display_recording_info(oled1)
    # enter to stop recording if in master or master/slave mode
    if vars.button_enter == "pressed":
        vars.button_enter = "released"
        if vars.device_mode == "MASTER/SLAVE":
            oled.display_stopping_info(oled1)
            vars.arm_state = "disarm"
            vars.shutter_state = "idle"

def starting():
    oled.display_starting_info(oled1)

def stopping():
    oled.display_stopping_info(oled1)


def menu_battery():
    oled.display_menu_battery(oled1)

    # page to camera protocol menu
    if vars.button_page == "pressed":
        vars.button_page = "released"
        vars.shutter_state = "menu_camera_protocol"
    
    # enter to hidden ap mode menu
    if vars.button_enter == "pressed":
        vars.button_enter = "released"       
        vars.shutter_state = "menu_ap_mode"

def menu_ap_mode():
    oled.display_menu_ap_mode(oled1)

    # enter to set ap
    if vars.button_enter == "pressed":
        vars.button_enter = "released"
        if vars.ap_state == "DOWN":
            ap.up()
            oled.display_menu_ap_mode(oled1)
        else:
            ap.down()
            oled.display_menu_ap_mode(oled1)

    ## page to back to battery menu
    if vars.button_page == "pressed":
        vars.button_page = "released"
        
        vars.shutter_state = "menu_battery"
        print("show battery")

def menu_camera_protocol():
    oled.display_menu_camera_protocol(oled1)

    # enter to set camera protocol
    if vars.button_enter == "pressed":
        vars.button_enter = "released"

        vars.camera_protocol = vars.next(vars.camera_protocol_range, vars.camera_protocol)
        settings.update_camera_preset()
        oled.display_menu_camera_protocol(oled1)
        print("var", vars.device_mode)
    
    # page to save and to device mode
    if vars.button_page == "pressed":
        vars.button_page = "released"
        settings.update()
        vars.shutter_state = "menu_device_mode"

def menu_device_mode():
    oled.display_menu_device_mode(oled1)

    # enter to set device mode
    if vars.button_enter == "pressed":
        vars.button_enter = "released"

        vars.device_mode = vars.next(vars.device_mode_range, vars.device_mode)
        oled.display_menu_device_mode(oled1)

    # page to inject mode menu
    if vars.button_page == "pressed":
        vars.button_page = "released"
        
        vars.shutter_state = "menu_inject_mode"

def menu_inject_mode():
    oled.display_menu_inject_mode(oled1)

    # enter to set inject mode
    if vars.button_enter == "pressed":
        vars.button_enter = "released"
        
        vars.inject_mode = vars.next(vars.inject_mode_range, vars.inject_mode)
        oled.display_menu_inject_mode(oled1)

    ## page to save and back to idle
    if vars.button_page == "pressed":
        vars.button_page = "released"
        settings.update()
        vars.shutter_state = "idle"

