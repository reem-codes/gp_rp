import uuid


class Config:
    TOKEN = ""
    INIT_NAME = str(uuid.uuid4())
    ID = -1
    SECONDS = 2  # Time before next request (30 sec in report)
    BASE = 'https://gp.reem-codes.com'  # web server's URL


def config_extract():
    with open("token.txt") as f:
        data = f.read().split("\n")
        if len(data) == 2:
            Config.ID = data[0]
            Config.TOKEN = data[1]
            print(Config.ID)
            print(Config.TOKEN)
