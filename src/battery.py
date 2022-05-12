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

print("Try to call adc init")
adc1, adc2 = target.init_adc()
print("Called ADC init")

adc_read_time_count = 0

def read_vol():
    global adc_read_time_count
    adc_read_time_count += 5
    if adc_read_time_count >= 50:
        # read voltage every 50ms
        adc_read_time_count = 0
        if adc1.read() != 0:
            vars.vol = (vars.vol + adc1.read() * 3.3 / 2048)/2
        else:
            vars.vol = (vars.vol + adc2.read() * 3.3 / 4096)/2
