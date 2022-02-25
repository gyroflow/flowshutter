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
import ap, buttons,oled, vars, json, settings, sony_multiport

welcome_time_count = 0

def update(t):
    buttons.check(t)
    if vars.shutter_state == "welcome":
        _welcome_()
    elif vars.shutter_state == "idle":
        _idle_()
    elif vars.shutter_state == "starting":
        _starting_()
    elif vars.shutter_state == "recording":
        _recording_()
    elif vars.shutter_state == "stopping":
        _stopping_()
    elif vars.shutter_state == "menu_battery":
        _menu_battery_()
    elif vars.shutter_state == "menu_ap_mode":
        _menu_ap_mode_() 
    elif vars.shutter_state == "menu_camera_protocol":
        _menu_camera_protocol_()
    elif vars.shutter_state == "menu_device_mode":
        _menu_device_mode_()
    elif vars.shutter_state == "menu_inject_mode":
        _menu_inject_mode_()

def _check_oled_():# check if we need to update the OLED
    if vars.previous_state != vars.shutter_state:
        vars.previous_state = vars.shutter_state
        oled.update(vars.shutter_state)

def _welcome_():
    global welcome_time_count
    _check_oled_()

    # enter do nothing
    if vars.button_enter == "pressed":
        vars.button_enter = "released"
    
    # page do nothing
    if vars.button_page == "pressed":
        vars.button_page = "released"

    # welcome auto switch
    if welcome_time_count <= 600:
        welcome_time_count = welcome_time_count + 1
    else:
        vars.shutter_state = "idle"

def _idle_():
    _check_oled_()

    # enter to start recording if in master or master/slave mode
    if vars.button_enter == "pressed":
        vars.button_enter = "released"
        _rec_enter_()

    ## page to battery menu
    if vars.button_page == "pressed":
        vars.button_page = "released"
        vars.shutter_state = "menu_battery"

def _starting_():
    _check_oled_()

    # enter do nonthing
    if vars.button_enter == "pressed":
        vars.button_enter = "released"
    
    # page do nonthing
    if vars.button_page == "pressed":
        vars.button_page = "released"

def _recording_():
    _check_oled_()
    
    # enter to stop recording if in master or master/slave mode
    if vars.button_enter == "pressed":
        vars.button_enter = "released"
        _rec_enter_()
    # page do nothing for now: TODO: let page cicle between rec_battery and recording
    if vars.button_page == "pressed":
        vars.button_page = "released"

def _stopping_():
    _check_oled_()

    # enter do nothing
    if vars.button_enter == "pressed":
        vars.button_enter = "released"
    
    # page do nothing
    if vars.button_page == "pressed":
        vars.button_page = "released"

def _menu_battery_():
    _check_oled_()

    # page to camera protocol menu
    if vars.button_page == "pressed":
        vars.button_page = "released"
        vars.shutter_state = "menu_camera_protocol"
    
    # enter to hidden ap mode menu
    if vars.button_enter == "pressed":
        vars.button_enter = "released"       
        vars.shutter_state = "menu_ap_mode"

def _menu_ap_mode_():
    _check_oled_()

    # enter to set ap up or down
    if vars.button_enter == "pressed":
        vars.button_enter = "released"
        if vars.ap_state == "DOWN":
            ap.up()
            oled.update(vars.shutter_state)
        else:
            ap.down()
            oled.update(vars.shutter_state)

    ## page to back to battery menu
    if vars.button_page == "pressed":
        vars.button_page = "released"
        vars.shutter_state = "menu_battery"

def _menu_camera_protocol_():
    _check_oled_()

    # enter to set camera protocol
    if vars.button_enter == "pressed":
        vars.button_enter = "released"
        vars.camera_protocol = vars.next(vars.camera_protocol_range, vars.camera_protocol)
        settings.update_camera_preset()
        oled.update(vars.shutter_state)
        settings.update()

    # page to device mode
    if vars.button_page == "pressed":
        vars.button_page = "released"
        vars.shutter_state = "menu_device_mode"

def _menu_device_mode_():
    _check_oled_()

    # enter to set device mode
    if vars.button_enter == "pressed":
        vars.button_enter = "released"
        vars.device_mode = vars.next(vars.device_mode_range, vars.device_mode)
        oled.update(vars.shutter_state)
        settings.update()

    # page to inject mode menu
    if vars.button_page == "pressed":
        vars.button_page = "released"       
        vars.shutter_state = "menu_inject_mode"

def _menu_inject_mode_():
    _check_oled_()

    # enter to set inject mode
    if vars.button_enter == "pressed":
        vars.button_enter = "released"
        vars.inject_mode = vars.next(vars.inject_mode_range, vars.inject_mode)
        oled.update(vars.shutter_state)
        settings.update()

    ## page to save and back to idle
    if vars.button_page == "pressed":
        vars.button_page = "released"
        vars.shutter_state = "idle"

def _rec_enter_():
    if (vars.camera_protocol == "Sony MTP") & (vars.device_mode == "MASTER/SLAVE"):
        sony_multiport.uart2.write(sony_multiport.REC_PRESS)
        sony_multiport.uart2.write(sony_multiport.REC_RELEASE)
        if vars.shutter_state == "idle":
            vars.shutter_state = "starting"
        elif vars.shutter_state == "recording":
            vars.shutter_state = "stopping"
