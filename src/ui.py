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
import wlan, canvas, vram, json, settings, camera, ota
ota = ota.OTA()
print("Try to build OLED_OLED")
canvas = canvas.Canvas()
welcome_time_count = 0
udpate_count = 0
starting_time_count = 0
ground_time_count = 0

# battery = battery.Battery()
# buttons = buttons.Buttons()

def update(t):          # UI tasks controller
    # battery.read_vol()  # read the battery voltage
    # buttons.check(t)    # check the buttons
    _check_shutter_state_() # check working state and assign handler
    _check_oled_()      # check if OLED needs update

def _check_oled_():# check if we need to update the OLED

    if vram.previous_state != vram.shutter_state:
        vram.previous_state = vram.shutter_state
        vram.info = vram.shutter_state
        canvas.update(vram.info)
    if vram.oled_need_update == "yes":
        vram.oled_need_update = "no"
        canvas.update(vram.info)

def _check_shutter_state_():
    if vram.shutter_state == "welcome":
        _welcome_()
    elif vram.shutter_state == "idle":
        _idle_()
    elif vram.shutter_state == "starting":
        _starting_()
    elif vram.shutter_state == "recording":
        _recording_()
    elif vram.shutter_state == "stopping":
        _stopping_()
    elif vram.shutter_state == "battery":
        _battery_()
    elif vram.shutter_state == "menu_internet":
        _menu_internet_() 
    elif vram.shutter_state == "menu_ota_source":
        _menu_ota_source_()
    elif vram.shutter_state == "menu_ota_channel":
        _menu_ota_channel_()
    elif vram.shutter_state == "menu_ota_check":
        _menu_ota_check_()
    elif vram.shutter_state == "menu_camera_protocol":
        _menu_camera_protocol_()
    elif vram.shutter_state == "menu_reboot_hint":
        _menu_reboot_hint_()
    elif vram.shutter_state == "menu_device_mode":
        _menu_device_mode_()
    elif vram.shutter_state == "menu_inject_mode":
        _menu_inject_mode_()
    else:
        print("Unknown UI state")

def _welcome_():
    _ignore_buttons_()
    global welcome_time_count
    # welcome auto switch
    if welcome_time_count <= 2500:
        welcome_time_count = welcome_time_count + 5
    else:
        vram.shutter_state = "idle"

def _idle_():

    # enter to start recording if in master or master/slave mode
    if vram.button_enter == "pressed":
        vram.button_enter = "released"
        _rec_enter_()

    ## page to battery menu
    if vram.button_page == "pressed":
        vram.button_page = "released"
        vram.shutter_state = "battery"

def _starting_():
    _ignore_buttons_()
    global ground_time_count
    if vram.camera_protocol == "MMTRY GND":
        if ground_time_count <1000:
            ground_time_count = ground_time_count + 5
        else:
            camera.Momentary_ground().momentary_ground(1)
            vram.shutter_state = "recording"
            vram.arm_state = "arm"
            ground_time_count = 0
    elif vram.camera_protocol == "Sony MTP":
        if ground_time_count <1000:
            ground_time_count = ground_time_count + 5
        elif ground_time_count == 1000:
            camera.Sony_multi().rec_press()
            print("called rec press")
            ground_time_count = ground_time_count + 5
        elif ground_time_count < 2000 and ground_time_count > 1000:
            ground_time_count = ground_time_count + 5
        else:
            camera.Sony_multi().rec_release()
            print("called rec release")
            ground_time_count = 0

    # starting timeout
    global starting_time_count
    if starting_time_count <= 5000:
        starting_time_count = starting_time_count + 5
    elif ((starting_time_count > 5000) & (starting_time_count <= 10000)):
        starting_time_count = starting_time_count + 5
        vram.info = "starting_timeout"
    elif starting_time_count > 10000:
        starting_time_count = 0
        vram.shutter_state = "idle"
        vram.info = vram.shutter_state

def _recording_():
    global starting_time_count
    starting_time_count = 0
    
    # enter to stop recording if in master or master/slave mode
    if vram.button_enter == "pressed":
        vram.button_enter = "released"
        _rec_enter_()
    # page cicle between rec_battery and recording
    if vram.button_page == "pressed":
        vram.button_page = "released"
        _rec_page_()

def _stopping_():
    _ignore_buttons_()
    global ground_time_count
    if vram.camera_protocol == "MMTRY GND":
        if ground_time_count <1000:
            ground_time_count = ground_time_count + 5
        else:
            camera.Momentary_ground().momentary_ground(1)
            vram.shutter_state = "idle"
            vram.arm_state = "disarm"
            ground_time_count = 0
    elif vram.camera_protocol == "Sony MTP":
        if ground_time_count <1000:
            ground_time_count = ground_time_count + 5
        elif ground_time_count == 1000:
            camera.Sony_multi().rec_press()
            print("called rec press")
            ground_time_count = ground_time_count + 5
        elif ground_time_count < 2000 and ground_time_count > 1000:
            ground_time_count = ground_time_count + 5
        else:
            camera.Sony_multi().rec_release()
            print("called rec release")
            ground_time_count = 0
    
        # starting timeout
    global starting_time_count
    if starting_time_count <= 5000:
        starting_time_count = starting_time_count + 5
    elif ((starting_time_count > 5000) & (starting_time_count <= 10000)):
        starting_time_count = starting_time_count + 5
        vram.info = "starting_timeout"
    elif starting_time_count > 10000:
        starting_time_count = 0
        vram.shutter_state = "idle"
        vram.info = vram.shutter_state

def _battery_():

    global udpate_count
    if udpate_count >=5000:
        udpate_count = 0
        vram.oled_need_update = "yes"
    else:
        udpate_count = udpate_count +5

    # page to camera protocol menu
    if vram.button_page == "pressed":
        vram.button_page = "released"
        vram.shutter_state = "menu_camera_protocol"
        vram.oled_need_update = "yes"
    
    # enter to hidden wlan mode menu
    if vram.button_enter == "pressed":
        vram.button_enter = "released"       
        vram.shutter_state = "menu_internet"
        vram.oled_need_update = "yes"

def _menu_internet_():

    # enter to set wlan up or down
    if vram.button_enter == "pressed":
        vram.button_enter = "released"
        if vram.wlan_state == "DISCONNECTED":
            wlan.up()
            vram.oled_need_update = "yes"
        else:
            wlan.down()
            vram.oled_need_update = "yes"

    ## page button
    if vram.button_page == "pressed":
        vram.button_page = "released"
        if vram.wlan_state == "CONNECTED":
            vram.shutter_state = "menu_ota_source"
        else:
            vram.shutter_state = "battery"

def _menu_ota_source_():

    # enter to set wlan up or down
    if vram.button_enter == "pressed":
        vram.button_enter = "released"
        vram.ota_source = vram.next(vram.ota_source_range, vram.ota_source)
        vram.oled_need_update = "yes"
        settings.update()

    ## page to ota channel menu
    if vram.button_page == "pressed":
        vram.button_page = "released"
        vram.shutter_state = "menu_ota_channel"

def _menu_ota_channel_():

    # enter to set ota channel
    if vram.button_enter == "pressed":
        vram.button_enter = "released"
        vram.ota_channel = vram.next(vram.ota_channel_range, vram.ota_channel)
        vram.oled_need_update = "yes"
        settings.update()
        print(vram.ota_channel)

    ## page to back to battery menu
    if vram.button_page == "pressed":
        vram.button_page = "released"
        vram.shutter_state = "menu_ota_check"

def _menu_ota_check_():

    # enter to check ota
    if vram.button_enter == "pressed":
        vram.button_enter = "released"
        # vram.info = "menu_ota_check_hint"
        ota.check()
        vram.oled_need_update = "yes"
    
    ## page to back to battery menu
    if vram.button_page == "pressed":
        vram.button_page = "released"
        vram.shutter_state = "battery"


def _menu_camera_protocol_():

    # enter to set camera protocol
    if vram.button_enter == "pressed":
        vram.button_enter = "released"
        vram.camera_protocol = vram.next(vram.camera_protocol_range, vram.camera_protocol)
        vram.update_camera_preset()
        vram.shutter_state = "menu_reboot_hint"
        settings.update()

    # page to device mode
    if vram.button_page == "pressed":
        vram.button_page = "released"
        vram.shutter_state = "menu_device_mode"

def _menu_reboot_hint_():
    
    if (vram.button_enter == "pressed") or (vram.button_page == "pressed"):
        vram.button_enter = "released"
        vram.button_page = "released"
        vram.shutter_state = "menu_camera_protocol"

def _menu_device_mode_():

    # enter to set device mode
    if vram.button_enter == "pressed":
        vram.button_enter = "released"
        vram.device_mode = vram.next(vram.device_mode_range, vram.device_mode)
        vram.oled_need_update = "yes"
        settings.update()

    # page to inject mode menu
    if vram.button_page == "pressed":
        vram.button_page = "released"       
        vram.shutter_state = "menu_inject_mode"

def _menu_inject_mode_():

    # enter to set inject mode
    if vram.button_enter == "pressed":
        vram.button_enter = "released"
        vram.inject_mode = vram.next(vram.inject_mode_range, vram.inject_mode)
        vram.oled_need_update = "yes"
        settings.update()

    ## page to save and back to idle
    if vram.button_page == "pressed":
        vram.button_page = "released"
        vram.shutter_state = "idle"

def _rec_enter_():
    if (vram.device_mode == "MASTER/SLAVE") & (vram.camera_protocol == "Sony MTP"):
        if vram.shutter_state == "idle":
            vram.shutter_state = "starting"
        elif vram.shutter_state == "recording":
            vram.shutter_state = "stopping"
    
    elif vram.device_mode == "MASTER":

        if vram.camera_protocol == "MMTRY GND":
            if vram.shutter_state == "idle":
                vram.shutter_state = "starting"
                camera.Momentary_ground().momentary_ground(0)
            elif vram.shutter_state == "recording":
                vram.shutter_state = "stopping"
                camera.Momentary_ground().momentary_ground(0)


        elif vram.camera_protocol == "3V3 Schmitt":
            if vram.shutter_state == "idle":
                vram.shutter_state = "recording"
                camera.Schmitt_3v3().toggle_cc_voltage_level()
                vram.arm_state = "arm"
            elif vram.shutter_state == "recording":
                vram.shutter_state = "idle"
                camera.Schmitt_3v3().toggle_cc_voltage_level()
                vram.arm_state = "disarm"

        elif vram.camera_protocol == "NO":
            if vram.shutter_state == "idle":
                vram.shutter_state = "recording"
                vram.arm_state = "arm"
            elif vram.shutter_state == "recording":
                vram.shutter_state = "idle"
                vram.arm_state = "disarm"

def _rec_page_():
    if vram.info == "recording":
        vram.info = "battery"
        vram.oled_need_update = "yes"
    elif vram.info == "battery":
        vram.info = "recording"
        vram.oled_need_update = "yes"

def _ignore_buttons_():    
    # enter do nonthing
    if vram.button_enter == "pressed":
        vram.button_enter = "released"
    
    # page do nonthing
    if vram.button_page == "pressed":
        vram.button_page = "released"
