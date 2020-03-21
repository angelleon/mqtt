from multiprocessing import Process, Queue, Event, queues

import sqlite3


class Register(Process):
    MKDB_STMNT = "CREATE TABLE Temperature(tempId INTEGER PRIMARY KEY, temp REAL, timestamp DATETIME DEFAULT (STRFTIME('%Y-%m-%d %H:%M:%f', 'NOW')))"
    INSERT_STMNT = "INSERT INTO Temperature(temp) VALUES (?)"
    def __init__(self, queue: Queue, stop_event: Event):
        super().__init__()
        self._queue = queue
        self._stop_event = stop_event

    def _mk_db(self):
        cur = self._db.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type = 'table'")
        if len(cur.fetchall()) == 0:
            cur.execute(self.MKDB_STMNT)
        cur.close()
        self._db.commit()

    def run(self):
        self._db = sqlite3.connect("./db.sqlite")
        self._mk_db()
        while True:
            if self._stop_event.is_set():
                break
            try:
                value = self._queue.get(block=True, timeout=0.5)
                self._write_value((value,))
            except queues.Empty:
                pass
            except KeyboardInterrupt:
                self._stop_event.set()

    def _write_value(self, values):
        cur = self._db.cursor()
        cur.execute(self.INSERT_STMNT, values)
        cur.close()
        self._db.commit()