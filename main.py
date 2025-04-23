import sys
import colorama
import datetime
import subprocess
import atexit
import os

def log(msg):
    """Prints a message to the console with [*] prefix."""
    print(colorama.Fore.GREEN + "\n[*] " + colorama.Fore.RESET + str(msg), end=" ")

def fail(msg):
    """Prints a message to the console with [x] prefix and exits."""
    print(colorama.Fore.RED + "\n[x] " + colorama.Fore.RESET + str(msg), end=" ")
    sys.exit(1)

def convert_to_ms(time_str):
    """Convert time string to milliseconds."""
    try:
        if time_str.endswith("ms"):
            return int(time_str[:-2])
        elif time_str.endswith("s"):
            return int(float(time_str[:-1]) * 1000)
        elif time_str.endswith("m"):
            return int(float(time_str[:-1]) * 60 * 1000)
        elif time_str.endswith("h"):
            return int(float(time_str[:-1]) * 3600 * 1000)
        else:
            raise ValueError("Couldn't parse time string: Possible formats: ms, s, m, h")
    except ValueError as e:
        fail(e)

def convert_to_string(ms):
    """Convert milliseconds to a human-readable string."""
    if ms < 1000:
        return f"{ms}ms"
    elif ms < 60000:
        return f"{ms // 1000}s"
    elif ms < 3600000:
        return f"{ms // 60000}m"
    else:
        return f"{ms // 3600000}h"

if sys.argv[1] == "get":
    if not os.path.exists(".timerconfig"):
        fail("No timer set")
    else:
        with open(".timerconfig", "r") as f:
            log(convert_to_string(int(f.read())) + " remaining")
    sys.exit(0)

if sys.argv[1] == "stop":
    if not os.path.exists(".timerconfig"):
        fail("No timer set")
    else:
        # Kill any running timedeamon processes
        subprocess.run(["pkill", "-f", "timedeamon.py"])
        os.remove(".timerconfig")
        log("Timer stopped")
    sys.exit(0)
    
time = convert_to_ms(sys.argv[1])

with open(".timerconfig", "w") as f:
    f.write(str(time))

log(f"Set timer to {sys.argv[1]}")

# Start timedeamon in background
daemon_process = subprocess.Popen([
    "python3",
    os.path.join(os.path.dirname(__file__), "timedeamon.py"),
    str(time),
    ".timerconfig"
])

log("Started timer daemon")
sys.exit(0)