class PropFileOperation:
    def __init__(self, filepath) -> None:
        self._file = filepath
        self.propupd("users", "admin", append=True )
        self.propupd("pass_admin", "Kiran@123")
        self.propupd("roles_admin", "super")
        self.propupd("role_read", "read_vm,read_jobs")
        self.propupd("role_write", "create_vm,read_vm,create_jobs,read_jobs")
        self.propupd("role_super", "all")
        self.propupd("allroles", "read", append=True)
        self.propupd("allroles", "write", append=True)
        self.propupd("allroles", "super", append=True)
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

    def propupd(self, keyname, value, append=False) -> bool:
        try:
            tmp = self._readpropfile()
            if not tmp:
                tmp = {}
            if append and keyname in tmp.keys():
                x = tmp[keyname].split(",")
                x.append(value)
                tmp[keyname] = ",".join(set(x))
            else:
                tmp[keyname] = value
            # print (tmp)
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

