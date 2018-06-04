import machine
import ubinascii

config = {
    "debug": True,
    "ESSID": "Tog Hackerspace", # Ensure you're using a 2.4Ghz AP
    "PSK": "DucksLoveToQuack",
    "broker": "10.48.1.254",
    "topic": "/tog/sensors/knife_switch",
    "client_id_prefix": "knife_switch_",
    "sensor_name": "Knife Switch",
    "sensor_pin": 4,
    "sensor_mode": "PULL_UP",
    "interval": 20,
}

config.update({"client_id":bytes(config["client_id_prefix"],'utf-8') + ubinascii.hexlify(machine.unique_id())})
