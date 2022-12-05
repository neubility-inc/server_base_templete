import os
from app.utils.timestamp import timestamp
import threading, multiprocessing, traceback, sys
import define


class Logger:
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"

    def __init__(self, fileName):
        self._lock = multiprocessing.Lock()
        self._queue = multiprocessing.Queue(-1)
        self._baseDir = define.ROOT_DIR
        self._logPath = f"{self._baseDir}/var/log"
        self._fileName = fileName
        self._yymmdd = timestamp.get_current_time_to_format("%y%m%d")
        self._openFile()
        t = threading.Thread(target=self._process)
        t.daemon = True
        t.start()

    def info(self, message):
        self.write(self.INFO, message)

    def warning(self, message):
        self.write(self.WARNING, message)

    def error(self, message):
        self.write(self.ERROR, message)

    def write(self, level, message):
        log = f"[ {level} ] [ {timestamp.get_current_time()} ] {message}"
        self._queue.put(log)

    def _write(self, log):
        self._lock.acquire()
        if self._checkLogRotate():
            self.close()
            self._yymmdd = timestamp.get_current_time_to_format("%y%m%d")
            self._openFile()
        self._logFile.write(log)
        self._logFile.flush()
        self._lock.release()

    def _process(self):
        while True:
            try:
                log = self._queue.get()
                self._write(log)
            except (KeyboardInterrupt, SystemExit):
                raise
            except EOFError:
                break
            except:
                traceback.print_exc(file=sys.stderr)

    def _checkLogRotate(self):
        if self._yymmdd != timestamp.get_current_time():
            return True
        return False

    def _openFile(self):
        filePath = f"{self._logPath}"
        fileName = f"/{self._fileName}_{self._yymmdd}.log"
        os.makedirs(filePath, exist_ok=True)
        mode = "w+"
        if os.path.isfile(filePath + fileName):
            mode = "a"
        self._logFile = open(filePath + fileName, mode=mode, encoding="utf-8")
        self._logFile.write("\n")

    def close(self):
        self._logFile.close()


logger = Logger(f"{define.SERVER_NAME}")
access_logger = Logger(f"{define.SERVER_NAME}_access")
