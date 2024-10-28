import time
from app.utils.logger import log


class Timer:
    def __init__(self, name='default'):
        self.name = name
        self.timers = {}
    
    def start(self, name='default', logger=True) -> None:
        self.timers[name] = time.time()
        if logger:
            log.debug(f'Timer \'{name}\' started at {self.timers[name]}')

    def get(self, name='default', logger=True) -> float:
        if logger:
            elapsed_time = time.time() - self.timers[name]
            minutes, seconds = divmod(elapsed_time, 60)
            milliseconds = (seconds - int(seconds)) * 1000
            log.debug(f'Timer \'{name}\' is at {int(minutes)} minutes, {int(seconds)} seconds, {int(milliseconds)} milliseconds')
        return time.time() - self.timers[name]

    def stop(self, name='default', logger=True) -> float:
        if logger:
            elapsed_time = time.time() - self.timers[name]
            minutes, seconds = divmod(elapsed_time, 60)
            milliseconds = (seconds - int(seconds)) * 1000
            log.debug(f'Timer {name} stopped at {int(minutes)} minutes, {int(seconds)} seconds, {int(milliseconds)} milliseconds')
        return time.time() - self.timers.pop(name)

    def stop_all(self, logger=True) -> dict:
        times = {}
        for name in self.timers.keys():
            times[name] = self.stop(name, logger)
        return times
    
timer = Timer()