import time
import requests


def main(BASE):
    url = BASE + "/command"
    resp = requests.get(url=url)
    data = resp.json()
    print(data)
    for command in data:
        if command["schedule_id"] is not None:  # != null
            url = BASE + "/schedule/" + str(command["schedule_id"])
            resp = requests.get(url=url)
            schedule = resp.json()
            print(schedule)
        else:
            print(command["updateAt"])


if __name__ == '__main__':
    SECONDS = 2
    BASE = 'http://127.0.0.1:5000'
    while True:
        main(BASE)
        time.sleep(SECONDS)