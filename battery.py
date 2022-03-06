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
import target, vars

adc = target.init_adc()

adc_read_time_count = 0

def read_vol():
    global adc_read_time_count
    adc_read_time_count += 5
    if adc_read_time_count >= 100:
        # read voltage every 100ms
        adc_read_time_count = 0
        vars.vol = (vars.vol + adc.read() * 3.3 / 2048)/2
