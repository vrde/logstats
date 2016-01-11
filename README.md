# logstats

A util to output stats out of long running processes. Super useful when you have **daemons**, or long running scripts, that need to output some data every now and then.


# How to use it

You need three things to make it run:
 1. a `dict`, or a [collections.Counter](https://docs.python.org/2/library/collections.html#collections.Counter), to collect stats;
 2. a `Logstats` instance (to be initialized with stats);
 3. something to call regularly the `Logstats` instance.

Everything is customizable but by default the `Logstats` instance will output the values of the stats object using the `logging` module. Together with every numerical value, the module will output the number of "values per second" for each of them.


# Example
In this example, we create a new instance of `Logstats` using a helper function that will:
 1. create the object for us;
 2. put it in a `thread` and run it forever

```python
import logging
logging.basicConfig(level=logging.INFO)

import time

from logstats.thread import logstats
from collections import Counter
from random import choice, uniform

# initialize the counter
stats = Counter()

# use the `thread.logstats` helper to create a Logstats object
# and run it in a Thread every 4 seconds
logstats_thread = logstats(stats, timeout=4)

# start our forever-running "daemon"
while True:
    stats[choice(['A', 'B', 'C'])] += 1
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

c = Counter()
logstats = Logstats(c, msg='This is a test. {value_a}, {value_b}', emit_func=emit)

c['value_a'] += 10
c['value_b'] += 2
c['value_c'] += 100

# will calculate the value for stats and output using the emit function
logstats()
```

Check the output of `nc` again, you should read this on your stdout:
```
This is a test. 10, 2
```

This time we didn't put the `Logstats` instance in an infinite loop in a thread. This is just to show you how to use the `Logstats` directly. If we want to output every second, we can use the `logstats.thread.logstats` util function. It supports all the parameters the `Logstats` class supports, plus a `timeout` parameter.
