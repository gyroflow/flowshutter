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

# MIT License

# Copyright (c) 2017 Tayfun ULU

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import network, gc, vram, socket, ure, time, oled

ap_ssid = "Flowshutter"
ap_password = "ilovehugo"
ap_authmode = 3  # WPA2
connect_to_open_wifis = False

NETWORK_PROFILES = 'wifi.dat'

wlan_ap = network.WLAN(network.AP_IF)
wlan_sta = network.WLAN(network.STA_IF)

server_socket = None

def unquote_plus(s):
    r = s.replace('+', ' ').split('%')
    for i in range(1, len(r)):
        s = r[i]
        try:
            r[i] = chr(int(s[:2], 16)) + s[2:]
        except ValueError:
            r[i] = '%' + s
    return ''.join(r)

def _get_connection_():
    # return a working WLAN(STA_IF) instance or None

    # First check if there already is any connection:
    if wlan_sta.isconnected():
        return wlan_sta
    oled.show_wlan_connecting()## TODO: add oled hint here
    connected = False
    try:
        # ESP connecting to WiFi takes time, wait a bit and try again:
        time.sleep(3)
        if wlan_sta.isconnected():
            return wlan_sta

        # Read known network profiles from file
        profiles = _read_profiles_()
        ## TODO: add oled hint here

        # Search WiFis in range
        wlan_sta.active(True)
        networks = wlan_sta.scan()

        AUTHMODE = {0: "open", 1: "WEP", 2: "WPA-PSK", 3: "WPA2-PSK", 4: "WPA/WPA2-PSK"}
        for ssid, bssid, channel, rssi, authmode, hidden in sorted(networks, key=lambda x: x[3], reverse=True):
            ssid = ssid.decode('utf-8')
            encrypted = authmode > 0
            print("ssid: %s chan: %d rssi: %d authmode: %s" % (ssid, channel, rssi, AUTHMODE.get(authmode, '?')))
            if encrypted:
                if ssid in profiles:
                    password = profiles[ssid]
                    connected = _do_connect_(ssid, password)
                else:
                    print("skipping unknown encrypted network")
            elif connect_to_open_wifis:  # open
                connected = _do_connect_(ssid, None)
            if connected:
                break

    except OSError as e:
        print("exception", str(e))

    # _start_ web server for connection manager:
    if not connected:
        connected = _start_()

    return wlan_sta if connected else None

def _read_profiles_():
    with open(NETWORK_PROFILES) as f:
        lines = f.readlines()
    profiles = {}
    for line in lines:
        ssid, password = line.strip("\n").split(";")
        profiles[ssid] = password
    return profiles

def _write_profiles_(profiles):
    lines = []
    for ssid, password in profiles.items():
        lines.append("%s;%s\n" % (ssid, password))
    with open(NETWORK_PROFILES, "w") as f:
        f.write(''.join(lines))

def _do_connect_(ssid, password):
    wlan_sta.active(False)
    wlan_sta.active(True)
    if wlan_sta.isconnected():
        return None
    print('Trying to connect to %s...' % ssid)
    wlan_sta.connect(ssid, password)
    for retry in range(100):
        connected = wlan_sta.isconnected()
        if connected:
            break
        time.sleep(0.1)
        print('.', end='')
    if connected:
        print('\nConnected. Network config: ', wlan_sta.ifconfig())
    else:
        print('\nFailed. Not Connected to: ' + ssid)
    return connected

def _send_header_(client, status_code=200, content_length=None ):
    client.sendall("HTTP/1.0 {} OK\r\n".format(status_code))
    client.sendall("Content-Type: text/html\r\n")
    if content_length is not None:
      client.sendall("Content-Length: {}\r\n".format(content_length))
    client.sendall("\r\n")

def _send_response_(client, payload, status_code=200):
    content_length = len(payload)
    _send_header_(client, status_code, content_length)
    if content_length > 0:
        client.sendall(payload)
    client.close()

def _handle_root_(client):
    wlan_sta.active(True)
    ssids = sorted(ssid.decode('utf-8') for ssid, *_ in wlan_sta.scan())
    _send_header_(client)
    client.sendall("""\
        <html>
            <h1 style="color: #5e9ca0; text-align: center;">
                <span style="color: #ff0000;">
                    Flowshutter Wi-Fi Setup
                </span>
            </h1>
            <form action="configure" method="post">
                <table style="margin-left: auto; margin-right: auto;">
                    <tbody>
    """)
    while len(ssids):
        ssid = ssids.pop(0)
        client.sendall("""\
                        <tr>
                            <td colspan="2">
                                <input type="radio" name="ssid" value="{0}" />{0}
                            </td>
                        </tr>
        """.format(ssid))
    client.sendall("""\
                        <tr>
                            <td>Password:</td>
                            <td><input name="password" type="password" /></td>
                        </tr>
                    </tbody>
                </table>
                <p style="text-align: center;">
                    <input type="submit" value="Submit" />
                </p>
            </form>
            <p>&nbsp;</p>
            <hr />
            <h5>
                <span style="color: #ff0000;">
                    Your SSID and password information will be saved into the
                    "%(filename)s" file in your own flowshutter device.
                    Be careful about security!
                </span>
            </h5>
            <hr />
        </html>
    """ % dict(filename=NETWORK_PROFILES))
    client.close()

def _handle_configure_(client, content):
    match = ure.search("ssid=([^&]*)&password=(.*)", content)

    if match is None:
        _send_response_(client, "Parameters not found", status_code=400)
        return False
    # version 1.9 compatibility
    try:
        ssid = unquote_plus(match.group(1).decode("utf-8"))
        password = unquote_plus(match.group(2).decode("utf-8"))
    except UnicodeEncodeError:
        ssid = unquote_plus(match.group(1))
        password = unquote_plus(match.group(2))

    if len(ssid) == 0:
        _send_response_(client, "SSID must be provided", status_code=400)
        return False

    if _do_connect_(ssid, password):
        response = """\
                    <html>
                        <center>
                            <br><br>
                            <h1 style="color: #458f94; text-align: center;">
                                <span style="color: #8d3b86;">
                                    Flowshutter successfully connected to WiFi network %(ssid)s.
                                </span>
                            </h1>
                            <br><br>
                        </center>
                    </html>
        """ % dict(ssid=ssid)## TDDO: add stlye to header
        _send_response_(client, response)
        try:
            profiles = _read_profiles_()
        except OSError:
            profiles = {}
        profiles[ssid] = password
        _write_profiles_(profiles)

        time.sleep(5)

        return True
    else:
        response = """\
            <html>
                <center>
                    <h1 style="color: #458f94; text-align: center;">
                        <span style="color: #8d3b86;">
                            Flowshutter could not connect to WiFi network %(ssid)s.
                        </span>
                    </h1>
                    <br><br>
                    <form>
                        <input type="button" value="Go back!" onclick="history.back()"></input>
                    </form>
                </center>
            </html>
        """ % dict(ssid=ssid)
        _send_response_(client, response)
        return False

def _handle_not_found_(client, url):
    _send_response_(client, "Path not found: {}".format(url), status_code=404)

def _stop_():
    global server_socket

    if server_socket:
        server_socket.close()
        server_socket = None

def _start_(port=80):
    global server_socket

    addr = socket.getaddrinfo('0.0.0.0', port)[0][-1]

    _stop_()

    wlan_sta.active(True)
    wlan_ap.active(True)

    wlan_ap.config(essid=ap_ssid, password=ap_password, authmode=ap_authmode)

    server_socket = socket.socket()
    server_socket.bind(addr)
    server_socket.listen(1)

    oled.show_ap_info()
    ## TODO: add oled hint here

    print('Connect to WiFi ssid ' + ap_ssid + ', default password: ' + ap_password)
    print('and access the ESP via your favorite web browser at 192.168.4.1.')
    print('Listening on:', addr)

    while True:
        if wlan_sta.isconnected():
            return True

        client, addr = server_socket.accept()
        print('client connected from', addr)
        try:
            client.settimeout(5.0)
            request = bytearray()
            try:
                while "\r\n\r\n" not in request:
                    request.extend(client.recv(512))
            except OSError:
                pass

            print("Request is: {}".format(request))
            if "HTTP" not in request:
                # skip invalid requests
                continue

            if "POST" in request and "Content-Length: " in request:
                content_length = int(ure.search("Content-Length: ([0-9]+)?", bytes(request)).group(1))
                content = bytearray(request[bytes(request).index(b"\r\n\r\n") + 4:])
                content_length_remaining = content_length - len(content)

                while content_length_remaining > 0:
                    chunk = client.recv(512)
                    content.extend(chunk)
                    content_length_remaining -= len(chunk)

            request = bytes(request)

            print("Request is: {}".format(request))

            # version 1.9 compatibility
            try:
                url = ure.search("(?:GET|POST) /(.*?)(?:\\?.*?)? HTTP", request).group(1).decode("utf-8").rstrip("/")
            except Exception:
                url = ure.search("(?:GET|POST) /(.*?)(?:\\?.*?)? HTTP", request).group(1).rstrip("/")
            print("URL is {}".format(url))

            if url == "":
                _handle_root_(client)
            elif url == "configure":
                _handle_configure_(client, bytes(content))
            else:
                _handle_not_found_(client, url)

        finally:
            client.close()


def up():
    vram.wlan_state = "CONNECTED"
    wlan = _get_connection_()
    if wlan is None:
        print("Could not niitialized the network connection.")
        while True:
            pass
    print("Flowshutter OK")

def down():
    vram.wlan_state = "DISCONNECTED"
    wlan_ap.active(False)
    wlan_sta.active(False)
