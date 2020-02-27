import requests
from config import Config


class BearerAuth(requests.auth.AuthBase):
    def __init__(self):
        self.token = Config.TOKEN

    def __call__(self, r):
        r.headers["authorization"] = "Bearer " + self.token
        return r


def register():
    data = {
        "name": Config.INIT_NAME
    }
    response = requests.post(Config.BASE + "/raspberry", json=data).json()
    Config.ID = response["object"]["id"]

    with open("token.txt", "w") as f:
        f.write(str(Config.ID) + "\n")

    print(response)


def login():
    if Config.ID == -1:
        register()
    data = {
        "raspberry_id": Config.ID
    }
    response = requests.post(Config.BASE + "/login", json=data).json()
    Config.TOKEN = response["access_token"]

    with open("token.txt", "a") as f:
        f.write(str(Config.TOKEN))

    print(response)


def get_commands():
    url = Config.BASE + "/command?raspberry_id=" + str(Config.ID)
    resp = requests.get(url=url, auth=BearerAuth())
    commands = resp.json()
    return commands


def get_schedule(_id):
    url = Config.BASE + "/schedule/" + str(_id)
    resp = requests.get(url=url, auth=BearerAuth())
    schedule = resp.json()
    return schedule


def get_hardware(_id):
    url = Config.BASE + "/hardware/" + str(_id)
    resp = requests.get(url=url, auth=BearerAuth())
    hardware = resp.json()
    return hardware


def post_response(data):
    response = requests.post(Config.BASE + "/response", json=data, auth=BearerAuth()).json()
    print(response)


def put_hardware(hw_id, is_on):
    data = {
        "status": is_on
    }
    response = requests.put(Config.BASE + "/hardware/" + str(hw_id), json=data, auth=BearerAuth()).json()
    print(response)
