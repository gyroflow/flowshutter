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
import hashlib, json, os, sys

files = os.listdir("src/")

try:
    files.remove("sha.json")
except ValueError:
    pass

# sort file list
files = sorted(files)

# print(files)
jtext = {"files":[]}

for f in files:
    with open("src/"+f,"rb") as hf:
        for byte_block in iter(lambda: hf.read(4096),b""):
            sha1 = hashlib.sha1()
            sha1.update(byte_block)
        # print(f,sha1.hexdigest()) # for debug
        jtext["files"].append({"name":f,"sha1":sha1.hexdigest()})
        del sha1

jdata = json.dumps(jtext,indent = 4, separators=(',', ': '))
print("SHA1 of all files generated!")

def write_json(jdir):
    jfile = open(jdir,"w")
    jfile.write(jdata)
    jfile.close()
    

jdir = ""
# print(len(sys.argv)) # for debug
if len(sys.argv) == 1:
    jdir = "src/sha.json"
    write_json(jdir)
    print("Update sha.json success!")
else:
    if sys.argv[1] == "check":
        jdir = "check_sha.json"
        write_json(jdir)
        print("Create check_sha.json success!")
    elif sys.argv[1] == "verify":
        f1 = open("check_sha.json","r").read()
        f2 = open("src/sha.json","r").read()
        if f1 == f2:
            pass
        else:
            raise Exception("'sha.json' is outdated! Please run 'python tools/gen_sha.py' to update!")
        print("SHA verify success!")
