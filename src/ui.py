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
import canvas, vram, json, settings, camera, ota, peripherals, time
import wlan

class UI_Logic:
    def __init__(self):
        print(str(time.ticks_us()) + " [Create] UI logic object")
        self.ota = ota.OTA()
        self.canvas = canvas.Canvas()
        self.buttons = peripherals.Buttons()
        self.battery = peripherals.Battery()
        self.welcome_time_count = 0
        self.udpate_count = 0
        self.starting_time_count = 0
        self.ground_time_count = 0
        if vram.camera_protocol == "NO":
            self.camera = camera.No_Cam()
        elif vram.camera_protocol == "Sony MTP":
            self.camera = camera.Sony_multi()
        elif vram.camera_protocol == "LANC":
            self.camera = camera.LANC()
        elif vram.camera_protocol == "ZCAM UART":
            self.camera = camera.ZCAM_UART()
        elif vram.camera_protocol == "MMTRY GND":
            self.camera = camera.Momentary_ground()
        elif vram.camera_protocol == "3V3 Schmitt":
            self.camera = camera.Schmitt_3v3()
        print(str(time.ticks_us()) + " [  OK  ] UI logic object")

    def show_sub(self, i):
        self.canvas.show_sub(i)

    def update(self, t):          # UI tasks controller
        # battery.read_vol()  # read the battery voltage
        # buttons.check(t)    # check the buttons
        self._check_shutter_state_() # check working state and assign handler
        self._check_oled_()      # check if OLED needs update

    def _check_oled_(self):# check if we need to update the OLED

        if vram.previous_state != vram.shutter_state:
            vram.previous_state = vram.shutter_state
            vram.info = vram.shutter_state
            self.canvas.update(vram.info)
        if vram.oled_need_update == "yes":
            vram.oled_need_update = "no"
            self.canvas.update(vram.info)

    def _check_shutter_state_(self):
        if vram.shutter_state == "welcome":
            self._welcome_()
        elif vram.shutter_state == "idle":
            self._idle_()
        elif vram.shutter_state == "starting":
            self._starting_()
        elif vram.shutter_state == "recording":
            self._recording_()
        elif vram.shutter_state == "stopping":
            self._stopping_()
        elif vram.shutter_state == "battery":
            self._battery_()
        elif vram.shutter_state == "menu_internet":
            self._menu_internet_() 
        elif vram.shutter_state == "menu_ota_source":
            self._menu_ota_source_()
        elif vram.shutter_state == "menu_ota_channel":
            self._menu_ota_channel_()
        elif vram.shutter_state == "menu_ota_check":
            self._menu_ota_check_()
        elif vram.shutter_state == "menu_camera_protocol":
            self._menu_camera_protocol_()
        elif vram.shutter_state == "menu_reboot_hint":
            self._menu_reboot_hint_()
        elif vram.shutter_state == "menu_device_mode":
            self._menu_device_mode_()
        elif vram.shutter_state == "menu_inject_mode":
            self._menu_inject_mode_()
        elif vram.shutter_state == "menu_erase_blackbox":
            self._menu_erase_blackbox_()
        else:
            print("Unknown UI state")

    def _welcome_(self):
        self._ignore_buttons_()
        # welcome auto switch
        if self.welcome_time_count <= 2500:
            self.welcome_time_count += 5
        else:
            vram.shutter_state = "idle"

    def _idle_(self):

        # enter to start recording if in master or master/slave mode
        if self.buttons.state[2] == "SHORT":
            self.buttons.state[2] = "RLS"
            if vram.device_mode == "MASTER" or vram.device_mode == "MASTER/SLAVE":
                vram.shutter_state = "starting"
                self.camera.rec()
            elif vram.device_mode == "TEST":
                self.camera.set_mode()

        ## page to battery menu
        if self.buttons.state[1] == "SHORT":
            self.buttons.state[1] = "RLS"
            vram.shutter_state = "battery"

    def _starting_(self):
        self._ignore_buttons_()
        self.camera.rec()

        # starting timeout
        if self.starting_time_count <= 5000:
            self.starting_time_count += 5
        elif ((self.starting_time_count > 5000) & (self.starting_time_count <= 10000)):
            self.starting_time_count += 5
            vram.info = "starting_timeout"
        elif self.starting_time_count > 10000:
            self.starting_time_count = 0
            vram.shutter_state = "idle"
            vram.info = vram.shutter_state
            self.camera.timeout()

    def _recording_(self):
        self.starting_time_count = 0
        
        # enter to stop recording if in master or master/slave mode
        if self.buttons.state[2] == "SHORT":
            self.buttons.state[2] = "RLS"
            if vram.device_mode == "MASTER" or vram.device_mode == "MASTER/SLAVE":
                vram.shutter_state = "stopping"
                self.camera.rec()
        # page cicle between rec_battery and recording
        if self.buttons.state[1] == "SHORT":
            self.buttons.state[1] = "RLS"
            self._rec_page_()

    def _stopping_(self):
        self._ignore_buttons_()
        self.camera.rec()
        
        # stopping timeout
        if self.starting_time_count <= 5000:
            self.starting_time_count += 5
        elif ((self.starting_time_count > 5000) & (self.starting_time_count <= 10000)):
            self.starting_time_count += 5
            vram.info = "starting_timeout"
        elif self.starting_time_count > 10000:
            self.starting_time_count = 0
            vram.shutter_state = "idle"
            vram.info = vram.shutter_state
            self.camera.timeout()

    def _battery_(self):

        if self.udpate_count >=5000:
            self.udpate_count = 0
            vram.oled_need_update = "yes"
        else:
            self.udpate_count += 5

        # page to camera protocol menu
        if self.buttons.state[1] == "SHORT":
            self.buttons.state[1] = "RLS"
            vram.shutter_state = "menu_camera_protocol"
            vram.oled_need_update = "yes"

        # enter to hidden wlan mode menu
        if self.buttons.state[2] == "SHORT":
            self.buttons.state[2] = "RLS"
            vram.shutter_state = "menu_internet"
            vram.oled_need_update = "yes"

    def _menu_internet_(self):

        # self.wlan = wlan.WIFI()
        # enter to set wlan up or down
        if self.buttons.state[2] == "SHORT":
            self.buttons.state[2] = "RLS"
            if vram.wlan_state == "DISCONNECTED":
                wlan.up()
                vram.oled_need_update = "yes"
            else:
                wlan.down()
                vram.oled_need_update = "yes"

        ## page button
        if self.buttons.state[1] == "SHORT":
            self.buttons.state[1] = "RLS"
            if vram.wlan_state == "CONNECTED":
                vram.shutter_state = "menu_ota_source"
            else:
                vram.shutter_state = "battery"

    def _menu_ota_source_(self):

        # enter to set wlan up or down
        if self.buttons.state[2] == "SHORT":
            self.buttons.state[2] = "RLS"
            vram.ota_source = vram.next(vram.ota_source_range, vram.ota_source)
            vram.oled_need_update = "yes"
            settings.update()

        ## page to ota channel menu
        if self.buttons.state[1] == "SHORT":
            self.buttons.state[1] = "RLS"
            vram.shutter_state = "menu_ota_channel"

    def _menu_ota_channel_(self):

        # enter to set ota channel
        if self.buttons.state[2] == "SHORT":
            self.buttons.state[2] = "RLS"
            vram.ota_channel = vram.next(vram.ota_channel_range, vram.ota_channel)
            vram.oled_need_update = "yes"
            settings.update()
            print(vram.ota_channel)

        ## page to back to battery menu
        if self.buttons.state[1] == "SHORT":
            self.buttons.state[1] = "RLS"
            vram.shutter_state = "menu_ota_check"

    def _menu_ota_check_(self):

        # enter to check ota
        if self.buttons.state[2] == "SHORT":
            self.buttons.state[2] = "RLS"
            # vram.info = "menu_ota_check_hint"
            self.ota.check()
            vram.oled_need_update = "yes"
        
        ## page to back to battery menu
        if self.buttons.state[1] == "SHORT":
            self.buttons.state[1] = "RLS"
            vram.shutter_state = "battery"

    def _menu_camera_protocol_(self):

        # enter to set camera protocol
        if self.buttons.state[2] == "SHORT":
            self.buttons.state[2] = "RLS"
            vram.camera_protocol = vram.next(vram.camera_protocol_range, vram.camera_protocol)
            vram.update_camera_preset()
            vram.shutter_state = "menu_reboot_hint"
            settings.update()

        # page to device mode
        if self.buttons.state[1] == "SHORT":
            self.buttons.state[1] = "RLS"
            vram.shutter_state = "menu_device_mode"

    def _menu_reboot_hint_(self):
        
        if (self.buttons.state[2] == "SHORT") or (self.buttons.state[1] == "SHORT"):
            self.buttons.state[2] = "RLS"
            self.buttons.state[1] = "RLS"
            vram.shutter_state = "menu_camera_protocol"

    def _menu_device_mode_(self):

        # enter to set device mode
        if self.buttons.state[2] == "SHORT":
            self.buttons.state[2] = "RLS"
            vram.device_mode = vram.next(vram.device_mode_range, vram.device_mode)
            vram.oled_need_update = "yes"
            settings.update()

        # page to inject mode menu
        if self.buttons.state[1] == "SHORT":
            self.buttons.state[1] = "RLS"
            vram.shutter_state = "menu_inject_mode"

    def _menu_inject_mode_(self):

        # enter to set inject mode
        if self.buttons.state[2] == "SHORT":
            self.buttons.state[2] = "RLS"
            vram.inject_mode = vram.next(vram.inject_mode_range, vram.inject_mode)
            vram.oled_need_update = "yes"
            settings.update()

        ## page to erase menu
        if self.buttons.state[1] == "SHORT":
            self.buttons.state[1] = "RLS"
            vram.shutter_state = "menu_erase_blackbox"

    def _menu_erase_blackbox_(self):

        # enter to erase blackbox
        if self.buttons.state[2] == "SHORT":
            self.buttons.state[2] = "RLS"
            if vram.erase_flag == False:
                vram.erase_flag = True
                print("erasing...")
            else:
                vram.erase_flag = False
                print("stop erase...")
            vram.oled_need_update = "yes"
            # self.erase.erase()

        ## page to save and back to idle
        if self.buttons.state[1] == "SHORT":
            self.buttons.state[1] = "RLS"
            vram.shutter_state = "idle"

    def _rec_page_(self):
        if vram.info == "recording":
            vram.info = "battery"
            vram.oled_need_update = "yes"
        elif vram.info == "battery":
            vram.info = "recording"
            vram.oled_need_update = "yes"

    def _ignore_buttons_(self):
        # enter do nonthing
        if self.buttons.state[2] == "SHORT":
            self.buttons.state[2] = "RLS"

        # page do nonthing
        if self.buttons.state[1] == "SHORT":
            self.buttons.state[1] = "RLS"
