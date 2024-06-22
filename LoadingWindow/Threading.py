import traceback
import threading
import time



class TaskThread(threading.Thread):
    running = {}
    def __init__(self, target, interval=0, delay=0, tries=5, fargs=(), onFinished=lambda:None):
        super(self.__class__, self).__init__(target=self.wrappedFunction, daemon=True)
        self.target = target
        self.threadName = self.target.__name__
        self.event = threading.Event()
        self.interval = interval
        self.delay = delay
        self.tries = tries
        self.fargs = fargs
        self.onFinished = onFinished

    def finish(self):
        if(self.threadName in self.running): 
            del self.running[self.threadName]
        if(not self.event.is_set()):
            self.event.set()
            self.onFinished()

    def wrappedFunction(self):
        passed = False
        time.sleep(self.delay)
        while(not self.event.is_set() and not passed and self.tries != 0):
            try:
                passed = self.target(*self.fargs)
            except Exception as e:
                print(traceback.format_exc())
            finally:
                self.tries -= 1
                time.sleep(self.interval)
        else: self.finish()

    def start(self):
        if(self.threadName not in self.running):
            self.running[self.threadName] = self
            super().start()
        return self.running[self.threadName]




