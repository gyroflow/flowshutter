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
import network, vars

ap = network.WLAN(network.AP_IF)
ap.config(essid='Flowshutter', authmode=network.AUTH_WPA_WPA2_PSK, password='ilovehugo')

def up():
    vars.ap_state = "UP"
    ap.active(True)

def down():
    vars.ap_state = "DOWN"
    ap.active(False)
