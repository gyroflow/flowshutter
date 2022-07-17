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
import hashlib
import json
import shutil
import sys

def move(argv):
    modules = []
    for subdir, dirs, files in os.walk('src'):
        for file in files:
            filepath = subdir + '/' + file
            modules.append(filepath)
    temp = {x.replace('src/','').replace('src\\','')
            .replace('gui\\','gui/').replace('protocols\\','protocols/')
            for x in modules}
    modules = temp

    modules.remove('__init__.py')

    if argv == 'COMPLIE':
        try:
            # these files should/can not be compiled as frozen modules
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
        try:
            shutil.copyfile('src/'+f, 'obj/'+f)
            print('CP '+f+' ..')
        except FileNotFoundError:
            # print(f)
            try:
                os.mkdir(path='obj/'+f.split('/')[0])
                shutil.copyfile('src/'+f, 'obj/'+f)
                print('CP '+f+' ..')
            except FileExistsError:
                os.mkdir(path='obj/'+f.split('/')[0]+"/"+f.split('/')[1])
                shutil.copyfile('src/'+f, 'obj/'+f)
                print('CP '+f+' ..')
            except FileNotFoundError:
                os.mkdir(path='obj/'+f.split('/')[0]+"/"+f.split('/')[1])
                shutil.copyfile('src/'+f, 'obj/'+f)
                print('CP '+f+' ..')

    try:
        shutil.rmtree(path='obj/__pycache__')
        print('RM '+'obj/__pycache__')
        shutil.rmtree(path='obj/protocols/__pycache__')
        print('RM '+'obj/protocols/__pycache__')
    except FileNotFoundError:
        pass

def build(argv1, argv2):
    # create obj folder
    try:
        print('MKDIR obj ..')
        os.mkdir('obj')
        print('obj/ created')
    except:
        print('obj/ already exists')
        pass

    if argv1 == 'COMPLIE':
        # copy necessary modules
        prefix_modules = os.listdir('build/')
        print('..\nCOPY prefix')
        for f in prefix_modules:
            shutil.copyfile('build/'+f, 'obj/'+f)
            print('CP '+f+' ..')
        # copy flowshutter modules
        move(argv1)
    elif argv1 == 'DEBUG':
        # copy flowshutter modules
        move(argv1)

    print('RG '+ argv2 + ' ..')
    target_address ='obj/target.py'
    if argv2 == 'GENERIC':
        source_address = 'obj/targets/generic.py'
    elif argv2 == 'DIY_CARD':
        source_address = 'obj/targets/diy_card.py'
    elif argv2 == 'DIY_FC':
        source_address = 'obj/targets/diy_fc.py'
    elif argv2 == 'NEUTRONRC_SDB':
        source_address = 'obj/targets/neutronrc_sdb.py'
    elif argv2 == 'G12864':
        source_address = 'obj/targets/g12864.py'
    else:
        print('ERROR: target not found')
        sys.exit()

    print('CP '+source_address+' to '+target_address)
    shutil.copyfile(source_address, target_address)
    print('RG '+ argv2 + ' success')

def gen_sha(jdir):
    modules = []
    for subdir, dirs, files in os.walk('obj'):
        for file in files:
            filepath = subdir + '/' + file
            modules.append(filepath)
    temp = {x.replace('obj/','').replace('obj\\','').replace('\\','/') for x in modules}
    files = temp
    files = sorted(files)
    files.remove('sha.json')
    files.remove('target.py')
    # print(files)

    jtext = {'files':[]}

    for f in files:
        with open('obj/'+f, 'rb') as hf:
            for byte_block in iter(lambda: hf.read(4096), b''):
                sha1 = hashlib.sha1()
                sha1.update(byte_block)
            jtext["files"].append({"name":f,"sha1":sha1.hexdigest()})
        del sha1
    jdata = json.dumps(jtext,indent = 4, separators=(',', ': '))
    print("SHA1 of all files generated!")

    jfile = open(jdir,"wb")
    jfile.write(bytes(jdata, "utf-8"))
    jfile.close()

if __name__ == '__main__':
    if len(sys.argv) == 1:
        # `build.py`
        build('COMPLIE','GENERIC')
    else:
        if sys.argv[1] == 'build':
            # `build.py build`
            if len(sys.argv) == 2:
                print('Build started!')
                build('COMPLIE','GENERIC')
                print('Build complete!')
            elif sys.argv[2] == 'TARGET':
                # `build.py build TARGET XXXX`
                target = sys.argv[3]
                print('Build started!')
                build('COMPILE', target)
                print('Build complete!')

        elif sys.argv[1] == 'debug':
            # `build.py debug`
            if len(sys.argv) == 2:
                print('Preparing for debug mode...')
                build('DEBUG','GENERIC')
                print('Debug ready!')
            elif sys.argv[2] == 'TARGET':
                # `build.py debug TARGET XXXX`
                target = sys.argv[3]
                print('Preparing for debug mode...')
                build('DEBUG', target)
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

        elif sys.argv[1] == 'sha':
            # `build.py sha`
            if len(sys.argv) == 2:
                print('Updating SHA...')
                build('DEBUG','GENERIC')
                gen_sha('src/sha.json')
                print('SHA update success!')
            elif sys.argv[2] == 'build':
                # `build.py sha build`, for CI
                print('Generating check SHA...')
                build('DEBUG','GENERIC')
                gen_sha('check_sha.json')
                print('Check SHA generated!')
            elif sys.argv[2] == 'verify':
                # `build.py sha verify`, verify sha.json and check_sha.json
                f1 = open("check_sha.json","r").read()
                f2 = open("src/sha.json","r").read()
                if f1 == f2:
                    # sha.json is already updated with the changes
                    pass
                else:
                    raise Exception("'sha.json' is outdated! Please run 'python tools/gen_sha.py' to update!")
                print("SHA verify success!")
            elif sys.argv[2] == 'clean':
                # `build.py sha clean`, clean sha.json and check_sha.json
                # for development testing
                os.remove("check_sha.json")
                print("Extra SHA cleaned!")

        elif sys.argv[1] == 'clean':
            # `build.py clean`
            print('Performing full clean')
            try:
                shutil.rmtree('obj')
                print('Full clean completed!')
            except:
                print('obj does not exist, no need to clean.')

        else:
            print('Invalid Command!\n')
            print('- `build.py build`               for building generic target modules\n')
            print('- `build.py build TARGET XXX`    for building specific target modules\n')

            print('- `build.py debug`               for preparing generic target modules for debug mode\n')
            print('- `build.py debug TARGET XXX`    for preparing specific target modules for debug mode\n')
            print('- `build.py debug clean`         for cleaning files on the device\n')

            print('- `build.py sha`                 for updating SHA\n')
            print('- `build.py sha build`           for generating check SHA\n')
            print('- `build.py sha verify`          for verifying SHA\n')
            print('- `build.py sha clean`           for removing check SHA\n')

            print('- `build.py clean`               for full clean\n')
