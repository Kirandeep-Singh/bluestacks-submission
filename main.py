from propfileoperation import PropFileOperation
from rbac_logic import CredMain
from rbac_exceptions import *
import sys, getpass
pfile = ".kd_rbac_data"
propobj = PropFileOperation(pfile)


# user, password = "admin", "Kiran@123"
# user, password = "kirandeep", "kirandeep"

while True:
    user = input("Enter User Name:")
    password = getpass.getpass("Enter Password:")
    try:
        credobj = CredMain(user, password, propobj)
        credobj.validate()
    except invaliduser as E:
        print (E)
    except invalidpassword as E:
        print (E)
    else:
        print ("Password entered is correct. You have logged in as {}".format(user))
        break

while True:
    try:
        for line in credobj.menu:
            print (line)
        selection = int(input("Choose from above options!!!"))
        if selection not in [x for x in range(len(credobj.menu) - 1)]:
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
                status = credobj.execute(selection)
            except Exception as E:
                print (E)
                print ("Exception in execute")
            else:
                proceedconsent = input("Selected Task is Done.\nDo you want to do something more1? (yes/no): ")
                if proceedconsent.lower() in ("yes", "y"):
                    continue
                elif proceedconsent.lower() in ("no", "n"):
                    print ("user Chose to Exit.")
                    sys.exit(0)
                else:
                    print ("invalid value chosen!!! Exiting...")
                    sys.exit(0)

