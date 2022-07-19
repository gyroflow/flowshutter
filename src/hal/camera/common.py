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
class Camera:
    def __init__(self,task_mode):
        self.transation_time = 0
        self.task_mode = task_mode
        self.notification = ''
        self.oled_update_flag = False
        self.state = False # stop, True = recording

    def timeout(self):
        self.transation_time = 0

    def rec_event(self, event1, argv1, event2, argv2):
        self.transation_time += 5
        if self.transation_time == 500:
            event1(argv1)
        elif self.transation_time == 800:
            event2(argv2)
            self.oled_update_flag = True
            self.transation_time = 0
