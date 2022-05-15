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
import network, gc, vram, socket, ure, time

NETWORK_PROFILES = 'wifi.dat'

wlan_ap = network.WLAN(network.AP_IF)
wlan_sta = network.WLAN(network.STA_IF)

class WIFIManager:
    def __init__(self):
        self.ap_ssid = "Flowshutter"
        self.ap_password = "ilovehugo"
        self.ap_authmode = 3  # WPA2
        self.connect_to_open_wifis = False
        self.server_socket = None

    def get_connection(self):
        # return a working WLAN(STA_IF) instance or None

        import entry
        wlan_canvas = entry.task.ui.canvas# wlan_canvas = entry.task

        # First check if there already is any connection:
        if wlan_sta.isconnected():
            return wlan_sta
        # canvas.show_wlan_connecting()
        # canvas1.show_wlan_connecting()## TODO: add canvas hint here
        wlan_canvas.show_wlan_connecting()
        wlan_canvas.show_all()
        # vram.info = "show wlan connecting"
        connected = False
        try:
            # ESP connecting to WiFi takes time, wait a bit and try again:
            time.sleep(3)
            if wlan_sta.isconnected():
                return wlan_sta

            # Read known network profiles from file
            profiles = read_profiles()
            # TODO: add canvas hint here

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
                        connected = do_connect(ssid, password)
                    else:
                        print("skipping unknown encrypted network")
                elif self.connect_to_open_wifis:  # open
                    connected = do_connect(ssid, None)
                if connected:
                    break

        except OSError as e:
            print("exception", str(e))

        # start web server for connection manager:
        if not connected:
            connected = self.start()

        return wlan_sta if connected else None
    def stop(self):

        if self.server_socket:
            self.server_socket.close()
            self.server_socket = None

    def start(self, port=80):

        addr = socket.getaddrinfo('0.0.0.0', port)[0][-1]

        self.stop()

        wlan_sta.active(True)
        wlan_ap.active(True)

        wlan_ap.config(essid=self.ap_ssid, password=self.ap_password, authmode=self.ap_authmode)

        self.server_socket = socket.socket()
        self.server_socket.bind(addr)
        self.server_socket.listen(1)

        wlan_canvas.show_ap_info()
        wlan_canvas.show_all()
        # vram.info = "show ap info"
        ## TODO: add canvas hint here

        print('Connect to WiFi ssid ' + self.ap_ssid + ', default password: ' + self.ap_password)
        print('and access the ESP via your favorite web browser at 192.168.4.1.')
        print('Listening on:', addr)

        while True:
            if wlan_sta.isconnected():
                return True

            client, addr = self.server_socket.accept()
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
                gc.enable()
                gc.collect()
                gc.disable()

                # version 1.9 compatibility
                try:
                    url = ure.search("(?:GET|POST) /(.*?)(?:\\?.*?)? HTTP", request).group(1).decode("utf-8").rstrip("/")
                except Exception:
                    url = ure.search("(?:GET|POST) /(.*?)(?:\\?.*?)? HTTP", request).group(1).rstrip("/")
                print("URL is {}".format(url))

                gc.enable()
                gc.collect()
                gc.disable()

                if url == "":
                    handel_root(client)
                elif url == "configure":
                    handel_configure(client, bytes(content))
                else:
                    handle_not_found(client, url)

            finally:
                client.close()

def unquote_plus(s):
    r = s.replace('+', ' ').split('%')
    for i in range(1, len(r)):
        s = r[i]
        try:
            r[i] = chr(int(s[:2], 16)) + s[2:]
        except ValueError:
            r[i] = '%' + s
    return ''.join(r)

def read_profiles():
    with open(NETWORK_PROFILES, "r") as f:
        lines = f.readlines()
    profiles = {}
    for line in lines:
        ssid, password = line.strip("\n").split(";")
        profiles[ssid] = password
    return profiles

def write_profiles(profiles):
    lines = []
    for ssid, password in profiles.items():
        lines.append("%s;%s\n" % (ssid, password))
    with open(NETWORK_PROFILES, "w") as f:
        f.write(''.join(lines))

def do_connect(ssid, password):
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

def send_header(client, status_code=200, content_length=None ):
    client.sendall("HTTP/1.0 {} OK\r\n".format(status_code))
    client.sendall("Content-Type: text/html\r\n")
    if content_length is not None:
      client.sendall("Content-Length: {}\r\n".format(content_length))
    client.sendall("\r\n")

def send_response(client, payload, status_code=200):
    content_length = len(payload)
    send_header(client, status_code, content_length)
    if content_length > 0:
        client.sendall(payload)
    client.close()

def handel_root(client):
    wlan_sta.active(True)
    ssids = sorted(ssid.decode('utf-8') for ssid, *_ in wlan_sta.scan())
    send_header(client)
    client.sendall("""\
        <html><head><style>
            html {
                background-color: #eee;
            }
            body { 
                font-family: sans-serif;
                max-width: 500px;
                margin: 50px auto;
                font-size: 0.8rem;
            }
            #container {
                border: outset silver 1px;
                background-color: white;
                padding: 50px;
                margin: 0 0 50px 0;
                color: #000;
                font-size: 1rem;
            }
            h1 {
                margin-top: 0;
                text-align: center;
            }
            </style></head>
            <body><div id="container">
            <h1>Flowshutter Wi-Fi Setup</h1>
            <form action="configure" method="post">""")
    for ssid in ssids:
        client.sendall(
            '<div><label><input type="radio" name="ssid" value="' + ssid + '" />' + ssid + '</label></div>')
    client.sendall("""
                <p>
                    Password:
                    <input name="password" type="password" />
                    <input type="submit" value="Submit" />
                </p>
            </form>
            </div>
            <p>
                Your ssid and password information will be saved into the
                """ + NETWORK_PROFILES + """ file in your flowshutter device for OTA udpate and other future usages.
                Be careful about security!
            </p>
        </body></html>
    """)
    client.close()

def handel_configure(client, content):
    match = ure.search("ssid=([^&]*)&password=(.*)", content)

    if match is None:
        send_response(client, "Parameters not found", status_code=400)
        return False
    # version 1.9 compatibility
    try:
        ssid = unquote_plus(match.group(1).decode("utf-8"))
        password = unquote_plus(match.group(2).decode("utf-8"))
    except UnicodeEncodeError:
        ssid = unquote_plus(match.group(1))
        password = unquote_plus(match.group(2))

    if len(ssid) == 0:
        send_response(client, "SSID must be provided", status_code=400)
        return False

    if do_connect(ssid, password):
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
        send_response(client, response)
        try:
            profiles = read_profiles()
        except OSError:
            profiles = {}
        profiles[ssid] = password
        write_profiles(profiles)

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
        send_response(client, response)
        return False

def handle_not_found(client, url):
    send_response(client, "Path not found: {}".format(url), status_code=404)

def up():
    vram.wlan_state = "CONNECTED"
    wlan = WIFIManager().get_connection()
    if wlan is None:
        print("Could not niitialized the network connection.")
        while True:
            pass
    print("Flowshutter OK")
    # vram.oled_need_update = "yes"

def down():
    vram.wlan_state = "DISCONNECTED"
    wlan_ap.active(False)
    wlan_sta.active(False)
    # vram.oled_need_update = "yes"
