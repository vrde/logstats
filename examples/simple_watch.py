import logging
logging.basicConfig(level=logging.INFO)

import time

from logstats.thread import logstats
from collections import Counter
from random import choice, uniform


stats = Counter()
ls = logstats(stats, timeout=2)

while True:
    stats[choice(['A', 'B', 'C'])] += 1
    time.sleep(uniform(0, 0.2))

