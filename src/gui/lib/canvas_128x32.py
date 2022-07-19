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
from gui.core.writer import Writer
from gui.fonts.icons import Icons
import gui.fonts.arial10 as a10
import vram, target
import framebuf, time

class Canvas_128x32(Icons):
    def __init__(self,screen):
        self.screen = screen
        self.a10 = Writer(self.screen, a10)
        self.animation = False
        super().__init__()

    def update(self, info, sub_state, sub_menu, sub_hint):
        if info == "welcome":
            self.display_welcome()
        elif info == "home":
            self.display_state(sub_state)
        elif info == "battery_info":
            self.display_battery()
        elif info == "menu":
            self.display_menu(sub_menu)
        elif info == 'hint':
            self.display_hint(sub_hint)

        else:
            print(str(time.ticks_us()) + " [ Error] Unkown info: " + info)

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

    def display_welcome(self):
        self.screen.fill(0)
        self.screen.blit(self.icon_gyroflow, 0, 2)
        # screen.invert(1)
        self.screen.show()

    def display_state(self, state):
        if state == 'HOME':
            fb, header, content1, content2, content3 = self.icon_cam, 'Flowshutter', 'Powered by', 'DusKing', ''.join(tuple(vram.version))
        elif state == 'STARTING':
            fb, header, content1, content2, content3 = self.icon_cam, 'Starting', 'FC Disarmed', 'Camera start', ''
        elif state == 'RECORDING':
            fb, header, content1, content2, content3 = self.icon_cam_wk, 'Flowshutter', 'FC Armed', 'Recording', ''
        elif state == 'STOPPING':
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
        self.draw_batterymask(vram.vol)
        voltage_str = "%.2fV" % vram.vol
        for i in range(5):
            for j in range(5):
                self.screen.text(voltage_str,42+i, 11+j,0)
        self.screen.text(voltage_str,44,13,1)
        self.screen.show()

    def display_menu(self, sub_cat):
        if sub_cat == 'camera_protocol':
            index, head, content, fb = 1, 'Camera Protocol',''.join(tuple(vram.camera_protocol)),               self.icon_settings
        elif sub_cat == 'device_mode':
            index, head, content, fb = 2, 'Device Mode',    ''.join(tuple(vram.device_mode)),                   self.icon_settings
        elif sub_cat == 'inject_mode':
            index, head, content, fb = 3, 'Audio Injection',''.join(tuple(vram.inject_mode)),                   (self.icon_audio if vram.inject_mode == "ON" else self.icon_audio_off)
        elif sub_cat == 'erase_blackbox':
            index, head, content, fb = 4, 'Blackbox Erase', ('Erasing...' if vram.erase_flag else 'Erase stop'),self.icon_blackbox
        elif sub_cat == 'internet':
            index, head, content, fb = 5, 'Internet',       ''.join(tuple(vram.wlan_state)),                    (self.self.icon_wifi if vram.wlan_state == "CONNECTED" else self.self.icon_wifi_dis)
        elif sub_cat == 'ota_source':
            index, head, content, fb = 6, 'OTA Source',     ''.join(tuple(vram.ota_source)),                    (self.icon_github if vram.ota_source == "GitHub" else self.icon_gitee)
        elif sub_cat == 'ota_channel':
            index, head, content, fb = 7, 'OTA Channel',    ''.join(tuple(vram.ota_channel)),                   self.icon_settings
        elif sub_cat == 'ota_check':
            index, head, content, fb = 8, 'OTA Check',      "".join(tuple(vram.ota_source))+"/"+"".join(tuple(vram.ota_channel)),self.icon_settings
        elif sub_cat == 'ota_update':
            index, head, content, fb = 9, 'OTA Update',     'ENT = START',                                      self.icon_settings
        else:
            print('Unknown sub_menu:', sub_cat)
        self.screen.fill(0)
        self.screen.blit(fb, 95, 0)
        self.a10.set_textpos(self.screen,0,0)
        self.a10.printstring(head)
        self.screen.hline(0,10,94,1)
        self.screen.text(content, 0, 14, 1)
        self.screen.text('<<  '+str(index)+'/4   >>', 0, 24, 1)
        self.screen.show()

    def display_hint(self, sub_hint):
        self.screen.fill(0)
        self.screen.fill_rect(2,1,124,30,1)
        self.screen.fill_rect(6,4,116,24,0)
        if sub_hint == 'REBOOT':
            self.screen.text('Please reboot', 9, 6, 1)
            self.screen.text('to apply', 32, 16, 1)
        elif sub_hint == 'SONY_MTP_ACK':
            self.screen.text('SONY Remote', 21, 6, 1)
            self.screen.text('Registered', 21, 16, 1)
        elif sub_hint == 'STARTING_TIMEOUT':
            self.screen.text('No ACK back', 17, 6, 1)
            self.screen.text('Start failed', 17, 16, 1)
        elif sub_hint == 'AP_HINT':
            self.screen.text('SSID:'+ 'Flowshutter', 3, 6, 1)
            self.screen.text('Pswd:'+ 'ilovehugo', 3, 16, 1)
        elif sub_hint == 'WLAN_CONNECTING':
            self.screen.text('Connecting', 21, 6, 1)
            self.screen.text('Please wait', 21, 16, 1)
        elif sub_hint == 'SETTINGS_FAULT':
            self.screen.text('Settings Fault', 26, 8, 1)
            self.screen.text('Please Reboot', 26, 20, 1)
        self.screen.show()
