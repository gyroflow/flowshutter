# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
#import webrepl
#webrepl.start()
import os, json

def update_files():
    new_f_flag = False
    del_f_flag = False

    try:
        with open("delete_list.json", "r") as f:
            delete_list = json.load(f)
            f.close()
            print("there are some outdated files")
            for i in range(0,len(delete_list['files'])):
                os.remove(str(delete_list['files'][i]['name']))
                print(str(delete_list['files'][i]['name']) + " deleted")
            os.remove("delete_list.json")
            print("delete_list.json removed")
            del_f_flag = True
    except:
        print("no outdate file")
        pass


    try: # update new files
        with open("update_list.json", "r") as f:
            update_list = json.load(f)
            f.close()
            print("there are new files")
            for i in range(0,len(update_list['files'])):
                os.rename("tmp/"+str(update_list['files'][i]['name']), str(update_list['files'][i]['name']))
                print(str(update_list['files'][i]['name']) + " updated")
            os.remove("update_list.json")
            print("update_list.json removed")
            os.rmdir("tmp")
            print("tmp dir removed")
            new_f_flag = True
    except:
        print("no new file")
        pass


    if new_f_flag == True or del_f_flag == True:
        print("hey we supposed to remove the project.pymakr and old sha.json")

        os.remove("sha.json")
        os.rename("tmp_sha.json","sha.json")
        print("sha.json updated")
        try:
            os.remove("project.pymakr")
        except:
            print("Already removed")

    print("delete flag: "+str(del_f_flag))
    print("update flag: "+str(new_f_flag))


update_files()
print(os.listdir())
