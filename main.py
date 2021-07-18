from propfileoperation import PropFileOperation
from rbac_logic import CredMain
from rbac_exceptions import *
import sys
pfile = ".kd_rbac_data"
propobj = PropFileOperation(pfile)


user, password = "admin", "Kiran@123"

while True:
    # user = input("Enter User Name:")
    # password = input("Enter Password:")
    try:
        credobj = CredMain(user, password, propobj)
        credobj.validate()
    except invaliduser:
        print ("Username is Invalid. No Such User Exists.Please Try Again...")
    except invalidpassword:
        print ("Incorrect Password is entered. Please Try Again...")
    else:
        print ("Password entered is correct. You have logged in as {}".format(user))
        break

while True:
    try:
        for line in credobj.menu:
            print (line)
        selection = int(input("Choose from above options!!!"))
        if selection not in credobj.menumap.keys():
            raise invalidinput
    except ValueError:
        print ("Only Choose an integer value from given values.")
    except invalidinput:
        print ("Enter from Given values only.")
    else:
        if selection == 0:
            print ("Exiting...")
            sys.exit(0)
        else:
            try:
                credobj.execute(selection)
            except:
                pass
            else:
                print ("Above selected Task is done!!")
                proceedconsent = input("Do you want to Continue? (yes/no): ")
                if proceedconsent.lower() in ("yes", "y"):
                    continue
                elif proceedconsent.lower() in ("no", "n"):
                    print ("user Chose to Exit.")
                    sys.exit(0)
                else:
                    print ("invalid value chosen!!! Exiting...")
                    sys.exit(0)

