class invaliduser(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__("Invalid Username is provided. No such user")

class invalidpassword(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__("Incorrect Password is supplied.")

class invalidinput(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__("invalid input chosen. please choose from above options only.")