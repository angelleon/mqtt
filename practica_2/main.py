#!/usr/bin/env python3.8

from logging import getLogger, basicConfig, DEBUG
from string import ascii_letters
from random import choice

basicConfig(level=DEBUG)


from paho.mqtt import client as mqtt
from time import sleep

class Client(mqtt.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.log = getLogger(__name__)

    def on_connect(self, userdata, flags, rc):
        self.log.info("Client connected to broker")

    def on_message(self, userdata, message):
        self.log.info(f"{userdata=}\n{repr(message)}")

def rand_msg(length=32):
    s = ''.join([choice(ascii_letters) for _ in range(length)])
    return s

def main():
    topic = "/iot/chat"
    topic = "mensajex"
    host_addr = "localhost"
    host_addr = "10.12.40.58"
    msg = rand_msg()
    client_name = "angelMQTT"
    client = Client(client_name)
    client.connect(host_addr)
    client.subscribe(topic, 2)
    for i in range(5):
        client.publish(topic, msg, 2, True)
    client.loop_start()
    sleep(5)
    client.loop_stop()
    client.disconnect()



if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\nExitting...")
