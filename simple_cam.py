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

switch = target.init_momentary_ground_pin()

def momentary_ground(value):
    # 1 High impedance (open drain)
    # 0 Low voltage (tied to ground)
    switch.value(value)

schmitt_3v3 = target.init_schmitt_3v3_trigger_pin()

def toggle_cc_voltage_level():
    if vars.shutter_state == "recording":
        schmitt_3v3.value(1)
        print("high voltage level")
    else:
        schmitt_3v3.value(0)
        print("low voltage level")

