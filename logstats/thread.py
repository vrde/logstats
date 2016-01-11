import time
from threading import Thread
from logstats import Logstats
import logging

log = logging.getLogger(__name__)


def logstats(stats, msg=None, emit_func=None, logger=log, level='INFO', timeout=1):

    def _run():
        while True:
            time.sleep(timeout)
            ls()

    ls = Logstats(stats, msg, emit_func, logger, level)
    t = Thread(target=_run)
    t.daemon = True
    t.start()
    return t
