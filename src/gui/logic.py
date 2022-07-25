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
import gui.settings as settings
import hal.ahal as ahal
import hal.shal as shal
from machine import Timer

class Logic:
    def __init__(self):
        print(str(time.ticks_us()) + " [ INIT ] UI logic object")
        self.refresh = [False, False]
        self.update_count = 0
        self.state = {
            'notification': '',
            'root_state': 0,
            'work_state': 0,
            'menu_page': 0,
            'field': 0,
            'field_state':0,
        }
        self.prev_state = self.state
        self.settings = settings.UserSettings()
        self.sync_hal = shal.SyncPeripherals()
        self.init_canvas()
        self.async_hal = ahal.AsnycPeripherals(camera = self.settings.settings['camera_protocol'])
        print(str(time.ticks_us()) + " [ SYNC ] UI logic HAL")
        self.init_sync_hal()
        print(str(time.ticks_us()) + " [ ASYNC] UI logic HAL")
        self.init_async_hal()

    def init_canvas(self):
        height = self.sync_hal.screen.height
        if height == 32:
            import gui.lib.canvas_128x32 as canvas
        elif height == 64:
            import gui.lib.canvas_128x64 as canvas
        self.canvas = canvas.Canvas(self.sync_hal.screen)

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

    async def update(self):
        print(str(time.ticks_us()) + " [  OK  ] Async UI state machine")
        while True:
            self.collect_data()
            self.check_state()
            self.compare_state()
            self.update_oled()
            await asyncio.sleep_ms(5)

    def update_oled(self):
        if self.refresh[0] or self.refresh[1]:
            self.refresh = [False, False]
            self.deliver_data()
            self.canvas.update(self.state)

    def collect_data(self):
        # read camera refresh request
        self.refresh[1] = self.async_hal.camera.oled_update_flag
        # read camera state and update work state
        if self.async_hal.camera.state == True and (self.state['work_state'] == 1 or self.state['work_state'] == 2):
            self.state['work_state'] = 3
        elif self.async_hal.camera.state == False and (self.state['work_state'] == 3 or self.state['work_state'] == 4):
            self.state['work_state'] = 1
        # read camera notification
        if self.async_hal.camera.notification != "":
            self.state['notification'] = self.async_hal.camera.notification
        # sync FC arm state with camera
        self.sync_hal.fc_link.arm_state = self.async_hal.camera.state

    def deliver_data(self):
        # pass settings and voltage to canvas
        self.canvas.settings = self.settings.settings
        self.canvas.vol = self.async_hal.battery.vol
        # clear camera refresh request
        self.async_hal.camera.oled_update_flag = False
        # pass inject mode from settings to fc_link
        self.sync_hal.fc_link.inject_mode = self.settings.settings['inject_mode']

    def compare_state(self):
        # compare_w_prev_state
        if self.prev_state != self.state:
            self.refresh[0] = True
            self.prev_state = self.state

    def check_state(self):
        # check notification field first
        if self.state['notification'] != '':
            notification = self.state['notification']
            if notification == 'REBOOT':
                self.info_reboot()
            elif notification == 'BATTERY':
                self.info_battery()
            elif notification == 'STARTING_TIMEOUT':
                self.info_starting_timeout()
            elif notification == 'SONY_MTP_ACK':
                self.info_sony_mtp_ack()
            else:
                print('Unknown notification: ' + str(notification))
        else: # then check rest of state
            self.check_rest_state()
        
    def check_rest_state(self):
        if self.state['root_state'] == 0: # work state

            if self.state['work_state'] == 0: # welcome
                self.update_count+=5
                self.bind_btn(0, 'SHORT', 'BLANK')
                self.bind_btn(0, 'LONG',  'BLANK')
                self.bind_btn(1, 'SHORT', 'BLANK')
                self.bind_btn(1, 'LONG',  'BLANK')
                self.bind_btn(2, 'SHORT', 'BLANK')
                self.bind_btn(2, 'LONG',  'BLANK')
                if self.update_count == 1500:
                    self.update_count = 0
                    self.state['work_state'] = 1
                    self.refresh[0] = True

            elif self.state['work_state'] == 1 or self.state['work_state'] == 3: #home/recording
                state = self.state['work_state'] 
                self.bind_btn(0, 'SHORT', 'NOTIF')
                self.bind_btn(0, 'LONG',  ('ROOT' if state ==1 else 'BLANK'))
                self.bind_btn(1, 'SHORT', 'REC'  )
                self.bind_btn(1, 'LONG',  'ROOT', 'REBOOT PAGE')
                self.bind_btn(2, 'SHORT', 'NOTIF')
                self.bind_btn(2, 'LONG',  ('ROOT' if state ==1 else 'BLANK'))

            elif self.state['work_state'] == 2 or self.state['work_state'] == 4: # starting/stopting
                self.update_count += 5
                self.bind_btn(0, 'SHORT', 'BLANK')
                self.bind_btn(0, 'LONG',  'BLANK')
                self.bind_btn(1, 'SHORT', 'BLANK')
                self.bind_btn(1, 'LONG',  'BLANK')
                self.bind_btn(2, 'SHORT', 'BLANK')
                self.bind_btn(2, 'LONG',  'BLANK')
                # timeout
                if self.update_count < 5000:
                    self.async_hal.camera.rec()
                elif self.update_count == 5000:
                    self.state['notification'] = "STARTING_TIMEOUT"
                    self.refresh[0] = True

        elif self.state['root_state'] == 1: # menu state

            if self.state['menu_page'] == 0: # status info
                self.bind_btn(0, 'SHORT', 'MENU', 'prv')
                self.bind_btn(0, 'LONG',  'ROOT')
                self.bind_btn(1, 'SHORT', 'BLANK')
                self.bind_btn(1, 'LONG',  'BLANK')
                self.bind_btn(2, 'SHORT', 'MENU', 'nxt')
                self.bind_btn(2, 'LONG',  'ROOT')

            elif (  self.state['menu_page'] == 1 or# camera_protocol
                    self.state['menu_page'] == 2 or# device_mode
                    self.state['menu_page'] == 3): # inject_mode
                if self.state['field'] == 0: # hang on field
                    self.bind_btn(0, 'SHORT', 'MENU', 'prv')        # previous page
                    self.bind_btn(0, 'LONG',  'ROOT')               # back to home
                    self.bind_btn(1, 'SHORT', 'FIELD','ent')   # enter the field
                    self.bind_btn(1, 'LONG',  'BLANK')
                    self.bind_btn(2, 'SHORT', 'MENU', 'nxt')        # next page
                    self.bind_btn(2, 'LONG',  'ROOT')               # back to home
                elif self.state['field'] == 1: # filed: leave
                    self.bind_btn(0, 'SHORT', 'FIELD', 'prv')   # previous field
                    self.bind_btn(0, 'LONG',  'BLANK')
                    self.bind_btn(1, 'SHORT', 'FIELD', 'lev')   # leave the field
                    self.bind_btn(1, 'LONG',  'BLANK')
                    self.bind_btn(2, 'SHORT', 'FIELD', 'nxt')   # next field
                    self.bind_btn(2, 'LONG',  'BLANK')
                elif self.state['field'] == 2: # filed: settings
                    if self.state['field_state'] == 0: # hang on
                        self.bind_btn(0, 'SHORT', 'FIELD',  'prv')   # previous field
                        self.bind_btn(0, 'LONG',  'BLANK')
                        self.bind_btn(1, 'SHORT', 'INFIELD','ent')       # change settings and preview it
                        self.bind_btn(1, 'LONG',  'BLANK')
                        self.bind_btn(2, 'SHORT', 'FIELD',  'nxt')   # next field
                        self.bind_btn(2, 'LONG',  'BLANK')
                    if self.state['field_state'] == 1: # land on filed
                        self.bind_btn(0, 'SHORT', 'INFIELD', 'prv')   # previous field
                        self.bind_btn(0, 'LONG',  'BLANK')
                        self.bind_btn(1, 'SHORT', 'INFIELD', 'lev')   # change settings and preview it
                        self.bind_btn(1, 'LONG',  'BLANK')
                        self.bind_btn(2, 'SHORT', 'INFIELD', 'nxt')   # next field
                        self.bind_btn(2, 'LONG',  'BLANK')
                elif self.state['field'] == 3: # filed: save
                    self.bind_btn(0, 'SHORT', 'FIELD', 'prv')   # previous field
                    self.bind_btn(0, 'LONG',  'BLANK')
                    self.bind_btn(1, 'SHORT', 'SAVE')              # save settings
                    self.bind_btn(1, 'LONG',  'BLANK')
                    self.bind_btn(2, 'SHORT', 'FIELD', 'nxt')   # next field
                    self.bind_btn(2, 'LONG',  'BLANK')

            elif self.state['menu_page'] == 4: # blackbox
                if self.state['field'] == 0: # hang on glance
                    self.bind_btn(0, 'SHORT', 'MENU', 'prv')        # previous page
                    self.bind_btn(0, 'LONG',  'ROOT')               # back to home
                    self.bind_btn(1, 'SHORT', 'FIELD','ent')   # enter the field
                    self.bind_btn(1, 'LONG',  'BLANK')
                    self.bind_btn(2, 'SHORT', 'MENU', 'nxt')        # next page
                    self.bind_btn(2, 'LONG',  'ROOT')    
                elif self.state['field'] == 1: # filed: leave
                    self.bind_btn(0, 'SHORT', 'FIELD', 'prv')   # previous field
                    self.bind_btn(0, 'LONG',  'BLANK')
                    self.bind_btn(1, 'SHORT', 'FIELD', 'lev')   # leave the field
                    self.bind_btn(1, 'LONG',  'BLANK')
                    self.bind_btn(2, 'SHORT', 'FIELD', 'nxt')   # next field
                    self.bind_btn(2, 'LONG',  'BLANK')
                elif self.state['field'] == 2: # filed: erase
                    self.bind_btn(0, 'SHORT', 'FIELD', 'prv')   # previous field
                    self.bind_btn(0, 'LONG',  'BLANK')
                    self.bind_btn(1, 'SHORT', 'FC')              # erase blackbox
                    self.bind_btn(1, 'LONG',  'BLANK')
                    self.bind_btn(2, 'SHORT', 'FIELD', 'nxt')   # next field
                    self.bind_btn(2, 'LONG',  'BLANK')

        elif self.state['root_state'] == 2: # reboot state
            if self.state['field_state'] == 0:
                self.bind_btn(0, 'SHORT', 'INFIELD', 'ent')
                self.bind_btn(0, 'LONG',  'BLANK')
                self.bind_btn(1, 'SHORT', 'ROOT')
                self.bind_btn(1, 'LONG',  'BLANK')
                self.bind_btn(2, 'SHORT', 'INFIELD', 'ent')
                self.bind_btn(2, 'LONG',  'BLANK')

            elif self.state['field_state'] == 1:
                self.bind_btn(0, 'SHORT', 'INFIELD', 'lev')
                self.bind_btn(0, 'LONG',  'BLANK')
                self.bind_btn(1, 'SHORT', 'REBOOT')
                self.bind_btn(1, 'LONG',  'BLANK')
                self.bind_btn(2, 'SHORT', 'INFIELD', 'lev')
                self.bind_btn(2, 'LONG',  'BLANK')

    def info_battery(self):
        self.update_count += 5
        if self.update_count ==5000:
            self.update_count = 0
            self.refresh[0] = True
        self.bind_btn(0, "SHORT", 'NOTIF')
        self.bind_btn(0, "LONG",  'BLANK')
        self.bind_btn(1, "SHORT", 'BLANK')
        self.bind_btn(1, "LONG",  'BLANK')
        self.bind_btn(2, "SHORT", 'NOTIF')
        self.bind_btn(2, "LONG",  'BLANK')

    def info_reboot(self):
        self.bind_btn(0, "SHORT", "NOTIF")
        self.bind_btn(1, "SHORT", "NOTIF")
        self.bind_btn(2, "SHORT", "NOTIF")

    def info_sony_mtp_ack(self):
        self.update_count += 5
        if self.update_count ==2000:
            self.update_count = 0
            self.async_hal.camera.notification = ''
            self.state['notification'] = ''
            self.refresh[0] = True

    def bind_btn(self, button, event, _type, keywords=None):
        if self.async_hal.buttons.state[button] == event:
            self.async_hal.buttons.state[button] = "RLS"
            if _type == 'BLANK':
                pass
            elif _type == 'REC':
                if self.settings.settings['device_mode'] == "MASTER" or self.settings.settings['device_mode'] == "MASTER/SLAVE":
                    self.state['work_state'] += 1
            elif _type == 'ROOT':  # change root_state
                if keywords == None:
                    self.state['root_state'] = (1 if self.state['root_state'] == 0 else 0)
                elif keywords == 'REBOOT PAGE':
                    self.state['root_state'] = (2 if self.state['root_state'] == 0 else 0)
            elif _type == 'NOTIF': # change notification
                if self.state['root_state'] == 0 and self.state['notification'] == '':
                    self.state['notification'] = 'BATTERY'
                else:
                    self.state['notification'] = ''
            elif _type == 'MENU':  # change menu_page
                self.settings.read()
                if keywords == 'nxt':
                    if self.state['menu_page'] !=4:
                        self.state['menu_page'] += 1
                    else:
                        self.state['menu_page'] = 0
                elif keywords == 'prv':
                    if self.state['menu_page'] !=0:
                        self.state['menu_page'] -= 1
                    else:
                        self.state['menu_page'] = 4
            elif _type == 'FIELD': # change menu field
                if keywords == 'ent':
                    self.state['field'] = 1
                elif keywords == 'lev':
                    self.settings.read()
                    self.state['field'] = 0
                elif keywords == 'prv':
                    if self.state['menu_page'] != 4:
                        self.state['field'] = (self.state['field']-1 if self.state['field'] != 1 else 3)
                    else:
                        self.state['field'] = (self.state['field']-1 if self.state['field'] != 1 else 2)
                elif keywords == 'nxt':
                    if self.state['menu_page'] != 4:
                        self.state['field'] = (self.state['field']+1 if self.state['field'] != 3 else 1)
                    else:
                        self.state['field'] = (self.state['field']+1 if self.state['field'] != 2 else 1)
            elif _type == 'INFIELD':# in field, change field_state
                if keywords == 'ent':
                    self.state['field_state'] = 1
                elif keywords == 'lev':
                    self.state['field_state'] = 0
                else: # prv or nxt
                    if self.state['menu_page'] == 1: #camera_protocol
                        _range = self.settings.camera_protocol_range
                        argv = 'camera_protocol'
                    elif self.state['menu_page'] == 2: # device_mode
                        _range = self.settings.device_mode_range
                        argv = 'device_mode'
                    elif self.state['menu_page'] == 3: # inject_mode
                        _range = self.settings.inject_mode_range
                        argv = 'inject_mode'
                    setting = self.settings.cycle(keywords, _range, self.settings.settings[argv])
                    self.canvas.settings[argv] = setting
                    self.refresh[0] = True
            elif _type == 'SAVE': # save settings
                self.settings.update_camera_preset()
                self.settings.write()
                self.state['notification'] = 'REBOOT'
            elif _type == 'FC':
                if self.state['menu_page'] == 4: # blackbox 
                    if self.sync_hal.fc_link.erase_flag == False:
                        self.sync_hal.fc_link.erase_flag = True
                    else:
                        self.sync_hal.fc_link.erase_flag = False
                    self.canvas.erase_flag = self.sync_hal.fc_link.erase_flag
                    self.refresh[0] = True
            elif _type == 'REBOOT':
                import machine
                machine.reset()
            self.refresh[0] = True
            # print(str(button) + ' ' + str(event) + ' Callback!'+ ' Type is ' + str(_type) + ' ' + str(keywords))
            # print('Notif: ' + str(self.state['notification']))
            # print('root state: ' + str(self.state['root_state']))
            # print('work state: ' + str(self.state['work_state']))
            # print('menu page: ' + str(self.state['menu_page']))
            # print('field: ' + str(self.state['field']))
            # print('field state: ' + str(self.state['field_state']))
