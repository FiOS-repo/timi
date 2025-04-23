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
        
        if time_str.endswith("ms"):
            total_ms = int(time_str[:-2])
        elif current_num:  # If there are remaining numbers without units
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

if sys.argv[1] == "clear":
    if not os.path.exists("timers") or not os.listdir("timers"):
        fail("No timers set")
    for timer_file in os.listdir("timers"):
        os.remove(os.path.join("timers", timer_file))
    log("Cleared all timers")
    sys.exit(0)
if sys.argv[1] in ("help", "-h", "--help"):
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
    stop       Stop a timer
    help       Show this help message
    -h, --help Show this help message
          
How to set a Timer:
    timi 10s     Set a timer for 10 seconds
    timi 5m      Set a timer for 5 minutes
    timi 1h      Set a timer for 1 hour
    timi 100ms   Set a timer for 100 milliseconds
    timi 1h30m  Set a timer for 1 hour and 30 minutes
""")
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