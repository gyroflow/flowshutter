# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
#import webrepl
#webrepl.start()
import os, json

def update_files():
    new_f_flag = False
    del_f_flag = False

    try: # update new files
        with open("update_list.json", "r") as f:
            update_list = json.load(f)
            f.close()
            print("there are new files")
            # for i in range(0,len(update_list['files'])):
            #     os.rename("tmp/"+str(update_list['files'][i]['name']), str(update_list['files'][i]['name']))
            # os.remove("update_list.json")
            # os.rmdir("tmp")
            new_f_flag = True
    except:
        print("no new file")
        pass

    try:
        with open("delete_list.json", "r") as f:
            delete_list = json.load(f)
            f.close()
            print("there are some outdated files")
            # for i in range(0,len(delete_list['files'])):
            #     os.remove(str(delete_list['files'][i]['name']))
            # os.remove("delete_list.json")
            del_f_flag = True
    except:
        print("no outdate file")
        pass

    if new_f_flag == True or del_f_flag == True:
        print("hey we supposed to remove the project.pymakr")
        # try:
        #     os.remove("project.pymakr")
        # except:
        #     print("Already removed")
    
    print("update flag: "+str(new_f_flag))
    print("delete flag: "+str(del_f_flag))


update_files()
print(os.listdir())
