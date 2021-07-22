## Data is sent to Pybytes. Needs to flashed with Pybyte firmware
from machine import Pin
from machine import ADC
import time  # import library called time
import pycom  # import library called pycom
import json # import json
import ssl # import ssl
import functions # import our functions file
import sensors # import sensors file
import algorithm # import the algorithm

# Making sure the "connection" to pybytes is activated
pycom.pybytes_on_boot(True)

# Set time using NTP server
rtc = functions.set_time()

VibSensorPin = 'P16' # Knock sensor connected to P16. Valid pins are P13 to P20.
VibSensorPinHigh = 'P13'  # Vibration sensor connected to P13. Valid pins are P13 to P20.

Pin(VibSensorPin, mode=Pin.IN)  # set up pin mode to input
Pin(VibSensorPinHigh, mode=Pin.IN)  # set up pin mode to input

# create an ADC object bits=10 means range 0-705 the lower value the more vibration detected
adc = ADC(bits=10)

# create analog pins on P16 and P13;
# attn=ADC.ATTN_11DB measures voltage from 0.1 to 3.3v
apin = adc.channel(attn=ADC.ATTN_11DB, pin=VibSensorPin) # Low sensitivity sensor
apin_high = adc.channel(attn=ADC.ATTN_11DB, pin=VibSensorPinHigh) # High sensitivity sensor


if __name__ == '__main__':
    # Loop forever
    while True:
        try:
            # Do one initial reading. If we don't detect anything here then we continue waiting for something to happen
            low_sensitivity_sensor = apin()   # analog value, low sensitivity sensor
            high_sensitivity_sensor = apin_high() # analog value, high sensitivity sensor

            # Everything above 600 is too little to care about. Ignoring that.
            # Everything below 20 (high sensitivty) is also too little/nothing. We ignore that as well.
            if low_sensitivity_sensor < 650 or high_sensitivity_sensor > 20:
                print("Detected a shock! Running application")

                #  Get data from the high sensititivty sensor
                data = sensors.detect_duration_of_shake(apin_high)
                high_sensitivity_duration = data[0] # Duration in MS of the vibration
                shake_readings = data[1] # How many times during the function did we get a value above 0 indicating vibration is occuring.

                # Get data from the low sensitivity sensor
                low_sensitivity_sensor = sensors.detect_shock_value(apin)

                # Get a calibrated value using the two sensors
                calibrated_data = algorithm.vibration_formula(
                    low_sensitivity_sensor, shake_readings)


                if calibrated_data['calibrated_score'] > 650:
                    pretty_status = "SICK"
                    signal = 1
                elif calibrated_data['calibrated_score'] > 500:
                    pretty_status = "BIG"
                    signal = 2
                elif calibrated_data['calibrated_score'] > 300:
                    pretty_status = "Medium"
                    signal = 3
                else:
                    pretty_status = "Light"
                    signal = 4

                # Store data, read data. For testing mainly
                functions.store_file_json_new(
                    pretty_status, low_sensitivity_sensor, high_sensitivity_duration, shake_readings, calibrated_data)
                # functions.read_json()


                # Console printing
                print("-------------------------", pretty_status," shock!-------------------------")
                print("Raw value (knock): ", low_sensitivity_sensor)
                print("Duration of shake: ",high_sensitivity_duration)
                print("Low sensor score: ",calibrated_data['low_sensor_score'])
                print("High sensor score: ",calibrated_data['high_sensor_score'])
                print("Calibrated score: ",calibrated_data['calibrated_score'])

                #C = Calibrated value, using the formula above and combining the readings of the two sensors. This is defined in algorithm.py
                #C = Right now more emphasis is put on the low sensivity sensors which mean that we increase how much we care about the shock of the impact and less about the impact duration
                #R = Raw data from the knock sensor, this detects how hard the impact is. Did we drop it from 10 cm height or from 2 meter height?
                #D = Duration from the vibration sensor, for how long did the impact last? Did it rattle around?

                # Pybytes send
                pybytes.send_signal(
                    signal, 
                    ""+pretty_status+": C: "+str(calibrated_data['calibrated_score'])+"/R: "+str(low_sensitivity_sensor)+"/D: "+str(round(high_sensitivity_duration))+"ms")

                #  Sleep after a impact to give the machine time to reset.
                time.sleep(1)

        except Exception as e:
            print(str(e))
