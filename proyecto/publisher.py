from time import sleep

from client import Publisher
from sensor import Sensor


def main():
    client_id = "sensorPublisher"
    broker_ip = "127.0.0.1"
    topic = "/sensors/temp"
    qos = 2
    sleep_time = 1
    sensor = Sensor()
    publisher = Publisher(client_id)
    publisher.connect(broker_ip)
    publisher.loop_start()
    try:
        while True:
            msg = sensor.read()
            publisher.publish(topic, msg, qos, retain=True)
            sleep(sleep_time)
    except KeyboardInterrupt:
        publisher.disconnect()
        publisher.loop_stop()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting...")
