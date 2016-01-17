# logstats

A util to output stats out of long running processes. Super useful when you have **daemons**, or long running scripts, that need to output some data every now and then.
It supports the `multiprocessing` modules, so you can collect stats from your child processes as well!


# How to use it

You need two things to make it run:
 1. a `Logstats` instance;
 2. something to call regularly the `Logstats` instance.

By default the `Logstats` instance will output the values of the stats object using the `logging` module. Together with every numerical value, the module will output the number of "values per second" for each of them.


# Example
In this example, we create a new instance of `Logstats` using a helper function that will:
 1. create the object for us;
 2. put it in a `thread` and run it forever

```python
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

```


The output looks like this:

```
logstats % python simple_watch.py
INFO:logstats.thread:A: 14, A.speed: 3, B: 19, B.speed: 4, C: 21, C.speed: 4
INFO:logstats.thread:A: 30, A.speed: 3, B: 38, B.speed: 4, C: 36, C.speed: 3
INFO:logstats.thread:A: 46, A.speed: 3, B: 53, B.speed: 3, C: 52, C.speed: 3
INFO:logstats.thread:A: 58, A.speed: 2, B: 69, B.speed: 3, C: 64, C.speed: 2
INFO:logstats.thread:A: 76, A.speed: 4, B: 83, B.speed: 3, C: 85, C.speed: 4
INFO:logstats.thread:A: 94, A.speed: 4, B: 98, B.speed: 3, C: 103, C.speed: 4
```

# Customize the emit function
A `Logstats` object can have a custom emit function. This time, to be fancy, we can output a custom string over UDP and receive it using the command line util `nc`.

First, start `nc` to listen on `localhost:5005`:
```bash
$ nc -ul 127.0.0.1 5005
```

Then run this script:

```python
from collections import Counter
from logstats import Logstats
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
def emit(msg):
    sock.sendto(msg, ('127.0.0.1', 5005))

stats = Logstats(msg='This is a test. {value_a}, {value_b}', emit_func=emit)

stats['value_a'] += 10
stats['value_b'] += 2
stats['value_c'] += 100

# will calculate the value for stats and output using the emit function
stats()
```

Check the output of `nc` again, you should read this on your stdout:
```
This is a test. 10, 2
```

This time we didn't put the `Logstats` instance in an infinite loop in a thread. This is just to show you how to use the `Logstats` directly. If we want to output every second, we can use the `logstats.thread.logstats` util function. It supports all the parameters the `Logstats` class supports, plus a `timeout` parameter.


# Collecting stats from child processes
A `Logstats` object has an handy method to *spawn* children instances: `get_child`.
Use this method to create a **child** instance of a `Logstats` object. The **child** instance will communicate with the parent using `multiprocessing.Queue`.
Remember to start the stats collection in all the children.


```python
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
```
