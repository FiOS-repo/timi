import sys
import time
import os

target_time = int(sys.argv[1])  # in ms
timerfile = sys.argv[2]
remaining_time = target_time

while True:
    with open(timerfile, "r") as f:
        remaining_time = int(f.read().strip())
        
        if remaining_time <= 0:
            print(f"Time's up for {os.path.basename(timerfile)}!")
            os.remove(timerfile)
            sys.exit(0)
    
    time.sleep(1)
    remaining_time -= 1000  # Subtract one second in milliseconds
    
    with open(timerfile, "w") as f:
        f.write(str(remaining_time))