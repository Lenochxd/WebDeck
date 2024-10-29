import time
from app.utils.logger import log


class Timer:
    def __init__(self, name='default'):
        self.name = name
        self.timers = {}
        self.stopped_timers = {}
    
    def start(self, name='default', logger=True) -> None:
        self.timers[name] = time.time()
        if logger:
            log.debug(f'[S] Timer \'{name}\' started at {self.timers[name]}')

    def get(self, name='default', logger=True) -> float:
        if name in self.timers:
            elapsed_time = time.time() - self.timers[name]
        elif name in self.stopped_timers:
            elapsed_time = self.stopped_timers[name]
        else:
            raise ValueError(f'Timer \'{name}\' does not exist.')

        if logger:
            minutes, seconds = divmod(elapsed_time, 60)
            milliseconds = (seconds - int(seconds)) * 1000
            log.debug(f'[G] Timer \'{name}\' is at {int(minutes)} minutes, {int(seconds)} seconds, {int(milliseconds)} milliseconds')
        return elapsed_time

    def stop(self, name='default', logger=True) -> float:
        if name not in self.timers:
            raise ValueError(f'Timer \'{name}\' does not exist.')

        elapsed_time = time.time() - self.timers.pop(name)
        self.stopped_timers[name] = elapsed_time

        if logger:
            minutes, seconds = divmod(elapsed_time, 60)
            milliseconds = (seconds - int(seconds)) * 1000
            log.debug(f'[/] Timer \'{name}\' stopped at {int(minutes)} minutes, {int(seconds)} seconds, {int(milliseconds)} milliseconds')
        return elapsed_time

    def stop_all(self, logger=True) -> dict:
        times = {}
        for name in list(self.timers.keys()):
            times[name] = self.stop(name, logger)
        return times

    def get_longest_timers(self, count=1, logger=True) -> list:
        """
        Retrieve the longest running timers.
        Args:
            count (int): The number of longest timers to retrieve. Defaults to 1.
            logger (bool): If True, logs the elapsed time of each timer. Defaults to True.
        Returns:
            list: A list of tuples where each tuple contains the timer name and the elapsed time.
              The list is sorted in descending order of elapsed time.
        """
        if not self.timers and not self.stopped_timers:
            return []

        count -= 1
        all_timers = {**self.timers, **self.stopped_timers}
        sorted_timers = sorted(all_timers.items(), key=lambda item: time.time() - item[1] if item[0] in self.timers else item[1], reverse=True)
        longest_timers = sorted_timers[:count]

        result = []
        for name, start_time in longest_timers:
            elapsed_time = time.time() - start_time if name in self.timers else start_time
            if logger:
                minutes, seconds = divmod(elapsed_time, 60)
                milliseconds = (seconds - int(seconds)) * 1000
                log.debug(f'[Final] Timer \'{name}\' is at {int(minutes)} minutes, {int(seconds)} seconds, {int(milliseconds)} milliseconds')
            result.append((name, elapsed_time))
        
        return result
    
timer = Timer()