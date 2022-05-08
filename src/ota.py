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
import json, urequests, vars

def build_url(file_name):
    source = ""
    channel = ""

    if vars.ota_source == "GitHub":
        source = "https://raw.githubusercontent.com/gyroflow/flowshutter/"
    elif vars.ota_source == "Gitee":
        source = "https://gitee.com/dusking1/flowshutter/raw/"

    if vars.ota_channel == "stable":
        channel = "stable"
    elif vars.ota_channel == "beta":
        channel = "beta"
    elif vars.ota_channel == "dev":
        channel = "master"
    
    # print("source:" + source)
    # print("channel:" + channel)
    remote_url = source + channel + "/src/" + file_name
    return remote_url

def build_sha_url():
    # https://raw.githubusercontent.com/gyroflow/flowshutter/master/src/sha.json
    # https://gitee.com/dusking1/flowshutter/raw/master/src/sha.json
    remote_sha_url = build_url("sha.json")
    return remote_sha_url


def check():
    remote_sha_url = build_sha_url()
    print("hello! Now trying to get remote SHA...")
    print("remote SHA url: " + remote_sha_url)
    
    #remote_sha = urequests.get(remote_sha_url).json()
    remote_sha = urequests.get(remote_sha_url)
    print("remote SHA downloaded")
    sha_jdata = remote_sha.json()
    #### this is for debugging
    # print(type(remote_sha))
    # print(remote_sha.text)
    with open("tmp_sha.json", "w") as f:
        json.dump(sha_jdata, f)
        print("Saved remote SHA to tmp_sha.json")
        f.close()
    import os
    print(os.listdir())
    compare()
    #### can be removed later

def compare():
    with open("tmp_sha.json", "r") as f_1:
        upstream = json.load(f_1)
        f_1.close()
    with open("sha.json", "r") as f_2:
        local = json.load(f_2)
        f_2.close()
    
    # print("upstream: " + str(upstream))
    # print("local: " + str(local))

    for i in range(1,len(local['files'])):
        # compare local => upstream to get update and delete info
        for j in range(1,len(upstream['files'])):
            if local['files'][i]['name'] == upstream['files'][j]['name']:

                # A file with the same name is found both locally and remotely,
                # check sha1 between the two files
                if local['files'][i]['sha1'] == upstream['files'][j]['sha1']:
                    # They are same, no update is needed
                    print(str(local['files'][i]['name']) + " no change")
                    break
                else:
                    # Local file is outdated, it should be updated
                    print(str(local['files'][i]['name']) + " outdated")
                    break

            elif j == len(upstream['files']) - 1 and local['files'][i]['name'] != upstream['files'][j]['name']:
                # The local file was not found in the remote
                # it should be deleted
                print(str(local['files'][i]['name']) + " deleted")
    
    for i in range(1,len(upstream['files'])):
        # compare upstream => local to get new file info
        for j in range(1,len(local['files'])):
            if upstream['files'][i]['name'] == local['files'][j]['name']:
                # we have checked this before
                break
            elif j == len(local['files']) - 1 and upstream['files'][i]['name'] != local['files'][j]['name']:
                # The remote file was not found in the local
                # It is the new file, which should be downloaded
                print(str(upstream['files'][i]['name']) + " new")
