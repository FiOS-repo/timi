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

def get_next_timer_name():
    """Get the next available timer name (timer1, timer2, etc.)"""
    if not os.path.exists("timers"):
        os.makedirs("timers")
    existing = [f for f in os.listdir("timers") if f.startswith("timer")]
    if not existing:
        return "timer1"
    numbers = [int(f[5:]) for f in existing]
    return f"timer{max(numbers) + 1}"

if sys.argv[1] == "get":
    if not os.path.exists("timers") or not os.listdir("timers"):
        fail("No timers set")
    for timer_file in os.listdir("timers"):
        with open(os.path.join("timers", timer_file), "r") as f:
            log(f"{timer_file}: {convert_to_string(int(f.read()))} remaining")
    sys.exit(0)

if sys.argv[1] == "stop":
    if len(sys.argv) < 3:
        fail("Please specify timer name")
    timer_name = sys.argv[2]
    timer_path = os.path.join("timers", timer_name)
    if not os.path.exists(timer_path):
        fail(f"Timer {timer_name} not found")
    subprocess.run(["pkill", "-f", f"timedeamon.py {timer_path}"])
    os.remove(timer_path)
    log(f"Timer {timer_name} stopped")
    sys.exit(0)
    
time = convert_to_ms(sys.argv[1])
timer_name = get_next_timer_name()
timer_path = os.path.join("timers", timer_name)

if not os.path.exists("timers"):
    os.makedirs("timers")

with open(timer_path, "w") as f:
    f.write(str(time))

log(f"Set {timer_name} to {sys.argv[1]}")

# Start timedeamon in background
daemon_process = subprocess.Popen([
    "python3",
    os.path.join(os.path.dirname(__file__), "timedeamon.py"),
    str(time),
    timer_path
])

log(f"Started timer daemon for {timer_name}")
sys.exit(0)