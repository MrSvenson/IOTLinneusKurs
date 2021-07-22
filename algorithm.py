def vibration_formula(low_sensitivity_sensor, shake_duration):
	# The knock sensor returns a low_sensitivity_sensorue from 700 (nothing detected), down to 0 (big impact detected). This is less accurate
	low_sensor_score = 720-int(low_sensitivity_sensor)
	low_sensor_score = low_sensor_score*4  # Increase importance of knock by a factor of 4.

	# The vibration sensor returns a low_sensitivity_sensorue from 0 (nothing detected) up to 1024 (vibration detected)
	# By taking the vibration time into account, we can consider how extreme the impact is.
	# This is more accurate sensor, so we place more emphasis on this low_sensitivity_sensorue
	# So if we detected a shake for 4'isch second this would give us 4*200 = 800 low_sensitivity_sensorue
	high_sensor_score = shake_duration*100

	calibrated_score = int(round(low_sensor_score)+int(high_sensor_score))

	data = {
		"low_sensor_score": low_sensor_score,
		"high_sensor_score": high_sensor_score,
		"calibrated_score": calibrated_score
	}
	return data
