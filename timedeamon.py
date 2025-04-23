import sys
import time
import os

target_time = int(sys.argv[1])  # in ms
timeconfigfile = sys.argv[2]

remaining_time = target_time

while True:
    with open(timeconfigfile, "r") as f:
        remaining_time = int(f.read().strip())
        
        if remaining_time <= 0:
            print(f"Time's up!")
            os.remove(timeconfigfile)
            sys.exit(0)
    
    time.sleep(1)
    remaining_time -= 1000  # Subtract one second in milliseconds
    
    with open(timeconfigfile, "w") as f:
        f.write(str(remaining_time))