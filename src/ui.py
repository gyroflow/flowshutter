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
import gui.canvas as canvas
import uasyncio as asyncio
import vram, json, settings, camera, ota, peripherals, time

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
        elif vram.camera_protocol == "SONY MTP":
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

    async def update(self):          # UI tasks controller
        print(str(time.ticks_us()) + " [  OK  ] Async UI state machine")
        while True:
            self.check_shutter_state() # check working state and assign handler
            self.check_oled()      # check if OLED needs update
            await asyncio.sleep_ms(5)

    def check_oled(self):# check if we need to update the OLED
        if vram.previous_state != vram.shutter_state:
            vram.previous_state = vram.shutter_state
            vram.info = vram.shutter_state
            self.canvas.update(vram.info,vram.sub_state,vram.sub_menu,vram.sub_hint)
        if vram.oled_need_update == "yes":
            vram.oled_need_update = "no"
            self.canvas.update(vram.info,vram.sub_state,vram.sub_menu,vram.sub_hint)

    def check_shutter_state(self):
        if vram.shutter_state == "welcome":
            self.welcome()
        elif vram.shutter_state == "home":
            if vram.sub_state == "HOME":
                self.home()
            elif vram.sub_state == "STARTING":
                self.starting()
            elif vram.sub_state == "RECORDING":
                self.recording()
            elif vram.sub_state == "STOPPING":
                self.stopping()
        elif vram.shutter_state == "battery_info":
            self.info_battery()
        elif vram.shutter_state == "hint":
            if vram.sub_hint == "REBOOT":
                self.hint_reboot()
        elif vram.shutter_state == "menu":
            if vram.sub_menu == "menu_root":
                self.menu_root()
            elif vram.sub_menu == "camera_protocol":
                self.menu_camera_protocol()
            elif vram.sub_menu == "device_mode":
                self.menu_device_mode()
            elif vram.sub_menu == "inject_mode":
                self.menu_inject_mode()
            elif vram.sub_menu == "erase_blackbox":
                self.menu_erase_blackbox()
            elif vram.sub_menu == "internet":
                self.menu_internet()
            elif vram.sub_menu == "ota_source":
                self.menu_ota_source()
            elif vram.sub_menu == "ota_channel":
                self.menu_ota_channel()
            elif vram.sub_menu == "ota_check":
                self.menu_ota_check()
            else:
                print('Unkown menu!' + vram.sub_menu)
        else:
            print("Unknown UI state")

    def welcome(self):
        self.bind_btn(1, "SHORT", "BLANK", 0, 0, 0)
        self.bind_btn(1, "LONG",  "BLANK", 0, 0, 0)
        self.bind_btn(2, "SHORT", "BLANK", 0, 0, 0)
        self.bind_btn(2, "LONG",  "BLANK", 0, 0, 0)
        # welcome auto switch
        if self.welcome_time_count <= 2500:
            self.welcome_time_count += 5
        else:
            vram.shutter_state = "home"

    def home(self):
        self.bind_btn(1, "SHORT", "FC", 0, 0, 0)
        self.bind_btn(1, "LONG",  "BLANK", 0, 0, 0)
        self.bind_btn(2, "SHORT", "INFO", 0, 0, "battery_info")
        self.bind_btn(2, "LONG",  "MENU", 0, 0, "menu")

    def starting(self):
        self.bind_btn(1, "SHORT", "BLANK", 0, 0, 0)
        self.bind_btn(1, "LONG",  "BLANK", 0, 0, 0)
        self.bind_btn(2, "SHORT", "BLANK", 0, 0, 0)
        self.bind_btn(2, "LONG",  "BLANK", 0, 0, 0)

        # starting timeout
        if self.starting_time_count < 5000:
            self.camera.rec()
            self.starting_time_count += 5
            # print(self.starting_time_count)
        elif self.starting_time_count == 5000:
            self.starting_time_count += 5
            vram.info = "hint"
            vram.sub_hint = "STARTING_TIMEOUT"
            vram.oled_need_update = "yes"
        elif ((self.starting_time_count > 5000) & (self.starting_time_count <= 10000)):
            self.starting_time_count += 5
        elif self.starting_time_count > 10000:
            self.starting_time_count = 0
            vram.shutter_state = "home"
            vram.sub_state = "HOME"
            vram.info = vram.shutter_state
            vram.oled_need_update = "yes"
            self.camera.timeout()

    def recording(self):
        self.starting_time_count = 0
        self.bind_btn(1, "SHORT", "FC", 0, 0, 0)
        self.bind_btn(1, "LONG",  "BLANK", 0, 0, 0)
        self.bind_btn(2, "SHORT", "INFO",0, 0, 0)
        self.bind_btn(2, "LONG",  "BLANK", 0, 0, 0)

    def stopping(self):
        self.bind_btn(1, "SHORT", "BLANK", 0, 0, 0)
        self.bind_btn(1, "LONG",  "BLANK", 0, 0, 0)
        self.bind_btn(2, "SHORT", "BLANK", 0, 0, 0)
        self.bind_btn(2, "LONG",  "BLANK", 0, 0, 0)

        # stopping timeout
        if self.starting_time_count < 5000:
            self.camera.rec()
            self.starting_time_count += 5
        elif self.starting_time_count == 5000:
            self.starting_time_count += 5
            vram.info = "hint"
            vram.sub_hint = "STARTING_TIMEOUT"
            vram.oled_need_update = "yes"
        elif ((self.starting_time_count > 5000) & (self.starting_time_count <= 10000)):
            self.starting_time_count += 5
        elif self.starting_time_count > 10000:
            self.starting_time_count = 0
            vram.shutter_state = "home"
            vram.sub_state = "HOME"
            vram.info = vram.shutter_state
            vram.oled_need_update = "yes"
            self.camera.timeout()

    def info_battery(self):
        if self.udpate_count >=5000:
            self.udpate_count = 0
            vram.oled_need_update = "yes"
        else:
            self.udpate_count += 5
        # self.bind_btn(1, "SHORT", "MENU", 0, 0, "menu_internet")
        self.bind_btn(1, "SHORT", "BLANK", 0, 0, 0)
        self.bind_btn(1, "LONG",  "BLANK", 0, 0, 0)
        self.bind_btn(2, "SHORT", "MENU", 0, 0, "home")
        self.bind_btn(2, "LONG",  "BLANK", 0, 0, 0)

    def menu_camera_protocol(self):
        self.bind_btn(1, "SHORT", "SETTING", vram.camera_protocol, vram.camera_protocol_range, 0)
        self.bind_btn(1, "LONG",  "BLANK", 0, 0, 0)
        self.bind_btn(2, "SHORT", "SUBMENU", 0, 0, "device_mode")
        self.bind_btn(2, "LONG",  "MENU", 0, 0, "home")

    def menu_device_mode(self):
        self.bind_btn(1, "SHORT", "SETTING", vram.device_mode, vram.device_mode_range, 0)
        self.bind_btn(1, "LONG",  "BLANK", 0, 0, 0)
        self.bind_btn(2, "SHORT", "SUBMENU", 0, 0, "inject_mode")
        self.bind_btn(2, "LONG",  "MENU", 0, 0, "home")

    def menu_inject_mode(self):
        self.bind_btn(1, "SHORT", "SETTING", vram.inject_mode, vram.inject_mode_range, 0)
        self.bind_btn(1, "LONG",  "BLANK", 0, 0, 0)
        self.bind_btn(2, "SHORT", "SUBMENU", 0, 0, "erase_blackbox")
        self.bind_btn(2, "LONG",  "MENU", 0, 0, "home")

    def menu_erase_blackbox(self):
        self.bind_btn(1, "SHORT", "FC", 0,0,0)
        self.bind_btn(1, "LONG",  "BLANK", 0, 0, 0)
        self.bind_btn(2, "SHORT", "SUBMENU", 0, 0, "camera_protocol")
        self.bind_btn(2, "LONG",  "MENU", 0, 0, "home")

    def hint_reboot(self):
        self.bind_btn(1, "SHORT", "SUBMENU", 0, 0, "camera_protocol")
        self.bind_btn(1, "LONG",  "BLANK", 0, 0, 0)
        self.bind_btn(2, "SHORT", "SUBMENU", 0, 0, "camera_protocol")
        self.bind_btn(2, "LONG",  "MENU", 0, 0, "home")

    def menu_root(self):
        self.bind_btn(1, "SHORT", "BLANK", 0,0,0)
        self.bind_btn(1, "LONG",  "BLANK", 0, 0, 0)
        self.bind_btn(2, "SHORT", "SUBMENU", 0, 0, "camera_protocol")
        self.bind_btn(2, "LONG",  "MENU", 0, 0, "home")

    def bind_btn(self, button, event, dest, setting, setting_range, next_state):
        if self.buttons.state[button] == event:
            self.buttons.state[button] = "RLS"
            if dest == 'MENU':
                vram.shutter_state = next_state
                vram.oled_need_update = "yes"
            elif dest == 'SUBMENU':
                vram.shutter_state = 'menu'
                vram.sub_menu = next_state
                vram.oled_need_update = "yes"
            elif dest == 'INFO':
                if vram.shutter_state == "recording":
                    if vram.info == "recording":
                        vram.info = "battery_info"
                    elif vram.info == "battery_info":
                        vram.info = "recording"
                elif vram.shutter_state == 'home':
                    if vram.info == "home":
                        vram.info = "battery_info"
                    elif vram.info == "battery_info":
                        vram.info = "home"
                vram.oled_need_update = "yes"
            elif dest == 'BLANK':
                pass
            elif dest == "SETTING":
                setting = vram.next(setting_range,setting)
                if vram.sub_menu == "device_mode":
                    vram.device_mode = setting
                elif vram.sub_menu == "inject_mode":
                    vram.inject_mode = setting
                elif vram.sub_menu == "camera_protocol":
                    vram.camera_protocol = setting
                    vram.update_camera_preset()
                    vram.shutter_state = 'hint'
                    vram.sub_hint = 'REBOOT'
                elif vram.sub_menu == "ota_source":
                    vram.ota_source = setting
                elif vram.sub_menu == "ota_channel":
                    vram.ota_channel = setting
                else:
                    print("Hey what's this?")
                vram.oled_need_update = "yes"
                settings.update()
            elif dest == 'FC':
                if vram.sub_state == "HOME":
                    if vram.device_mode == "MASTER" or vram.device_mode == "MASTER/SLAVE":
                        vram.sub_state = "STARTING"
                    elif vram.device_mode == "TEST":
                        self.camera.set_mode()
                elif vram.sub_state == "RECORDING":
                    if vram.device_mode == "MASTER" or vram.device_mode == "MASTER/SLAVE":
                        vram.sub_state = "STOPPING"
                elif vram.sub_menu == "erase_blackbox":
                    if vram.erase_flag == False:
                        vram.erase_flag = True
                    else:
                        vram.erase_flag = False
                vram.oled_need_update = "yes"
            elif dest == 'SHUTTER':
                if vram.sub_state == "internet":
                    import wlan
                    if vram.wlan_state == "DISCONNECTED":
                        wlan.up()
                        vram.oled_need_update = "yes"
                    else:
                        wlan.down()
                elif vram.sub_state == "ota_check":
                    self.ota.check()
                    vram.oled_need_update = "yes"
