from os import curdir
from rbac_exceptions import *
import re, getpass

class CredMain:

    def __init__(self, username, password, propobj) -> None:
        self._username = username
        self._password = password
        self._propobj = propobj
    
    def validate(self):
        if self._username not in self._propobj.getprop("users").split(","):
            raise invaliduser
        else:
            if self._propobj.getprop("pass_" + self._username) != self._password:
                raise invalidpassword
            else:
                self._setvals()
                self._setmenu()
                return True

    def _setvals(self):
        self.resources = set()
        self.roles = self._propobj.getprop("roles_" + self._username).split(",")
        if "super" in self.roles:
            role_resources = self._propobj.getprop("resources").split(",")
            for rsrc in role_resources:
                self.resources.add(rsrc)
        else:
            for role in self.roles:
                role_resources = self._propobj.getprop("role_" + role).split(",")
                for rsrc in role_resources:
                    self.resources.add(rsrc)
    
    def _setmenu(self):
        if self._username == "admin":
            self.allusers = self._propobj.getprop(keyname="users").split(",")  #List
            self.allroles = self._propobj.getprop(keyname="allroles").split(",")  #List
            self.allresources = self._propobj.getprop(keyname="resources").split(",")  #List
            self.menu = ["Wecome to admin Tasks.", "1). Create New User.", "2). Create New Role.", "3). Edit a User.", "4). Edit a Role.", "5). View All users", "6). View All Roles!!", "0). Exit!!"]
            # self.menumap = {1:"createuser", 2:"createrole", 3:"edituser", 4:"editrole", 5:"viewusers", 6:"viewroles", 0:"exit"}
        else:
            self.menu = ["Wecome to user Tasks.", "1). View Your permissions/roles.", "2). Access a resource.", "0). Exit!!"]
            # self.menumap = {1:"viewperm", 2:"access", 0:"exit"}
    
    def execute(self, task):
        print ("Entered Execute")
        if self._username == "admin":
            self.__task_obj = AdminTasks(username=self._username, password=self._password, propobj=self._propobj, task=task)
        else:
            self.__task_obj = NormalUserTasks(username=self._username, password=self._password, propobj=self._propobj, task=task)
        return self.__task_obj.run()

    def _changepass(self, user):
        if self._username == "admin":
            checkcurrentpassword = False
        else:
            checkcurrentpassword = True
        
        if checkcurrentpassword:
            curpswd = input("Enter Current Password:")
            if self._propobj.getprop("pass_" + user) != curpswd:
                print ("Invalid Current Password. Try this option again.")
                return False
        
        newpass = self._get_pass()
        if not newpass:
            return False
        else:
            self._propobj.propupd("pass_" + user, newpass)    

    def _get_pass(self):
        x = 0
        while x < 3:
            inputpass = getpass.getpass("Enter New Password:")
            if len(inputpass) < 8:
                print ("Password Must be minimum 8 characters.")
                x+=1
                continue
            elif re.search(r"=", inputpass):
                print ("= is not allowed in password. It's a restricted character. Please enter again.")
                x+=1
                continue
            else:
                return inputpass
        return False

    def _changerole(self,user):
        print ("Welcome to Change Role Utility!!")
        newrole = self._get_roles_or_resources(type="Role")
        if not newrole:
            return False
        self._propobj.propupd("roles_{}".format(user), ",".join(newrole.strip().split(",")))
        
    def _get_user_or_role(self, type="User"):
        x = 0
        while x < 3:
            inputuser = input("Enter {} Name:".format(type))
            if type == "User" and inputuser in self.allusers:
                print("Entered User already exists. Try again.")
                x+=1 
                continue
            elif type == "Role" and inputuser in self.allroles:
                print("Entered Role already exists. Try again.")
                x+=1
                continue
            else:
                if re.match(r"[\w]+$", inputuser):
                    return inputuser
                else:
                    print ("Input is invalid. Please use alphanumeric value. only _ is allowed")
                    x+=1
                    continue
        return False
        
    def _get_roles_or_resources(self, type="Role"):
        x = 0
        if type == "Role":
            z = self.allroles
        else:
            z = self.allresources
        while x < 3:
            inputroles = input("Please input the {0}. Available {0} are [{1}]. Select Multiple values by ','.".format(type, z))
            y = lambda k: k.strip() in z
            if False in list(map(y, inputroles.split(","))):
                print ("Invalid value of {} entered. Please copy paste and separate with ,".format(type))
                x+=1
                continue
            else:
                return inputroles
    
        return False


class AdminTasks(CredMain):
    def __init__(self, username, password, propobj, task) -> None:
        self.__task = task
        super().__init__(username, password, propobj)
        self._setvals() 
        self._setmenu()
    
    def run(self):
        self.menumap = {1:self.createuser, 2:self.createrole, 3:self.edituser, 4:self.editrole, 5:self.viewusers, 6:self.viewroles}
        return self.menumap[self.__task]()
    
    def createuser(self):
        print("Welcome to User Creation Tool!!")
        inputuser = self._get_user_or_role(type="User")
        if not inputuser:
            return False
        inputpass = self._get_pass()
        if not inputpass:
            return False 
        inputroles = self._get_roles_or_resources(type="Role")
        if not inputroles:
            return False
        self._propobj.propupd("users", inputuser, append=True)
        self._propobj.propupd("pass_{}".format(inputuser), inputpass)
        self._propobj.propupd("roles_{}".format(inputuser), ",".join(inputroles.strip().split(",")))
        return True

    def createrole(self):
        print ("Welcome to Create Role Utility!!")
        newrole = self._get_user_or_role(type="Role")
        if not newrole:
            return False
        rsrc = self._get_roles_or_resources(type="Resources")
        if not rsrc:
            return False
        self._propobj.propupd("allroles", newrole, append=True)
        self._propobj.propupd("role_{}".format(newrole), ",".join(rsrc.strip().split(",")))

    def edituser(self):
        print("Welcome to User Creation Tool!!")
        while True:
            inputuser = input("Enter the Username you want to modify:")
            if inputuser not in self.allusers:
                print("Invalid username entered. No such user exists.")
                continue
            else:
                break
        
        print ("Choose 1 from Options Below:\n1). Change Password\n2). Change role\n")
        optionmap = {1:self._changepass, 2:self._changerole}
        while True:
            try:
                useroption = int(input("Choose Option:"))
                if useroption not in (1,2):
                    raise invalidinput
            except ValueError:
                print ("Enter an integer only.")
                continue
            except invalidinput:
                print ("Choose from above options only.")
            else:
                print ("You have Chosen Option {}".format(useroption))
                return optionmap[useroption](inputuser)

    def editrole(self):
        print("Welcome to User Creation Tool!!")
        x = 0
        while x < 3:
            role = input("Enter the Role you want to modify {}:".format(self.allroles))
            if role not in self.allroles:
                print("Invalid Role entered. No such role exists.")
                x+=1
                continue
            else:
                break
        
        rsrc = self._get_roles_or_resources(type="Resources")
        if not rsrc:
            return False
        else:
            self._propobj.propupd("role_{}".format(role), ",".join(rsrc.strip().split(",")))

    def viewusers(self):
        print ("Below Users currently exist on System.\n{}".format(self.allusers))
        return True

    def viewroles(self):
        x = [x + "\t\t" + self._propobj.getprop("role_{}".format(x)) for x in self.allroles]
        print ("Below Roles currently exist on System.\nRole Name\tResources Associated\n{}".format("="*30))
        for line in x:
            print (line)
        return True


class NormalUserTasks(CredMain):
    def __init__(self, username, password, propobj, task) -> None:
        self.__task = task
        super().__init__(username, password, propobj)
        self._setvals()
        self._setmenu()
    
    def run(self):
        self.menumap = {1:self.__viewperm, 2:self.__access}
        return self.menumap[self.__task]()
    
    def __viewperm(self):
        print ("Your User {} has below permissions.\nRole ==> {}\nResources ==> {}\n".format(self._username, ", ".join(self.roles), ", ".join(self.resources)))

    def __access(self):
        print ("You have requested to access a resource.\nBelow Resources can be accessed from your user.\nChoose the one you want to access.\n")
        x = 1
        for rsrc in self.resources:
            print ("{}).\t {}.".format(x, rsrc))
            x+=1
        print ("Voila!!! This is end of this Code.")
        print ("A User can access only the resources available in his role.\nadmin Can't run these tasks. We must create a non admin user with role super assigned.")