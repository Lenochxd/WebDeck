import os
import traceback
from datetime import datetime
from colorama import init, Fore
from app.utils.working_dir import get_base_dir

# Initialize colorama
init(autoreset=True)

class Logger:
    def __init__(self, from_updater=False):
        """
        Initializes the Logger instance.
        
        This method creates a log directory if it doesn't exist and sets the log file path.
        """
        log_dir = os.path.join(get_base_dir(), ".logs")
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        date_str = datetime.now().date().isoformat()
        if from_updater:
            self.log_file = f"{log_dir}/{date_str}-updater.log"
        else:
            self.log_file = f"{log_dir}/{date_str}.log"
        self.debug_enabled = True  # Add this line

    def _write_log(self, level, message):
        """
        Writes a log message to the log file with a given level and message.
        
        Returns:
            str: The formatted log message.
        """
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_message = f"[{level} @ {timestamp}] - {message}"
        try:
            with open(self.log_file, 'a') as file:
                file.write(log_message + '\n')
        except PermissionError:
            new_log_file = os.path.join(os.path.dirname(self.log_file), os.path.basename(self.log_file).replace('.log', '-new.log'))
            self.set_log_file(new_log_file)
            with open(self.log_file, 'a') as file:
                file.write(log_message + '\n')
        return log_message
    
    def set_log_file(self, log_file: str):
        """
        Sets the log file path to the specified file.
        
        Args:
            log_file (str): The path to the log file.
        """
        self.log_file = log_file

    def enable_debug(self):
        """
        Enables the printing of debug messages.
        """
        self.debug_enabled = True

    def disable_debug(self):
        """
        Disables the printing of debug messages.
        """
        self.debug_enabled = False

    def info(self, message):
        """
        Use this method for general information that highlights the progress of the application.
        """
        log_message = self._write_log("INFO", message)
        print(Fore.GREEN + log_message)

    def success(self, message):
        """
        Use this method to indicate successful completion of an operation.
        """
        log_message = self._write_log("SUCCESS", message)
        print(Fore.GREEN + log_message)
        
    def notice(self, message):
        """
        Use this method to indicate a redundant but correct action, such as trying to turn on something that is already on.
        """
        log_message = self._write_log("NOTICE", message)
        print(Fore.GREEN + log_message)

    def warning(self, message):
        """
        Use this method to indicate a potential problem or important situation that should be noted.
        """
        log_message = self._write_log("WARNING", message)
        print(Fore.YELLOW + log_message)

    def debug(self, message):
        """
        Use this method for detailed information, typically of interest only when diagnosing problems.
        """
        log_message = self._write_log("DEBUG", message)
        if self.debug_enabled:
            print(Fore.BLUE + log_message)

    def error(self, message):
        """
        Use this method to indicate a significant problem that has occurred.
        """
        log_message = self._write_log("ERROR", message)
        print(Fore.RED + log_message)
    
    def exception(self, exception, message=None, expected=True, log_traceback=True, print_log=True):
        """
        Logs an exception message along with the traceback.
        
        Use this method to log exceptions that occur during the execution of the program.
        
        Args:
            exception (Exception): The exception instance to log.
            message (str, optional): Additional message to log with the exception.
            expected (bool, optional): Indicates if the exception was expected (caught using try-except). Defaults to True.
            log_traceback (bool, optional): Indicates if the traceback details should be logged. Defaults to True.
            print_log (bool, optional): Indicates if the log message should be printed. Defaults to True.
        """
        exception_title = f"{type(exception).__name__}:\n {str(exception)}\n"
        if log_traceback:
            exception_message = ''.join(traceback.format_exception(type(exception), exception, exception.__traceback__))
        else:
            exception_message = str(exception)
        exception_type = "EXPECTED EXCEPTION" if expected else "UNEXPECTED EXCEPTION"
        if message:
            log_message = self._write_log(exception_type, f"{message} - {exception_title}\n{exception_message}")
        else:
            log_message = self._write_log(exception_type, f"{exception_title}\n{exception_message}")
        if print_log:
            print(Fore.MAGENTA + log_message)

    def httprequest(self, req, response):
        """
        Logs an HTTP request and its response status.
        
        Use this method to log details of incoming HTTP requests and their responses.
        """
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