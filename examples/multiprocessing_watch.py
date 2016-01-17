import logging
logging.basicConfig(level=logging.INFO)

import time
import multiprocessing as mp
from random import choice, uniform

import logstats


def important_task(stats):
    logstats.thread.start(stats)

    while True:
        stats[choice(['A', 'B', 'C'])] += 1
        time.sleep(uniform(0, 0.2))


if __name__ == '__main__':
    stats = logstats.Logstats()
    logstats.thread.start(stats)

    for i in range(4):
        p = mp.Process(target=important_task, args=(stats.get_child(), ))
        p.start()
