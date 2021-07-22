from machine import RTC
import time  # import library called time
import json

# Store data in a .JSON file.
# This is great since we later have the option to analyze and use all the data for calculations.


def store_file_json_new(pretty_status, low_sensitivity_sensor, high_sensitivity_duration, shake_readings, calibrated_data):
    try:
        FILENAME = 'data.json'
        new = False
        try:
            f = open(FILENAME, "r")
            HAS_FILE = True
            f.close()
        except:  # open failed
            HAS_FILE = False
        if not HAS_FILE:
            new = True
            my_list = []
        else:
            with open(FILENAME, 'r+') as file:
                my_list = json.loads(file.read())
        with open(FILENAME, 'w+') as file:
            entry = {
                'pretty_status': pretty_status, # Pretty status
                'low_sensitivity_value': low_sensitivity_sensor, # Raw value from the low sensor 
                'high_sensitivity_duration': high_sensitivity_duration, # Raw duration value
                'shake_readings': shake_readings, # Same as duration, 1 == 100ms
                'low_sensor_score': calibrated_data['low_sensor_score'], # Calibrated score of the low sensor
                'high_sensor_score': calibrated_data['high_sensor_score'], # Calibrated score of the high sensor
                'calibrated_score': calibrated_data['calibrated_score'], # Low+high sensor calibrated together.
                'time': str(time.localtime())
            }
            my_list.append(entry)
            jsonString = json.dumps(my_list)
            file.write(jsonString)
    except Exception as e:
        print(e)

# Read the .JSON data file. This is for debugging.
def read_json():
    FILENAME = 'data.json'
    with open(FILENAME, 'r+') as fp:
        d = fp.read()
        print(d)

#  For testing so that we don't have to shake the LoPy4 too much :)
def rand_val(x, y):
    sub = y-x
    random = int(time.time()*1000)
    random %= sub
    random += x
    return random

# Set the time using a NTP server from Netnod
def set_time():
    
    print("inquire RTC time")
    rtc = RTC()
    rtc.ntp_sync(server="gbg1.ntp.netnod.se")

    timeout = 10
    for _ in range(timeout):
        if rtc.synced():
            break
        print("Waiting for rtc time")
        time.sleep(1)

    if rtc.synced():
        print("Time fetched: ", rtc.now())
    else:
        print("could not get NTP time")

    return rtc
