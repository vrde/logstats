import logging
logging.basicConfig(level=logging.INFO)

import time

import logstats
from random import choice, uniform


ls = logstats.Logstats()
logstats.thread.start(ls)

while True:
    ls[choice(['A', 'B', 'C'])] += 1
    time.sleep(uniform(0, 0.2))

