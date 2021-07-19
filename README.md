# bluestacks-submission
## RBAC Auth System for BlueStacks screening round.
## 1. Since, No Database is being used, so to make data persistent, I have used a text file (.kd_rbac_data) which is a property file format.
## 2. At First execution, this system will allow user to login with a default login (admin/Kiran@123).
    a. Role means the access type and level.
    b. password must be minimum 8 chars long. = cant be used in password as its being stored in property file as plain text. it can be encrypted with any suitable encryption algo.
    c. Password change feature not implemented for admin user as of now. It can be done with a few modifications if needed.

Details of files are below:
1. **main.py** is the driver code. run this to execute the rbac.
2. **propfileoperation.py** contains class for updating and getting values from property file. It can be modified to update and fetch from DB or any other place.
3. **rbac_exceptions.py** contains the user defined exceptions for this tool.
4. **rbac_logic.py** contains the backend code and classes which are excuted upon selecting an action from main.py

**Clone the Repository.**
**_run main.py, login as **admin/Kiran@123_**
**Following Menu Appears:**
**When user selects the number, appropriate tasks will be executed.**
**Following example shows execution of task6**
_Wecome to admin Tasks._
_1). Create New User._
_2). Create New Role._
_3). Edit a User._
_4). Edit a Role._
_5). View All users_
_6). View All Roles!!_
_0). Exit!!_
_Choose from above options!!!6_
Entered Execute
**Below Roles currently exist on System.**
**Role Name       Resources Associated**
**==============================**
**write           create_vm,read_vm,create_jobs,read_jobs**
**super           all**
**read            read_vm,read_jobs**
**Selected Task is Done.**




