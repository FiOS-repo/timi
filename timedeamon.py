import sys
import time
import os
import shutil
import notify2
import contextlib

TIMER_DIR = "/var/timi/timers"

# Initialize notify2
notify2.init("TIMI")

# Helper to suppress output (stdout and stderr)
@contextlib.contextmanager
def suppress_output():
    with open(os.devnull, 'w') as devnull:
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        sys.stdout = devnull
        sys.stderr = devnull
        try:
            yield
        finally:
            sys.stdout = old_stdout
            sys.stderr = old_stderr

# Ensure timer directory exists
if not os.path.exists(TIMER_DIR):
    os.makedirs(TIMER_DIR, exist_ok=True)

# Get arguments
target_time = int(sys.argv[1])  # in milliseconds
timerfile = sys.argv[2]
remaining_time = target_time

while True:
    with open(timerfile, "r") as f:
        remaining_time = int(f.read().strip())

        if remaining_time <= 0:
            with suppress_output():
                notification = notify2.Notification(
                    "TIMI - Timer notifications",
                    f"Time's up for {os.path.basename(timerfile)}!"
                )
                notification.show()
            print(f"Time's up for {os.path.basename(timerfile)}!")
            os.remove(timerfile)
            sys.exit(0)

    time.sleep(1)
    remaining_time -= 1000  # Subtract one second in milliseconds

    with open(timerfile, "w") as f:
        f.write(str(remaining_time))
