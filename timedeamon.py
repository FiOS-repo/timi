import sys
import time
import datetime

time = sys.argv[1]
timeconfigfile = sys.argv[2]

while True:
    with open(timeconfigfile, "r") as f:
        time_at_start = f.read()
    time.sleep(1)