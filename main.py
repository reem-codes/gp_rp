import datetime
import time
from config import Config, config_extract
import RPi.GPIO as GPIO
import api_calls as api


def execute(_gpio, _on, command_id):
    """

    :param _gpio: the GPIO pin connected
    :param _on: Whether to make it high or low
    """
    print("I'm executing..")
    print(_gpio, _on)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(_gpio, GPIO.OUT)
    GPIO.output(_gpio, GPIO.LOW if _on else GPIO.HIGH)
    # time.sleep(0.5)
    # GPIO.output(_gpio, GPIO.HIGH)
    # time.sleep(0.5)
    res = {"isDone": True,
           "message": "command executed successfully",
           "executionTime": datetime.datetime.now().strftime('%a, %d %b %Y %H:%M:%S %Z'),
           "command_id": command_id
           }
    api.post_response(res)


def main():
    now = datetime.datetime.now()  # today's datetime

    # GET all commands from server and save it in data variable
    data = api.get_commands()

    for command in data:  # looping through commands
        _gpio = api.get_hardware(command["hardware_id"])["gpio"]
        _conf = command["configuration"]
        command_id = command["id"]

        if command["schedule_id"] is not None:  # if the command is scheduled (i.e. schedule_id != null)
            # GET schedule/<id> from the server and save it in schedule variable
            schedule = api.get_schedule(str(command["schedule_id"]))
            # the schedule has a time string (e.x. "9:45 AM") and an integer from 0-126 representing the binary days
            schedule_time = datetime.datetime.strptime(schedule["time"], '%I:%M %p')  # time string into datetime object
            # turn the time string into today's date with the time given
            execution_time = datetime.datetime(now.year, now.month, now.day, schedule_time.hour, schedule_time.minute)
            # find today's weekday (e.x. sun, mon, tues)
            weekday = execution_time.today().weekday()
            # return the days of execution from the schedule
            days = binary_to_position(bin(schedule["days"]))
            # if the weekday is part of the execution days and the time is before now
            if weekday in days and execution_time <= now:
                execute(_gpio=_gpio, _on=_conf, command_id=command_id)  # execute
        else:  # immediate command
            # turn updateAt from string into datetime
            datetime_object = datetime.datetime.strptime(command["updateAt"], '%a, %d %b %Y %H:%M:%S %Z')
            if datetime_object <= now:  # if the execution time before now
                # EXECUTE METHOD
                execute(_gpio=_gpio, _on=_conf, command_id=command_id)


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
    config_extract()
    if Config.ID == -1:
        api.register()
    if Config.TOKEN == "":
        api.login()
    while True:
	main()
	time.sleep(Config.SECONDS)
# while True:
# main(Config.BASE)
# time.sleep(Config.SECONDS)  # Time loop
