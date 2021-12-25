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
def init_multiport_packet():
    rcd_prs = b'#7100*'
    rcd_rls = b'#7110*'

    cm_hdsk = b'%000*'
    cm_hdsk_ack = b'&00080*'

    cm_rcd_start = b'%7610*'
    cm_rcd_start_ack = b'&76100*'

    cm_rcd_stop  = b'%7600*'
    cm_rcd_stop_ack = b'&76000*'

    return rcd_prs, rcd_rls, cm_hdsk, cm_hdsk_ack, cm_rcd_start, cm_rcd_start_ack, cm_rcd_stop, cm_rcd_stop_ack