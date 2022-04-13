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
import hashlib, json, os

sha1_hash = hashlib.sha1()
files = os.listdir("src/")

# print(files)
jtext = {"files":[]}

for f in files:
    with open("src/"+f,"rb") as hf:
        for byte_block in iter(lambda: hf.read(4096),b""):
            sha1_hash.update(byte_block)
        # print(f,sha1_hash.hexdigest()) # for debug
        jtext["files"].append({"name":f,"sha1":sha1_hash.hexdigest()})

jdata = json.dumps(jtext,indent = 4, separators=(',', ': '))
print("SHA1 of all files generated!")
jfile = open("src/sha.json","w")
jfile.write(jdata)
jfile.close()
print("Update sha.json success!")
