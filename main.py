import time
import requests
import datetime
import RPi.GPIO as GPIO


def execute(_gpio, _on):
    """

    :param _gpio: the GPIO pin connected
    :param _on: Whether to make it high or low
    """
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(_gpio, GPIO.OUT)
    GPIO.output(_gpio, GPIO.LOW)
    time.sleep(0.5)
    GPIO.output(_gpio, GPIO.HIGH)
    time.sleep(0.5)


def main(BASE):
    now = datetime.datetime.utcnow()  # today's datetime

    # GET all commands from server and save it in data variable
    url = BASE + "/command"
    resp = requests.get(url=url)
    data = resp.json()

    # TODO: take the gpio and conf values from each command
    _gpio = 11  # data["hardware"]["gpio"]
    _conf = True  # data["confgiguration"]["name"]

    for command in data:  # looping through commands
        if command["schedule_id"] is not None:  # if the command is scheduled (i.e. schedule_id != null)
            # GET schedule/<id> from the server and save it in schedule variable
            url = BASE + "/schedule/" + str(command["schedule_id"])
            resp = requests.get(url=url)
            schedule = resp.json()
            # the schedule has a time string (e.x. "9:45") and an integer from 0-126 representing the binary days
            schedule_time = datetime.datetime.strptime(schedule["time"], '%H:%M')  # time stirng into datetime object
            # turn the time string into today's date with the time given
            execution_time = datetime.datetime(now.year, now.month, now.day, schedule_time.hour, schedule_time.minute)
            # find today's weekday (e.x. sun, mon, tues)
            weekday = execution_time.today().weekday()
            # return the days of execution from the schedule
            days = binary_to_position(bin(schedule["days"]))
            # if the weekday is part of the execution days and the time is before now
            if weekday in days and execution_time <= now:
                    execute(_gpio=_gpio, _on=_conf)  # execute
        else:  # immediate command
            # turn updateAt from string into datetime
            datetime_object = datetime.datetime.strptime(command["updateAt"], '%a, %d %b %Y %H:%M:%S %Z')
            if datetime_object <= now:  # if the execution time before now
                # EXECUTE METHOD
                execute(_gpio=_gpio, _on=_conf)


def binary_to_position(binary):
    """
    :param binary:
    :return: array of positions on
    This method takes the binary string that has 7 bits representing the weekdays from monday to sunday
    if the bit is equal to 1, it means that day is an execution day and thus added to the list
    """
    positions = []
    for index, digit in enumerate(binary):
        if index in [0, 1]:
            continue
        if int(digit) == 1:
            positions.append(index-2)
    return positions


if __name__ == '__main__':
    SECONDS = 2  # Time before next request (30 sec in report)
    BASE = 'http://127.0.0.1:5000'  # web server's URL
    while True:
        main(BASE)
        time.sleep(SECONDS)  # Time loop
