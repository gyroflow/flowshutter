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

def move(argv):
    modules = os.listdir('src/')
    modules.remove('__init__.py')

    if argv == 'COMPLIE':
        try:
            # these files should/can not be compiled as frozen modle
            modules.remove('boot.py')
            print('RM '+'boot.py')
            modules.remove('LICENSE')
            print('RM '+'LICENSE')
            modules.remove('main.py')
            print('RM '+'main.py')
            modules.remove('README.md')
            print('RM '+'README.md')
            modules.remove('sha.json')
            print('RM '+'sha.json')
        except ValueError:
            print('RM error')
            pass
    elif argv == 'DEBUG':
        pass

    modules = sorted(modules)
    print('..\nCOPY modules')
    for f in modules:
        shutil.copyfile('src/'+f, 'obj/'+f)
        print('CP '+f+' ..')

def build(argv):
    # create obj folder
    try:
        print('MKDIR obj ..')
        os.mkdir('obj')
        print('obj/ created')
    except:
        print('obj/ already exists')
        pass

    if argv == 'COMPLIE':
        # copy necessary modules
        prefix_modules = os.listdir('build/')
        print('..\nCOPY prefix')
        for f in prefix_modules:
            shutil.copyfile('build/'+f, 'obj/'+f)
            print('CP '+f+' ..')
        # copy flowshutter modules
        move(argv)
    elif argv == 'DEBUG':
        # copy flowshutter modules
        move(argv)

if __name__ == '__main__':
    if len(sys.argv) == 1:
        build('COMPLIE')
    else:
        if sys.argv[1] == 'clean':
            print('Performing full clean')
            try:
                shutil.rmtree('obj')
                print('Full clean completed!')
            except:
                print('obj does not exist, no need to clean.')
        elif sys.argv[1] == 'build':
            print('Build started!')
            build('COMPLIE')
            print('Build complete!')
        elif sys.argv[1] == 'debug':
            if len(sys.argv) == 2:
                print('Preparing for debug mode...')
                build('DEBUG')
                print('Debug ready!')
            elif sys.argv[2] == 'clean':
                print('Performing clean')
                try:
                    shutil.rmtree('obj')
                    print('Clean completed!')
                except:
                    print('obj does not exist')
                os.mkdir('obj')
                print('Remove ready!')
        else:
            print('Invalid Command!\n')
            print('- `build.py` or\n  `build.py build` for building modules\n')
            print('- `build.py clean` for full clean\n')
            print('- `build.py debug` for debug mode\n')
            print('- `build.py debug clean` for cleaning files on the device\n')
