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
import target

adc = target.init_adc()

adc_read_time_count = 0
# vol = 4.1
def read_vol():
    # vol = 4.1
    global adc_read_time_count
    adc_read_time_count += 1
    if adc_read_time_count >= 600:
        adc_read_time_count = 0
        vol_read = adc.read()
    #     vol =0.5*vol+0.5* vol_read * 0.001305 *13 + 0.3401
        
    #     print("vol:", vol)
        # print("vol_read:",vol_read)
    #     # print("read:",adc.read())
    #     # print("read:",adc.read())
    #     # print("read:",adc.read())
    #     # print("read:",adc.read())
    #     # print("read:",adc.read())
    #     # print("read:",adc.read())
    #     # print("read:",adc.read())
    #     # print("read:",adc.read())
    #     # print("read:",adc.read())
    #     # print("read:",adc.read())
    #     # print("read:",adc.read())
    #     # print("u16:",adc.read_u16())


