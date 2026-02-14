import datetime
import os

LOG_FILE = "tanya.log"

def log_info(message):
    _log(message, level="INFO")

def log_warning(message):
    _log(message, level="WARNING")

def log_error(message):
    _log(message, level="ERROR")

def _log(message, level="INFO"):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"[{now}] [{level}] {message}\n"
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(log_line)
    except Exception:
        pass
