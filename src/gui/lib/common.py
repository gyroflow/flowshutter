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
import target
import time

class Canvas_Abstract(Icons):
    def __init__(self,screen):
        self.settings = {
            'version':          '0.66',
            'camera_protocol':  'NO',
            'device_mode':      'MASTER',
            'inject_mode':      'OFF',
            'ota_source':       'GitHub',
            'ota_channel':      'stable',
            'target_name':      target.name
        }
        self.vol = 0
        self.erase_flag = False
        self.screen = screen
        self.a10 = Writer(self.screen, a10)
        super().__init__()

    def update(self, gui_state):
        print('canvas update called')
        if gui_state['notification'] != '':
            if gui_state['notification'] =='BATTERY':
                self.display_battery()
            else:
                self.display_hint(gui_state['notification'])
        elif gui_state['root_state'] == 0:
            self.display_work_state(gui_state['work_state'])
        elif gui_state['root_state'] == 1:
            self.display_menu(gui_state['menu_page'],gui_state['field'],gui_state['field_state'])
        elif gui_state['root_state'] == 2:
            self.display_reboot_page(gui_state['field_state'])
        else:
            print(str(time.ticks_us()) + " [ Error] Unkown info: " + info)
