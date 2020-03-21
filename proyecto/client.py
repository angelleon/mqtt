from multiprocessing import Queue, Event

from paho.mqtt import client as mqtt

from plotter import Plotter
from register import Register

class Client(mqtt.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)



class Publisher(Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Subscriber(Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.on_message = self.__class__._on_message
        self.on_subscribe = self.__class__._on_subscribe
        self._stop_event = Event()
        self._plot_queue = Queue()
        self._register_queue = Queue()
        self._plotter = Plotter(self._plot_queue, self._stop_event)
        self._register = Register(self._register_queue, self._stop_event)

    def _on_subscribe(self, userdata, mid, granted_qos, properties=None):
        print("subscribing")
        self._plotter.start()
        self._register.start()
        print("successful subscribed")

    def _on_disconnect(self, userdata, rc, properties):
        self._stop_event.set()

    def _on_message(self, userdata, message):
        msg = message.payload.decode("utf8")
        # print(msg)
        self._plot_queue.put(float(msg))
        self._register_queue.put(msg)
