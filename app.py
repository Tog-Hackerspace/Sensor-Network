import gc
from config import config
from sys import maxsize
import time
import machine

def connect_wifi(config=None):
    if not config:
        config = load_config()
    import network
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('Connecting to network...')
        wlan.connect(config.get("ESSID",""), config.get("PSK",""))
        while not wlan.isconnected():
            pass
    print('Network config:', wlan.ifconfig())

def get_pin(config):
    """
    TOG Sensor Developers - set up your pins here as necessary.
    You shouldn't need to touch anything else...

    sensor_mode: "ADC", "PULL_UP", "", None
    """
    #Set up our pin instance
    sensor_pin = config["sensor_pin"] or 0
    sensor_mode = config.get("sensor_mode",None)

    if sensor_mode:
        if sensor_mode == "ADC":
            return machine.ADC(sensor_pin)
        if sensor_mode == "PULL_UP":
            sensor_mode = machine.Pin.PULL_UP

    return machine.Pin(sensor_pin, machine.Pin.IN, sensor_mode)


def run():
    connect_wifi(config=config)
    pin = get_pin(config)

    #Where's all the RAM gone?
    gc.collect()

    from sensornet import SensorTransporter
    s = SensorTransporter(config=config, sensor=pin)
    s.knock_knock() # Setup and test the connection

    #The ESP8266 timer drifts after 7h:45 minutes, so we do a forced restart every 7.5 hours,
    #or if there is a user limit set, whichever is first.
    #TODO - Make this deep_sleep-able, maybe check the interval and if it's more than a minute then sleep.

    interval = config.get("interval", 60)
    limit = config.get("limit", maxsize)
    HARD_LIMIT = int(2.7e4 / interval)
    loop_count = 0

    print("Looping every {0} seconds, rebooting after {1} loops".format(interval, min(limit,HARD_LIMIT)))
    while loop_count < min(limit, HARD_LIMIT):
        s.log_value()
        loop_count += 1
        if loop_count % 100 == 0:
            print("Loop %s" % loop_count)
        time.sleep(interval)
    machine.reset()
