from time import sleep

from client import Subscriber


def main():
    sleep_time = 0.5
    client_id = "graphicSubscriber"
    broker_ip = "127.0.0.1"
    topic = "/sensors/temp"
    qos = 2
    subscriber = Subscriber(client_id)
    subscriber.connect(broker_ip)
    subscriber.subscribe(topic)
    subscriber.loop_start()
    try:
        while True:
            sleep(sleep_time)
    except KeyboardInterrupt:
        raise
        subscriber.disconnect()
        subscriber.loop_stop()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        raise
        print("\nExiting...")