class PropFileOperation:
    def __init__(self, filepath) -> None:
        self._file = filepath
        self.propupd("user_admin", "admin")
        self.propupd("pass_admin", "Kiran@123")
        self.propupd("roles_admin", "all")
        self.propupd("role_all", "all")
        self.propupd("resources", "create_vm,delete_vm,read_vm,update_vm,create_jobs,update_jobs,delete_jobs,read_jobs")
    
    def _readpropfile(self) -> dict:
        tmp = {}
        try:
            with open(self._file, "r") as f:
                for line in f.readlines():
                    if line.strip():
                        key = line.split("=")[0]
                        val = line.split("=")[1].strip()
                        tmp[key] = val
        except IOError:
            return False
        else:
            return tmp

    def _writepropfile(self, tmp) -> bool:
        with open(self._file, "w+") as f:
            for key, val in tmp.items():
                line = "{}={}".format(key, val) + "\n"
                f.write(line)

    def propupd(self, keyname, value, multi=False) -> bool:
        try:
            tmp = self._readpropfile()
            if not tmp:
                tmp = {}   
            if multi:
                tmp[keyname] = ",".join(value)
            else:
                tmp[keyname] = value
        except Exception as E:
            return False
        else:
            self._writepropfile(tmp)
            return True

    def getprop(self, keyname, multi=False):
        try:
            tmp = self._readpropfile()
            if tmp:
                if multi:
                    x = []
                    for key, value in tmp.items():
                        if key.startswith(keyname):
                            x.append(value)
                    return x
                else:
                    return tmp[keyname]
            else:
                raise KeyError
        except KeyError:
            return None

