import threading
import time

from oslo_log import log as logging


LOG = logging.getLogger(__name__)


def periodic_task(interval_sec=30):
    """Executes the task in a separate daemon thread and repeats
    after every interval_sec.
    Daemon thread terminates when main-programs exits;
    and is used for join-independent tasks
    """
    def repeat(f):
        """decorator that repeatedly calls f"""

        def periodic_task_executor(*args, **kwargs):
            while True:
                LOG.debug("Periodic task: Executing: %s:%s",
                          f.func_name, f.__module__)
                f(*args, **kwargs)
                time.sleep(interval_sec)

        def thread_f(*args, **kwargs):
            t = threading.Thread(target=periodic_task_executor,
                                 name='periodic_task_' + f.func_name,
                                 args=args,
                                 kwargs=kwargs)
            t.daemon = True
            t.start()

        return thread_f

    return repeat
