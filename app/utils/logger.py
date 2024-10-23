from datetime import datetime
from colorama import init, Fore
import os
import traceback

# Initialize colorama
init(autoreset=True)

class Logger:
    def __init__(self):
        log_dir = ".logs"
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        self.log_file = f"{log_dir}/{datetime.now().date().isoformat()}.log"

    def _write_log(self, level, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_message = f"[{level} @ {timestamp}] - {message}"
        with open(self.log_file, 'a') as file:
            file.write(log_message + '\n')
        return log_message

    def info(self, message):
        log_message = self._write_log("INFO", message)
        print(Fore.GREEN + log_message)

    def success(self, message):
        log_message = self._write_log("SUCCESS", message)
        print(Fore.GREEN + log_message)

    def warning(self, message):
        log_message = self._write_log("WARNING", message)
        print(Fore.YELLOW + log_message)

    def debug(self, message):
        log_message = self._write_log("DEBUG", message)
        print(Fore.BLUE + log_message)

    def error(self, message):
        log_message = self._write_log("ERROR", message)
        print(Fore.RED + log_message)
    
    def exception(self, exception, message=None):
        exception_title = f"{type(exception).__name__}:\n {str(exception)}\n"
        exception_message = ''.join(traceback.format_exception(type(exception), exception, exception.__traceback__))
        if message:
            log_message = self._write_log("EXCEPTION", f"{message} - {exception_title}\n{exception_message}")
        else:
            log_message = self._write_log("EXCEPTION", f"{exception_title}\n{exception_message}")
        print(Fore.MAGENTA + log_message)

    def httprequest(self, req, response):
        log_message = self._write_log(
            "REQUEST",
            f"{req.remote_addr} - {req.method} {req.url} - Status: {response.status_code}"
        )
        print(Fore.CYAN + log_message)

# Instantiate Logger at the module level
log = Logger()

if __name__ == '__main__':
    # Usage example:
    log.info('hello world')
    log.success('task completed successfully')
    log.warning('this is a warning')
    log.debug('this is a debug message')
    log.error('this is an error')
    try:
        1 / 0  # This will raise a ZeroDivisionError
    except ZeroDivisionError as e:
        log.exception(e, "An error occurred while performing division")