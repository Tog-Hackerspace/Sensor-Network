# Sensor-Network
hackerspace sensor network / microservice api


Sensor developers are mainly going to be interested in modifying the config.py as needed.

Also worthy of note for the more adventurous -feel free to modify "get_pin" in app.py, just make sure to return a machine.Pin instance at somepoint.

The SensorTransporter hooks into a specified pin and polls it at a specified interval, then ships it off to the TOG MQTT broker for aggregation and further analysis.

Note: Make sure to configure the WiFi in config.py before assuming it's broken.
