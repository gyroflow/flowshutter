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
from gui.lib.common import Canvas_Abstract

class Canvas(Canvas_Abstract):
    def __init__(self,screen):
        self.animation = False
        super().__init__(screen)

    def draw_batterymask(self, voltage):

        bat_usage = int(100*(4.2 - voltage))
        # % of the battery usage

        if (bat_usage >= 0) & (bat_usage < 20):
            self.screen.pixel(112-bat_usage,5,0)
            self.screen.pixel(112-bat_usage,26,0)
            self.screen.fill_rect(113-bat_usage,5,bat_usage,22,0)
        elif (bat_usage >= 20) & (bat_usage < 40):
            self.screen.fill_rect(93,5,20,22,0)
            self.screen.pixel(110-bat_usage,5,0)
            self.screen.pixel(110-bat_usage,26,0)
            self.screen.fill_rect(111-bat_usage,5,bat_usage,22,0)
        elif (bat_usage >= 40) & (bat_usage < 60):
            self.screen.fill_rect(93,5,20,22,0)
            self.screen.pixel(108-bat_usage,5,0)
            self.screen.pixel(108-bat_usage,26,0)
            self.screen.fill_rect(109-bat_usage,5,bat_usage,22,0)
        elif (bat_usage >= 60) & (bat_usage < 80):
            self.screen.fill_rect(93,5,20,22,0)
            self.screen.pixel(106-bat_usage,5,0)
            self.screen.pixel(106-bat_usage,26,0)
            self.screen.fill_rect(107-bat_usage,5,bat_usage,22,0)
        elif (bat_usage >= 80) & (bat_usage < 100):
            self.screen.fill_rect(93,5,20,22,0)
            self.screen.pixel(104-bat_usage,5,0)
            self.screen.pixel(104-bat_usage,26,0)
            self.screen.fill_rect(105-bat_usage,5,bat_usage,22,0)
        elif (bat_usage>=100): # more than 100%
            self.screen.fill_rect(5,5,108,22,0)
        # else: # less than 0%, then do nothing

    def display_work_state(self, state):
        if state == 0:
            self.screen.fill(0)
            self.screen.blit(self.icon_gyroflow, 0, 18)
            self.screen.show()
        else:
            if state == 1:
                fb, header, content1, content2, content3 = self.icon_cam, 'Flowshutter', 'Powered by', 'DusKing', ''.join(tuple(self.settings['version']))
            elif state == 2:
                fb, header, content1, content2, content3 = self.icon_cam, 'Starting', 'FC Disarmed', 'Camera start', ''
            elif state == 3:
                fb, header, content1, content2, content3 = self.icon_cam_wk, 'Flowshutter', 'FC Armed', 'Recording', ''
            elif state == 4:
                fb, header, content1, content2, content3 = self.icon_cam_wk, 'Stopping', 'FC Armed', 'Camera stop', ''
            else:
                print('Unkown state: ' + state)
            self.screen.fill(0)
            self.screen.blit(fb, 0, 0)
            self.screen.text(header, 34, 0, 1)
            self.screen.text(content1, 34, 12, 1)
            self.screen.text(content2, 34, 24, 1)
            self.screen.text(content3, 94, 24, 1)
            self.screen.show()

    def display_battery(self):
        self.screen.blit(self.icon_big_bat, 0, 0)
        self.draw_batterymask(self.vol)
        voltage_str = "%.2fV" % self.vol
        for i in range(5):
            for j in range(5):
                self.screen.text(voltage_str,42+i, 11+j,0)
        self.screen.text(voltage_str,44,13,1)
        self.screen.show()

    def display_menu(self, sub_menu, field,field_state):
        self.screen.fill(0)
        if sub_menu == 0:
            index, head, content, fb = 0, 'General Infomation','Land Page',                                     self.icon_settings
        elif sub_menu == 1:
            index, head, content, fb = 1, 'Camera Protocol',''.join(tuple(self.settings['camera_protocol'])),   self.icon_settings
        elif sub_menu == 2:
            index, head, content, fb = 2, 'Device Mode',    ''.join(tuple(self.settings['device_mode'])),       self.icon_settings
        elif sub_menu == 3:
            index, head, content, fb = 3, 'Audio Injection',''.join(tuple(self.settings['inject_mode'])),       (self.icon_audio if self.settings['inject_mode'] == "ON" else self.icon_audio_off)
        elif sub_menu == 4:
            index, head, content, fb = 4, 'Blackbox Erase', ('Erasing...' if self.erase_flag else 'Erase stop'),self.icon_blackbox
        else:
            print('Unknown sub_menu:', sub_menu)

        self.screen.blit(fb, 95, 0)
        self.a10.set_textpos(self.screen,0,0)
        self.a10.printstring(head)
        self.screen.hline(0,10,94,1)

        if field == 0:
            cont_color = 1
        elif field == 1:
            self.screen.fill_rect(40,23,40,11,1)
            self.screen.text('SAVE',0, 24, 1)
            self.screen.text('LEAVE',40, 24, 0)
            cont_color = 1
        elif field == 2:
            self.screen.text('SAVE',0, 24, 1)
            self.screen.text('LEAVE',40, 24, 1)
            if field_state ==0:
                self.screen.fill_rect(0,12,int(len(content)*8),11,1)
                cont_color = 0
            else:
                self.screen.rect(0,12,int(len(content)*8),11,1)
                cont_color = 1
        elif field == 3:
            self.screen.fill_rect(0,23,32,11,1)
            self.screen.text('SAVE',0, 24, 0)
            self.screen.text('LEAVE',40, 24, 1)
            cont_color = 1
        self.screen.text(content, 0, 14, cont_color)
        self.screen.text(('<<  '+str(index)+'/4   >>'),0, 34, 1)
        self.screen.show()


    def display_hint(self, sub_info):
        self.screen.fill(0)
        self.screen.fill_rect(2,1,124,30,1)
        self.screen.fill_rect(6,4,116,24,0)
        if sub_info == 'REBOOT':
            self.screen.text('Please reboot', 9, 6, 1)
            self.screen.text('to apply', 32, 16, 1)
        elif sub_info == 'SONY_MTP_ACK':
            self.screen.text('SONY Remote', 21, 6, 1)
            self.screen.text('Registered', 21, 16, 1)
        elif sub_info == 'STARTING_TIMEOUT':
            self.screen.text('No ACK back', 17, 6, 1)
            self.screen.text('Start failed', 17, 16, 1)
        elif sub_info == 'SETTINGS_FAULT':
            self.screen.text('Settings Fault', 26, 8, 1)
            self.screen.text('Please Reboot', 26, 20, 1)
        self.screen.show()

    def display_reboot_page(self, state):
        self.screen.fill(0)
        self.screen.text('Exit',0,0,1)
        self.screen.text('Reboot',0,12,1)
        if state == 0:
            self.screen.text('<<',56,0,1)
        elif state == 1:
            self.screen.text('<<',56,12,1)
        self.screen.show()
