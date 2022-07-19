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
import uasyncio as asyncio
import vram, settings, time
import gui.core.canvas as canvas
import gui.settings as settings
import hal.ahal as ahal
import hal.shal as shal
from machine import Timer

class Logic:
    def __init__(self):
        print(str(time.ticks_us()) + " [ INIT ] UI logic object")
        self.update_count = 0
        self.settings = settings.UserSettings()
        self.sync_hal = shal.SyncPeripherals()
        self.canvas = canvas.init_canvas(self.sync_hal.screen)
        self.async_hal = ahal.AsnycPeripherals(camera = vram.camera_protocol)
        print(str(time.ticks_us()) + " [ SYNC ] UI logic HAL")
        self.init_sync_hal()
        print(str(time.ticks_us()) + " [ ASYNC] UI logic HAL")
        self.init_async_hal()

    def init_sync_hal(self):
        timer0 = Timer(0)
        timer0.init(period=5, mode=Timer.PERIODIC, callback=self.sync_hal.scheduler)

    def init_async_hal(self):
        loop = asyncio.get_event_loop()
        loop.create_task(self.sync_hal.fc_link.uart_handler())
        loop.create_task(self.async_hal.buttons.checker('PAGE UP'))
        loop.create_task(self.async_hal.buttons.checker('PAGE DOWN'))
        loop.create_task(self.async_hal.buttons.checker('ENTER'))
        loop.create_task(self.async_hal.battery.adc_handler())
        loop.create_task(self.update())
        if self.async_hal.camera.task_mode == "THREAD":
            import _thread
            import machine
            machine.freq(240000000)
            _thread.start_new_thread(self.async_hal.camera.uart_handler, ())
        elif self.async_hal.camera.task_mode == "ASYNC":
            loop.create_task(self.async_hal.camera.uart_handler())
        loop.run_forever()

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
        self.update_count += 5
        self.bind_btn(0, "SHORT", "BLANK", 0, 0, 0)
        self.bind_btn(1, "LONG",  "BLANK", 0, 0, 0)
        self.bind_btn(1, "SHORT", "BLANK", 0, 0, 0)
        self.bind_btn(1, "LONG",  "BLANK", 0, 0, 0)
        self.bind_btn(2, "SHORT", "BLANK", 0, 0, 0)
        self.bind_btn(2, "LONG",  "BLANK", 0, 0, 0)
        # welcome auto switch
        if self.update_count == 2500:
            self.update_count = 0
            vram.shutter_state = "home"

    def home(self):
        self.bind_btn(0, "SHORT", "INFO", 0, 0, "battery_info")
        self.bind_btn(0, "LONG",  "MENU", 0, 0, "menu")
        self.bind_btn(1, "SHORT", "SHUTTER", 0, 0, 0)
        self.bind_btn(1, "LONG",  "BLANK", 0, 0, 0)
        self.bind_btn(2, "SHORT", "INFO", 0, 0, "battery_info")
        self.bind_btn(2, "LONG",  "MENU", 0, 0, "menu")

    def starting(self):
        self.update_count += 5
        self.bind_btn(0, "SHORT", "BLANK", 0, 0, 0)
        self.bind_btn(0, "LONG",  "BLANK", 0, 0, 0)
        self.bind_btn(1, "SHORT", "BLANK", 0, 0, 0)
        self.bind_btn(1, "LONG",  "BLANK", 0, 0, 0)
        self.bind_btn(2, "SHORT", "BLANK", 0, 0, 0)
        self.bind_btn(2, "LONG",  "BLANK", 0, 0, 0)

        # starting timeout
        if self.update_count < 5000:
            self.async_hal.camera.rec()
        elif self.update_count == 5000:
            vram.info = "hint"
            vram.sub_hint = "STARTING_TIMEOUT"
            vram.oled_need_update = "yes"
        elif self.update_count == 10000:
            self.update_count = 0
            vram.shutter_state = "home"
            vram.sub_state = "HOME"
            vram.info = vram.shutter_state
            vram.oled_need_update = "yes"
            self.async_hal.camera.timeout()

    def recording(self):
        self.update_count = 0
        self.bind_btn(0, "SHORT", "INFO", 0, 0, 0)
        self.bind_btn(0, "LONG",  "BLANK", 0, 0, 0)
        self.bind_btn(1, "SHORT", "SHUTTER", 0, 0, 0)
        self.bind_btn(1, "LONG",  "BLANK", 0, 0, 0)
        self.bind_btn(2, "SHORT", "INFO",0, 0, 0)
        self.bind_btn(2, "LONG",  "BLANK", 0, 0, 0)

    def stopping(self):
        self.update_count += 5
        self.bind_btn(0, "SHORT", "BLANK", 0, 0, 0)
        self.bind_btn(0, "LONG",  "BLANK", 0, 0, 0)
        self.bind_btn(1, "SHORT", "BLANK", 0, 0, 0)
        self.bind_btn(1, "LONG",  "BLANK", 0, 0, 0)
        self.bind_btn(2, "SHORT", "BLANK", 0, 0, 0)
        self.bind_btn(2, "LONG",  "BLANK", 0, 0, 0)

        # stopping timeout
        if self.update_count < 5000:
            self.async_hal.camera.rec()
        elif self.update_count == 5000:
            vram.info = "hint"
            vram.sub_hint = "STARTING_TIMEOUT"
            vram.oled_need_update = "yes"
        elif self.update_count == 10000:
            self.update_count = 0
            vram.shutter_state = "home"
            vram.sub_state = "HOME"
            vram.info = vram.shutter_state
            vram.oled_need_update = "yes"
            self.async_hal.camera.timeout()

    def info_battery(self):
        self.update_count += 5
        if self.update_count ==5000:
            self.update_count = 0
            vram.oled_need_update = "yes"

        # self.bind_btn(1, "SHORT", "MENU", 0, 0, "menu_internet")
        self.bind_btn(0, "SHORT", "MENU", 0, 0, "home")
        self.bind_btn(0, "LONG",  "BLANK", 0, 0, 0)
        self.bind_btn(1, "SHORT", "BLANK", 0, 0, 0)
        self.bind_btn(1, "LONG",  "BLANK", 0, 0, 0)
        self.bind_btn(2, "SHORT", "MENU", 0, 0, "home")
        self.bind_btn(2, "LONG",  "BLANK", 0, 0, 0)

    def menu_camera_protocol(self):
        self.bind_btn(0, "SHORT", "SUBMENU", 0, 0, "erase_blackbox")
        self.bind_btn(0, "LONG",  "MENU", 0, 0, "home")
        self.bind_btn(1, "SHORT", "SETTING", vram.camera_protocol, vram.camera_protocol_range, 0)
        self.bind_btn(1, "LONG",  "BLANK", 0, 0, 0)
        self.bind_btn(2, "SHORT", "SUBMENU", 0, 0, "device_mode")
        self.bind_btn(2, "LONG",  "MENU", 0, 0, "home")

    def menu_device_mode(self):
        self.bind_btn(0, "SHORT", "SUBMENU", 0, 0, "camera_protocol")
        self.bind_btn(0, "LONG",  "MENU", 0, 0, "home")
        self.bind_btn(1, "SHORT", "SETTING", vram.device_mode, vram.device_mode_range, 0)
        self.bind_btn(1, "LONG",  "BLANK", 0, 0, 0)
        self.bind_btn(2, "SHORT", "SUBMENU", 0, 0, "inject_mode")
        self.bind_btn(2, "LONG",  "MENU", 0, 0, "home")

    def menu_inject_mode(self):
        self.bind_btn(0, "SHORT", "SUBMENU", 0, 0, "device_mode")
        self.bind_btn(0, "LONG",  "MENU", 0, 0, "home")
        self.bind_btn(1, "SHORT", "SETTING", vram.inject_mode, vram.inject_mode_range, 0)
        self.bind_btn(1, "LONG",  "BLANK", 0, 0, 0)
        self.bind_btn(2, "SHORT", "SUBMENU", 0, 0, "erase_blackbox")
        self.bind_btn(2, "LONG",  "MENU", 0, 0, "home")

    def menu_erase_blackbox(self):
        self.bind_btn(0, "SHORT", "SUBMENU", 0, 0, "inject_mode")
        self.bind_btn(0, "LONG",  "MENU", 0, 0, "home")
        self.bind_btn(1, "SHORT", "FC", 0,0,0)
        self.bind_btn(1, "LONG",  "BLANK", 0, 0, 0)
        self.bind_btn(2, "SHORT", "SUBMENU", 0, 0, "camera_protocol")
        self.bind_btn(2, "LONG",  "MENU", 0, 0, "home")

    def hint_reboot(self):
        self.bind_btn(0, "SHORT", "SUBMENU", 0, 0, "camera_protocol")
        self.bind_btn(0, "LONG",  "MENU", 0, 0, "home")
        self.bind_btn(1, "SHORT", "SUBMENU", 0, 0, "camera_protocol")
        self.bind_btn(1, "LONG",  "BLANK", 0, 0, 0)
        self.bind_btn(2, "SHORT", "SUBMENU", 0, 0, "camera_protocol")
        self.bind_btn(2, "LONG",  "MENU", 0, 0, "home")

    def menu_root(self):
        self.bind_btn(0, "SHORT", "SUBMENU", 0, 0, "erase_blackbox")
        self.bind_btn(0, "LONG",  "MENU", 0, 0, "home")
        self.bind_btn(1, "SHORT", "BLANK", 0,0,0)
        self.bind_btn(1, "LONG",  "BLANK", 0, 0, 0)
        self.bind_btn(2, "SHORT", "SUBMENU", 0, 0, "camera_protocol")
        self.bind_btn(2, "LONG",  "MENU", 0, 0, "home")

    def bind_btn(self, button, event, dest, setting, setting_range, next_state):
        if self.async_hal.buttons.state[button] == event:
            self.async_hal.buttons.state[button] = "RLS"
            if dest == 'MENU':
                vram.shutter_state = next_state
            elif dest == 'SUBMENU':
                vram.shutter_state = 'menu'
                vram.sub_menu = next_state
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
                self.settings.update()
            elif dest == 'FC':
                if vram.sub_menu == "erase_blackbox":
                    if vram.erase_flag == False:
                        vram.erase_flag = True
                    else:
                        vram.erase_flag = False
            elif dest == 'SHUTTER':
                if vram.sub_state == "internet":
                    import internet.wlan as wlan
                    if vram.wlan_state == "DISCONNECTED":
                        wlan.up()
                    else:
                        wlan.down()
                elif vram.sub_state == "ota_check":
                    import internet.ota as ota
                    self.ota = ota.OTA()
                    self.ota.check()
                elif vram.sub_state == "HOME":
                    if vram.device_mode == "MASTER" or vram.device_mode == "MASTER/SLAVE":
                        vram.sub_state = "STARTING"
                    elif vram.device_mode == "TEST":
                        self.async_hal.camera.set_mode()
                elif vram.sub_state == "RECORDING":
                    if vram.device_mode == "MASTER" or vram.device_mode == "MASTER/SLAVE":
                        vram.sub_state = "STOPPING"
            vram.oled_need_update = "yes"
