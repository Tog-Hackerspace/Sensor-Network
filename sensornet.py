import time
from umqtt.robust import MQTTClient
import json

class SensorTransporter(MQTTClient):

    def __init__(self, *args, **kwargs):
        self.config = config = kwargs["config"]
        self.client_id = config["client_id"]
        self.sensor_name = config["sensor_name"]
        self.broker = config["broker"]
        self.topic = self.set_topic(config["topic"])
        self.sensor = kwargs["sensor"]

        super(SensorTransporter, self).__init__(self.client_id, self.broker, *args)
        print("Transport settings: Broker: {0} Topic: {1}".format(self.broker, self.topic))


    def set_topic(self, topic):
        return '{}/{}'.format(topic or self.config.get('topic'),
                    self.client_id.decode('UTF-8'))

    def knock_knock(self):
        try:
            self.connect()
        except OSError:
            time.sleep(5)
            self.knock_knock()
        else:
            print("Saying Hello to %s" % self.broker)
            self.publish("/debug", bytes("Hello from %s" % self.client_id, 'utf-8'))
            self.disconnect()

    def log_value(self, value=None):

        if not value:
            value = self.sensor.value() or 0
            
        self.connect()
        data = json.dumps({"sensor_name": self.sensor_name,
                           "sensor_pin": self.config['sensor_pin'],
                           "client_id": self.client_id,
                           "value":value,})
        self.publish(self.topic, bytes(data, 'utf-8'))
        self.disconnect()
