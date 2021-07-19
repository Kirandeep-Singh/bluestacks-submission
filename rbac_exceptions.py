class invaliduser(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__("Username is Invalid. No Such User Exists.Please Try Again...")

class invalidpassword(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__("Incorrect Password is entered. Please Try Again...")

class invalidinput(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__("invalid input chosen. please choose from above options only.")