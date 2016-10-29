import machine
import ubinascii

config = {
    "debug": True,
    "ESSID": "TogLovesToHack", # Ensure you're using a 2.4Ghz AP
    "PSK": "SuperSecretPSK",
    "broker": "mqtt.tog.ie",
    "topic": "/tog/sensors",
    "client_id_prefix": "esp8266_",
    "sensor_name": "Test Sensor",
    "sensor_pin": 0,
    "interval": 20,
}

config.update({"client_id":bytes(config["client_id_prefix"],'utf-8') + ubinascii.hexlify(machine.unique_id())})
