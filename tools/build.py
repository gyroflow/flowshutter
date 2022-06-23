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
import os
import shutil
import sys

def build():
    try:
        print('MKDIR obj ..')
        os.mkdir("obj")
        print('obj/ created')
    except:
        pass

    prefix_modules = os.listdir("build/")
    print('..\nCOPY prefix')
    for f in prefix_modules:
        shutil.copyfile('build/'+f, 'obj/'+f)
        print('CP '+f+' ..')

    modules = os.listdir("src/")

    try:
        # these files should/can not be compiled as frozen modle
        modules.remove("boot.py")
        modules.remove("LICENSE")
        modules.remove("main.py")
        modules.remove("README.md")
        modules.remove("sha.json")
    except ValueError:
        pass

    modules = sorted(modules)
    print('..\nCOPY modules')
    for f in modules:
        shutil.copyfile('src/'+f, 'obj/'+f)
        print('CP '+f+' ..')

if len(sys.argv) == 1:
    build()
else:
    if sys.argv[1] == "clean":
        print('Performing full clean')
        try:
            shutil.rmtree('obj')
            print('Full clean completed!')
        except:
            print('obj does not exist, no need to clean.')
    elif sys.argv[1] == "build":
        print('Build started!')
        build()
        print('Build complete!')
    else:
        print('Invalid Command!\n')
        print('- `build.py` or\n  `build.py build` for building modules\n')
        print('- `build.py clean` for full clean\n')
