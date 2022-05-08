# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
#import webrepl
#webrepl.start()
import os

# try:
#     os.rename("tmp_sha.json", "sha.json")
#     print("sha files cleaned")
# except:
#     print("No sha file need to be cleaned")

# try:
#     os.remove('tmp/test.json')
# except:
#     print("test.json doesn't exist")

# try:
#     os.rmdir("tmp")
#     print("tmp folder removed")
# except:
#     print("No tmp folder to be removed")

print(os.listdir())
