import time
import requests
import datetime
import RPi.GPIO as GPIO


def execute(_gpio, _on):
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(_gpio, GPIO.OUT)
    GPIO.output(_gpio, GPIO.HIGH if _on else GPIO.LOW)


def main(BASE):
    now = datetime.datetime.utcnow()
    url = BASE + "/command"
    resp = requests.get(url=url)
    data = resp.json()
    _gpio = 11  # data["hardware"]["gpio"]
    _conf = True  # data["confgiguration"]["name"]

    for command in data:
        print(command)
        if command["schedule_id"] is not None:  # != null
            url = BASE + "/schedule/" + str(command["schedule_id"])
            resp = requests.get(url=url)
            schedule = resp.json()
            schedule_time = datetime.datetime.strptime(schedule["time"], '%H:%M')
            execution_time = datetime.datetime(now.year, now.month, now.day, schedule_time.hour, schedule_time.minute)
            weekday = execution_time.today().weekday()
            days = binary_to_position(bin(schedule["days"]))
            if weekday in days and execution_time <= now:
                    print("execute")
                    execute(_gpio = _gpio, _on=_conf)
        else:  # immediate command
            datetime_object = datetime.datetime.strptime(command["updateAt"], '%a, %d %b %Y %H:%M:%S %Z')
            if datetime_object <= now:
                print("I am older")
                # EXECUTE METHOD
                execute(_gpio=_gpio, _on=_conf)


def binary_to_position(binary):
    positions = []
    for index, digit in enumerate(binary):
        if index in [0, 1]:
            continue
        if int(digit) == 1:
            positions.append(index-2)
    return positions


if __name__ == '__main__':
    SECONDS = 2
    BASE = 'http://127.0.0.1:5000'
    while True:
        main(BASE)
        time.sleep(SECONDS)
