from rbac_exceptions import *

class CredMain:

    def __init__(self, username, password, propobj) -> None:
        self.__username = username
        self.__password = password
        self.__propobj = propobj
    
    def validate(self):
        if not self.__propobj.getprop("user_" + self.__username):
            raise invaliduser
        else:
            if self.__propobj.getprop("pass_" + self.__username) != self.__password:
                raise invalidpassword
            else:
                self.__setvals()
                self.__setmenu()
                return True

    def __setvals(self):
        print ("Entered the setvals")
        self.roles = self.__propobj.getprop("roles_" + self.__username).split(",")
        self.resources = set()
        for role in self.roles:
            role_resources = self.__propobj.getprop("role_" + role).split(",")
            for rsrc in role_resources:
                self.resources.add(rsrc)
    
    def __setmenu(self):
        if self.__username == "admin":
            self.allusers = self.__propobj.getprop(keyname="user", multi=True)
            self.allroles = self.__propobj.getprop(keyname="role", multi=True)
            self.menu = ["Wecome to admin Tasks.", "1). Create New User.", "2). Create New Role.", "3). Edit a User.", "4). Edit a Role.", "5). View All users", "6). View All Roles!!", "0). Exit!!"]
            self.menumap = {1:"createuser", 2:"createrole", 3:"edituser", 4:"editrole", 5:"viewusers", 6:"viewroles", 0:"exit"}
        else:
            self.menu = ["Wecome to user Tasks." "1). View Your permissions/roles.", "2). Access a resource.", "0). Exit!!"]
            self.menumap = {1:"viewperm", 2:"access", 0:"exit"}
    
    def execute(self, task):
        pass
    

class AdminTasks(CredMain):
    def __init__(self, username, password, propobj, task) -> None:
        self.__task = task
        super().__init__(username, password, propobj)
        self.__setvals() 
        self.__setmenu()
    



class NormalUserTasks(CredMain):
    def __init__(self, username, password, propobj, task) -> None:
        self.__task = task
        super().__init__(username, password, propobj)
        self.__setvals()
        self.__setmenu()