"""Queued event dispatcher"""
import eventlet
from eventlet import patcher

from oslo_log import log as logging


native_threading = patcher.original("threading")
LOG = logging.getLogger(__name__)


class Dispatcher(object):
    """Adapter class to create native thread or eventlet green thread
    dispatcher"""

    def __init__(self, thread_type):
        self.t = None
        self.t_type = thread_type
        self.alive = False

    @classmethod
    def create(cls, thread_type, func, *args, **kwargs):
        """ Spawn a new dispatcher thread
        * @thread_type: 'nativethread' or 'greenthread'
        * @func: thread will start executing func
        * @args: args for func
        * @kwargs: kwargs for func
        """
        dispatcher = cls(thread_type)

        if thread_type == 'greenthread':
            dispatcher._green_thread_dispatcher(func, *args, **kwargs)
        else:
            dispatcher._native_thread_dispatcher(func, *args, **kwargs)

        return dispatcher

    def _green_thread_dispatcher(self, func,
                                 event_queued_notify_recv,
                                 event_queue,
                                 *args, **kwargs):
        """Spawn green threads to dispatch queued virt events"""

        self.t = eventlet.greenthread.spawn(func,
                                            event_queued_notify_recv,
                                            event_queue)
        self.alive = True
        LOG.debug("Created a new green dispatcher thread ")

    def _native_thread_dispatcher(self, func,
                                  event_queued_notify_recv,
                                  event_queue,
                                  *args, **kwargs):

        """Spawn native threads to dispatch queued virt events"""

        self.t = native_threading.Thread(
            target=func,
            name='DispatcherThread',
            args=(event_queued_notify_recv, event_queue)
        )
        self.t.start()
        self.alive = True

        # LOG.debug("Created a new native dispatcher thread ")

    def join(self):
        """Make the calling thread wait until this thread returns/exits"""
        if self.t_type == 'greenthread':
            t_ret_value = self.t.wait()
            self.alive = False
        else:
            # TODO(jay): Native threads will throw exception if join()
            # is called before it is running
            self.t.join()

    def is_alive(self):
        if self.t_type == 'greenthread':
            return self.alive
        else:
            return self.t.is_alive()
