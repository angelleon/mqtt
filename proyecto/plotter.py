
import multiprocessing
from threading import Thread, Semaphore, Event
import queue
from time import sleep, time

from matplotlib import pyplot as plot, animation


class Worker(Thread):
    def __init__(self, queue, x_data, y_data, sem, stop_event, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._queue = queue
        self._plot_data_x = x_data
        self._plot_data_y = y_data
        self._sem = sem
        self._stop_event = stop_event

    def run(self):
        print("working")
        t0 = time()
        while True:
            if self._stop_event.is_set():
                break
            try:
                value = self._queue.get(block=True, timeout=0.5)
                print(value)
                self._sem.acquire()
                self._plot_data_x.append(time() - t0)
                self._plot_data_y.append(value)
                if len(self._plot_data_x) > 10:
                    self._plot_data_x.pop(0)
                    self._plot_data_y.pop(0)
                self._sem.release()
                sleep(0.5)
            except queue.Empty:
                pass
            except KeyboardInterrupt:
                self._stop_event.set()
                break


class Plotter(multiprocessing.Process):
    def __init__(self, queue, stop_event):
        super().__init__()
        self._queue = queue
        self._stop_event = stop_event
        

    def run(self):
        self._fig = plot.figure()
        self._ax = self._fig.add_subplot(111)
        self._ax.set_ylim(-1.5, 1.5)
        self._plot_data_x = []
        self._plot_data_y = []
        sem = Semaphore()
        stop = Event()
        def _draw_data(index):
            sem.acquire()
            self._ax.clear()
            self._ax.plot(self._plot_data_x, self._plot_data_y, color="magenta", marker=".")
            print(self._plot_data_y)
            sem.release()
        self._ani = animation.FuncAnimation(self._fig, _draw_data, interval=500)
        print("Starting worker thread")
        t = Worker(self._queue, self._plot_data_x, self._plot_data_y, sem, stop)
        t.start()
        plot.show()
        t.join()
        while not self._stop_event.is_set():
            sleep(0.5)
        print("End working thread")
