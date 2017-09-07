import six

if six.PY2:
    import Queue as native_queue
else:
    import queue as native_queue


from oslo_log import log as logging

from nimo import states as nimo_states


LOG = logging.getLogger(__name__)


class VirtEventQueue(object):
    '''Queue all libvirt events
    '''

    def __init__(self, q_size=0):
        '''Create a queue, internally of type Queue.Queue.
        Default queue size is infinite.
        '''
        self.q = native_queue.Queue(q_size)

    def qsize(self):
        '''Returns approx current items count in queue.
        '''
        return self.q.qsize()

    def maxsize(self):
        '''Return queue max size
        '''
        return self.q.maxsize()

    def get(self, block=True, timeout=None):
        '''Remove and return next item from queue.
        Default block the caller until item is available
        and does not timeout blocking.
        '''
        item = None
        try:
            item = self.q.get(block, timeout)
        except native_queue.Empty as e:
            return None
        return item

    def put(self, item, block=False, timeout=None):
        '''Put item in queue. Default Non-blocking.
        '''
        try:
            ret = self.q.put(item, block, timeout)
        except native_queue.Full as e:
            # Logging could prove to be blocking. Don't uncomment
            # LOG.error("Queue is full. Failed to push new message.")
            pass

    def q_stats(self):
        '''LOG queue current usage.
        Non blocking producers should not call this functions.
        '''
        LOG.debug("Current message count: %d", self.q.qsize())

    def empty(self):
        return self.q.empty()


class VirtLifeCycleEvent(object):
    '''Define VM event as items to be queued'''
    def __init__(self, conn=None, dom=None,
                 event=None, detail=None, opaque=None):
        # TODO(jay): deep copy conn, dom objects
        self.conn = conn
        self.dom = dom
        self.event = event
        self.detail = detail
        self.opaque = opaque

    def __repr__(self):
        ret = "Conn='%s'" % (
            self.conn.getURI() if self.conn is not None else None)
        ret = ret + " Domain='%s'" % (
            self.dom.UUIDString() if self.dom is not None else None)
        ret = ret + " Event Type = '%s'" % (nimo_states.event_type_to_str(self.event))
        ret = ret + " Event = '%s'" % (
            nimo_states.event_detail_to_str(self.event, self.detail))

        return ret
