import functions
import time
from machine import Timer
	
def detect_duration_of_shake(apin_high):
    # Small shake = 800ms
    # Two small shakes = 1200ms
    # Three smalle shakes = 1600ms
    try:
        # print("Detecting shake duration")
        chrono = Timer.Chrono()
        chrono.start() # Start a timer to record how long it's been shaking for.
        shake_readings = 0
        while True:
            value = 0
            # Read the data 400 times over 1 second to detect if it stopped shaking or not.
            for i in range(400):
                value = value+apin_high()
                time.sleep(0.001)
            if value == 0: # If we don't detect any shaking over 1 second then we assume shaking stopped and break out of loop
                break
            else:
                shake_readings += 1 # Otherwise continue reading the sensor.
        chrono.stop()
        total_ms = chrono.read()*1000
        return [total_ms, shake_readings] #Return the execution time of the function in ms, and the shake readings 1 == 100ms.
    except Exception as e:
        print(str(e))


# Read the shock_value 100 times and get an average reading. 
# We do this in case there is any problems with the readings due to interference from the high sensitivity sensor.
def detect_shock_value(apin):
    value = 0
    for i in range(100):
        value = value+apin()
        time.sleep(0.001)
    return int(value)/100