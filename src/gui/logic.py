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
import time
import gui.core.canvas as canvas
import gui.settings as settings
import hal.ahal as ahal
import hal.shal as shal
from machine import Timer

class Logic:
    def __init__(self):
        print(str(time.ticks_us()) + " [ INIT ] UI logic object")
        self.init_variables()
        self.settings = settings.UserSettings()
        self.sync_hal = shal.SyncPeripherals()
        self.canvas = canvas.init_canvas(self.sync_hal.screen)
        self.async_hal = ahal.AsnycPeripherals(camera = self.settings.settings['camera_protocol'])
        print(str(time.ticks_us()) + " [ SYNC ] UI logic HAL")
        self.init_sync_hal()
        print(str(time.ticks_us()) + " [ ASYNC] UI logic HAL")
        self.init_async_hal()

    def init_variables(self):
        self.shutter_state = "home"
        self.sub_state = "WELCOME"
        self.sub_info = ''
        self.update_count = 0
        self.refresh = [False, False] # native flag, flag from camera
        self.prev_state = 'blank'
        self.substate_index = 0
        self.substate = ['HOME', 'STARTING', 'RECORDING', 'STOPPING']
        self.submenu_index = 0
        self.submenu = ['camera_protocol', 'device_mode', 'inject_mode', 'erase_blackbox']
        # self.submenu = ['camera_protocol', 'device_mode', 'inject_mode', 'erase_blackbox', 'internet', 'ota_source', 'ota_channel', 'ota_check', 'ota_update']

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

    def exchange_data(self):
        self.sync_hal.fc_link.inject_mode = self.settings.settings['inject_mode']
        self.canvas.settings = self.settings.settings
        self.async_hal.camera.oled_update_flag = False
        self.canvas.vol = self.async_hal.battery.vol

    def check_camera(self):
        self.sync_hal.fc_link.arm_state = self.async_hal.camera.state
        self.refresh[1] = self.async_hal.camera.oled_update_flag
        if self.async_hal.camera.state == True and (self.sub_state == "HOME" or self.sub_state == "STARTING"):
            self.sub_state = 'RECORDING'
        elif self.async_hal.camera.state == False and (self.sub_state == "RECORDING" or self.sub_state == "STOPPING"):
            self.sub_state = 'HOME'
        if self.async_hal.camera.notification != "":
            self.sub_info = self.async_hal.camera.notification

    async def update(self):          # UI tasks controller
        print(str(time.ticks_us()) + " [  OK  ] Async UI state machine")
        while True:
            self.check_shutter_state() # check working state and assign handler
            self.check_camera()
            self.check_oled()      # check if OLED needs update
            await asyncio.sleep_ms(5)

    def check_oled(self):# check if we need to update the OLED
        if self.prev_state != self.shutter_state:
            self.prev_state = self.shutter_state
            self.refresh[0] = True
        if self.refresh[0] or self.refresh[1]:
            self.refresh = [False, False]
            self.exchange_data()
            self.canvas.update(self.shutter_state,self.sub_state,self.submenu[self.submenu_index],self.sub_info)

    def check_shutter_state(self):
        if self.sub_info != '':
            if self.sub_info == 'REBOOT':
                self.info_reboot()
            elif self.sub_info == 'BATTERY':
                self.info_battery()
            elif self.sub_info == 'STARTING_TIMEOUT':
                self.info_starting_timeout()
            elif self.sub_info == 'SONY_MTP_ACK':
                self.info_sony_mtp_ack()
        elif self.shutter_state == "home":
            if self.sub_state == "WELCOME":
                self.welcome()
            elif self.sub_state == "HOME":
                self.home()
            elif self.sub_state == "STARTING":
                self.starting()
            elif self.sub_state == "RECORDING":
                self.recording()
            elif self.sub_state == "STOPPING":
                self.stopping()
        elif self.shutter_state == "menu":
            if self.submenu[self.submenu_index] == "menu_root":
                self.menu_root()
            elif self.submenu[self.submenu_index] == "camera_protocol":
                self.menu_camera_protocol()
            elif self.submenu[self.submenu_index] == "device_mode":
                self.menu_device_mode()
            elif self.submenu[self.submenu_index] == "inject_mode":
                self.menu_inject_mode()
            elif self.submenu[self.submenu_index] == "erase_blackbox":
                self.menu_erase_blackbox()
            elif self.submenu[self.submenu_index] == "internet":
                self.menu_internet()
            elif self.submenu[self.submenu_index] == "ota_source":
                self.menu_ota_source()
            elif self.submenu[self.submenu_index] == "ota_channel":
                self.menu_ota_channel()
            elif self.submenu[self.submenu_index] == "ota_check":
                self.menu_ota_check()
            else:
                print('Unkown menu!' + self.submenu[self.submenu_index])
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
            self.sub_state = "HOME"
            self.refresh[0] = True

    def home(self):
        self.bind_btn(0, "SHORT", "INFO", 0, 0, "BATTERY")
        self.bind_btn(0, "LONG",  "MENU", 0, 0, "menu")
        self.bind_btn(1, "SHORT", "SHUTTER", 0, 0, 0)
        self.bind_btn(1, "LONG",  "BLANK", 0, 0, 0)
        self.bind_btn(2, "SHORT", "INFO", 0, 0, "BATTERY")
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
            self.sub_info = "STARTING_TIMEOUT"
            self.refresh[0] = True

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
            self.sub_info = "STARTING_TIMEOUT"
            self.async_hal.camera.state = False
            self.sync_hal.fc_link.state = False
            self.refresh[0] = True

    def info_battery(self):
        self.update_count += 5
        if self.update_count ==5000:
            self.update_count = 0
            self.refresh[0] = True

        # self.bind_btn(1, "SHORT", "MENU", 0, 0, "menu_internet")
        self.bind_btn(0, "SHORT", "INFO",  0, 0, 0)
        self.bind_btn(0, "LONG",  "BLANK", 0, 0, 0)
        self.bind_btn(1, "SHORT", "BLANK", 0, 0, 0)
        self.bind_btn(1, "LONG",  "BLANK", 0, 0, 0)
        self.bind_btn(2, "SHORT", "INFO",  0, 0, 0)
        self.bind_btn(2, "LONG",  "BLANK", 0, 0, 0)

    def menu_camera_protocol(self):
        self.bind_btn(0, "SHORT", "SUBMENU", 0, 0, 3)
        self.bind_btn(0, "LONG",  "MENU", 0, 0, "home")
        self.bind_btn(1, "SHORT", "SETTING", self.settings.settings['camera_protocol'], self.settings.camera_protocol_range, 0)
        self.bind_btn(1, "LONG",  "BLANK", 0, 0, 0)
        self.bind_btn(2, "SHORT", "SUBMENU", 0, 0, 1)
        self.bind_btn(2, "LONG",  "MENU", 0, 0, "home")

    def menu_device_mode(self):
        self.bind_btn(0, "SHORT", "SUBMENU", 0, 0, 0)
        self.bind_btn(0, "LONG",  "MENU", 0, 0, "home")
        self.bind_btn(1, "SHORT", "SETTING", self.settings.settings['device_mode'], self.settings.device_mode_range, 0)
        self.bind_btn(1, "LONG",  "BLANK", 0, 0, 0)
        self.bind_btn(2, "SHORT", "SUBMENU", 0, 0, 2)
        self.bind_btn(2, "LONG",  "MENU", 0, 0, "home")

    def menu_inject_mode(self):
        self.bind_btn(0, "SHORT", "SUBMENU", 0, 0, 1)
        self.bind_btn(0, "LONG",  "MENU", 0, 0, "home")
        self.bind_btn(1, "SHORT", "SETTING", self.settings.settings['inject_mode'], self.settings.inject_mode_range, 0)
        self.bind_btn(1, "LONG",  "BLANK", 0, 0, 0)
        self.bind_btn(2, "SHORT", "SUBMENU", 0, 0, 3)
        self.bind_btn(2, "LONG",  "MENU", 0, 0, "home")

    def menu_erase_blackbox(self):
        self.bind_btn(0, "SHORT", "SUBMENU", 0, 0, 2)
        self.bind_btn(0, "LONG",  "MENU", 0, 0, "home")
        self.bind_btn(1, "SHORT", "FC", 0,0,0)
        self.bind_btn(1, "LONG",  "BLANK", 0, 0, 0)
        self.bind_btn(2, "SHORT", "SUBMENU", 0, 0, 0)
        self.bind_btn(2, "LONG",  "MENU", 0, 0, "home")

    def info_sony_mtp_ack(self):
        self.update_count += 5
        self.bind_btn(0, "SHORT", "BLANK", 0, 0, 0)
        self.bind_btn(0, "LONG",  "BLANK", 0, 0, 0)
        self.bind_btn(1, "SHORT", "BLANK", 0, 0, 0)
        self.bind_btn(1, "LONG",  "BLANK", 0, 0, 0)
        self.bind_btn(2, "SHORT", "BLANK", 0, 0, 0)
        self.bind_btn(2, "LONG",  "BLANK", 0, 0, 0)

        if self.update_count == 2000:
            self.update_count = 0
            self.async_hal.camera.notification = ''
            self.sub_info = ''
            self.refresh[0] = True

    def info_reboot(self):
        self.bind_btn(0, "SHORT", "INFO", 0, 0, 0)
        self.bind_btn(0, "LONG",  "INFO", 0, 0, 0)
        self.bind_btn(1, "SHORT", "INFO", 0, 0, 0)
        self.bind_btn(1, "LONG",  "INFO", 0, 0, 0)
        self.bind_btn(2, "SHORT", "INFO", 0, 0, 0)
        self.bind_btn(2, "LONG",  "INFO", 0, 0, 0)

    def info_starting_timeout(self):
        self.update_count += 5
        self.bind_btn(0, "SHORT", "BLANK", 0, 0, 0)
        self.bind_btn(0, "LONG",  "BLANK", 0, 0, 0)
        self.bind_btn(1, "SHORT", "BLANK", 0, 0, 0)
        self.bind_btn(1, "LONG",  "BLANK", 0, 0, 0)
        self.bind_btn(2, "SHORT", "BLANK", 0, 0, 0)
        self.bind_btn(2, "LONG",  "BLANK", 0, 0, 0)

        if self.update_count == 10000:
            self.update_count = 0
            self.sub_info = ''
            self.sub_state = "HOME"
            self.refresh[0] = True
            self.async_hal.camera.timeout()

    def menu_root(self):
        self.bind_btn(0, "SHORT", "SUBMENU", 0, 0, "erase_blackbox")
        self.bind_btn(0, "LONG",  "MENU", 0, 0, "home")
        self.bind_btn(1, "SHORT", "BLANK", 0,0,0)
        self.bind_btn(1, "LONG",  "BLANK", 0, 0, 0)
        self.bind_btn(2, "SHORT", "SUBMENU", 0, 0, "camera_protocol")
        self.bind_btn(2, "LONG",  "MENU", 0, 0, "home")

    def bind_btn(self, button, event, dest, setting, setting_range, new_state):
        if self.async_hal.buttons.state[button] == event:
            self.async_hal.buttons.state[button] = "RLS"
            if dest == 'MENU':
                self.shutter_state = new_state
            elif dest == 'SUBMENU':
                self.shutter_state = 'menu'
                self.submenu_index = new_state
            elif dest == 'INFO':
                if self.shutter_state == 'home':
                    if self.sub_state == "RECORDING" or self.sub_state == 'HOME':
                        if self.sub_info == "":
                            self.sub_info = "BATTERY"
                        elif self.sub_info == "BATTERY":
                            self.sub_info = ""
                elif self.shutter_state == "menu":
                    print('called from btn cb: INFO.menu')
                    self.sub_info = ""
            elif dest == 'BLANK':
                pass
            elif dest == "SETTING":
                setting = self.settings.cycle('nxt',setting_range,setting)
                if self.submenu_index == 0:
                    self.settings.settings['camera_protocol'] = setting
                    self.settings.update_camera_preset()
                    self.sub_info = 'REBOOT'
                elif self.submenu_index == 1:
                    self.settings.settings['device_mode'] = setting
                elif self.submenu_index == 2:
                    self.settings.settings['inject_mode'] = setting
                elif self.submenu_index == 5:
                    self.settings.settings['ota_source'] = setting
                elif self.submenu_index == 6:
                    self.settings.settings['ota_channel'] = setting
                else:
                    print("Hey what's this?")
                self.settings.update()
            elif dest == 'FC':
                if self.submenu_index == 3:
                    if self.sync_hal.fc_link.erase_flag == False:
                        self.sync_hal.fc_link.erase_flag = True
                    else:
                        self.sync_hal.fc_link.erase_flag = False
                    self.canvas.erase_flag = self.sync_hal.fc_link.erase_flag
                    # print('FC link flag: '+ str(self.sync_hal.fc_link.erase_flag))
                    # print('Canvas flag: '+str(self.canvas.erase_flag))
            elif dest == 'SHUTTER':
                if self.sub_state == "internet":
                    if wlan is None:
                        import internet.wlan as wlan
                    if mwlan.wlan_state == "DISCONNECTED":
                        wlan.up()
                    else:
                        wlan.down()
                elif self.sub_state == "ota_check":
                    import internet.ota as ota
                    self.ota = ota.OTA()
                    self.ota.check()
                elif self.sub_state == "HOME":
                    if self.settings.settings['device_mode'] == "MASTER" or self.settings.settings['device_mode'] == "MASTER/SLAVE":
                        self.sub_state = "STARTING"
                    elif self.settings.settings['device_mode'] == "TEST":
                        self.async_hal.camera.set_mode()
                elif self.sub_state == "RECORDING":
                    if self.settings.settings['device_mode'] == "MASTER" or self.settings.settings['device_mode'] == "MASTER/SLAVE":
                        self.sub_state = "STOPPING"
            # print('sub_info: '+str(self.sub_info))
            # print('sub_state: '+str(self.sub_state))
            # print('shutter_state: '+str(self.shutter_state))
            self.refresh[0] = True
