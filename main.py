import sys
import colorama
import subprocess
import os
import signal
import shutil

TIMER_DIR = "/var/timi/timers"


def log(msg):
    """Prints a message to the console with [*] prefix."""
    print(colorama.Fore.GREEN + "\n[*] " + colorama.Fore.RESET + str(msg), end=" ")


def fail(msg):
    """Prints a message to the console with [x] prefix and exits."""
    print(colorama.Fore.RED + "\n[x] " + colorama.Fore.RESET + str(msg), end=" ")
    sys.exit(1)

def info(msg):
    """Prints a message to the console with [i] prefix."""
    print(colorama.Fore.YELLOW + "\n[i] " + colorama.Fore.RESET + str(msg), end=" ")



def convert_to_ms(time_str):
    """Convert time string to milliseconds."""
    try:
        total_ms = 0
        current_num = ""
        for char in time_str:
            if char.isdigit() or char == '.':
                current_num += char
            elif char in ['h', 'm', 's']:
                if not current_num:
                    raise ValueError("Invalid time format")
                if char == 'h':
                    total_ms += int(float(current_num) * 3600 * 1000)
                elif char == 'm':
                    total_ms += int(float(current_num) * 60 * 1000)
                elif char == 's':
                    total_ms += int(float(current_num) * 1000)
                current_num = ""
            else:
                raise ValueError("Invalid character in time string")
        # Handle ms suffix
        if time_str.endswith("ms"):
            total_ms = int(time_str[:-2])
        elif current_num:
            raise ValueError("Missing time unit")
        if total_ms == 0:
            raise ValueError("Time must be greater than 0")
        return total_ms
    except ValueError as e:
        fail(e)


def convert_to_string(ms):
    """Convert milliseconds to a human-readable string."""
    parts = []
    hours = ms // 3600000
    if hours > 0:
        parts.append(f"{hours}h")
        ms %= 3600000
    minutes = ms // 60000
    if minutes > 0:
        parts.append(f"{minutes}m")
        ms %= 60000
    seconds = ms // 1000
    if seconds > 0:
        parts.append(f"{seconds}s")
        ms %= 1000
    if ms > 0:
        parts.append(f"{ms}ms")
    return "".join(parts) if parts else "0ms"


def get_next_timer_name():
    """Get the next available timer name (timer1, timer2, etc.)"""
    if not os.path.exists(TIMER_DIR):
        os.makedirs(TIMER_DIR, exist_ok=True)
    existing = [f for f in os.listdir(TIMER_DIR) if f.startswith("timer") and not f.endswith(".pid")]
    if not existing:
        return "timer1"
    numbers = [int(f[5:]) for f in existing]
    return f"timer{max(numbers) + 1}"


def start_timer_daemon(time_ms, timer_path):
    """Start the background daemon and record its PID."""
    daemon_script = os.path.join(os.path.dirname(__file__), "timedeamon.py")
    proc = subprocess.Popen(["python3", daemon_script, str(time_ms), timer_path])
    with open(f"{timer_path}.pid", "w") as pidf:
        pidf.write(str(proc.pid))
    log(f"Started timer daemon for {os.path.basename(timer_path)}")


# Ensure command provided
if len(sys.argv) < 2:
    fail("Please provide a command. Use 'help' for options.")

cmd = sys.argv[1]

# GET command: list timers, showing paused state
if cmd == "get":
    if not os.path.exists(TIMER_DIR) or not any(f for f in os.listdir(TIMER_DIR) if not f.endswith(".pid")):
        fail("No timers set")
    for fname in sorted(os.listdir(TIMER_DIR)):
        if fname.endswith(".pid"):  # skip pid files
            continue
        path = os.path.join(TIMER_DIR, fname)
        with open(path) as tf:
            remaining = int(tf.read().strip())
        paused = not os.path.exists(f"{path}.pid")
        status = " (paused)" if paused else ""
        log(f"{fname}: {convert_to_string(remaining)} remaining{status}")
    sys.exit(0)

# CLEAR command
if cmd == "clear":
    if not os.path.exists(TIMER_DIR):
        fail("No timers to clear")

    for fname in os.listdir(TIMER_DIR):
        file_path = os.path.join(TIMER_DIR, fname)

        if not os.path.isfile(file_path):
            continue  # skip directories, just to be sure

        if fname.endswith(".pid"):
            # Kill the daemon process first
            try:
                with open(file_path) as pf:
                    pid = int(pf.read())
                    os.kill(pid, signal.SIGTERM)
            except Exception as e:
                info(f"Could not kill process {fname}: {e}")

        # Now delete the file
        os.remove(file_path)

    log("Cleared all timers")
    sys.exit(0)
    
# REMOVE command
if cmd == "remove":
    if len(sys.argv) < 3:
        fail("Please specify timer name")
    name = sys.argv[2]
    path = os.path.join(TIMER_DIR, name)
    pid_path = f"{path}.pid"
    if not os.path.exists(path):
        fail(f"Timer {name} not found")
    # kill daemon if running
    if os.path.exists(pid_path):
        with open(pid_path) as pf:
            try:
                os.kill(int(pf.read()), signal.SIGTERM)
            except Exception:
                pass
        os.remove(pid_path)
    os.remove(path)
    log(f"Timer {name} removed")
    sys.exit(0)

# TOGGLE command: pause or resume
if cmd == "toggle":
    if len(sys.argv) < 3:
        fail("Please specify timer name")
    name = sys.argv[2]
    path = os.path.join(TIMER_DIR, name)
    pid_path = f"{path}.pid"
    if not os.path.exists(path):
        fail(f"Timer {name} not found")
    # If running, pause it
    if os.path.exists(pid_path):
        with open(pid_path) as pf:
            try:
                os.kill(int(pf.read()), signal.SIGTERM)
            except Exception:
                pass
        os.remove(pid_path)
        log(f"Timer {name} paused")
    else:
        # resume from remaining
        with open(path) as tf:
            remaining = int(tf.read().strip())
        if remaining <= 0:
            fail(f"Timer {name} already finished")
        start_timer_daemon(remaining, path)
        log(f"Timer {name} resumed")
    sys.exit(0)

# HELP command
if cmd in ("help", "-h", "--help"):
    print("""        
┌────┬───┐▗▄▄▄▖▗▄▄▄▖▗▖  ▗▖▗▄▄▄▖
│    │   │  █    █  ▐▛▚▞▜▌  █  
│    │   │  █    █  ▐▌  ▐▌  █ 
├────┘   │  █  ▗▄█▄▖▐▌  ▐▌▗▄█▄▖
└────────┘
Usage: timi [time] [options]

Options:
    get        Get all timers
    clear      Clear all timers
    remove     Removes a timer
    toggle     Pauses or resumes a timer
    help       Show this help message
    -h, --help Show this help message

How to set a Timer:
    timi 10s     Set a timer for 10 seconds
    timi 5m      Set a timer for 5 minutes
    timi 1h      Set a timer for 1 hour
    timi 100ms   Set a timer for 100 milliseconds
    timi 1h30m   Set a timer for 1 hour and 30 minutes
""")
    sys.exit(0)

# DEFAULT: set a new timer
# interpret first argument as time
try:
    ms = convert_to_ms(cmd)
except SystemExit:
    sys.exit(1)

name = get_next_timer_name()
path = os.path.join(TIMER_DIR, name)
if not os.path.exists(TIMER_DIR):
    os.makedirs(TIMER_DIR, exist_ok=True)
with open(path, "w") as f:
    f.write(str(ms))

log(f"Set {name} to {cmd}")
if shutil.which("notify-send") is  None:
    info("notify-send is not avabiale. You won't get a notification if a timer finishes. But you still get Sound and in the Terminal.")
start_timer_daemon(ms, path)

sys.exit(0)
