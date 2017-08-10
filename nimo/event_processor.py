from oslo_log import log as logging

LOG = logging.getLogger(__name__)


def act_on_event(event):
    LOG.debug("Acting on event: %s", event)


def process_queued_events(event_queue):

    # Process as many events as possible currently queued.
    # Currently serially processing, but can implement green pool here.

    while not event_queue.empty():
        event = event_queue.get()
        act_on_event(event)


def wait_and_dispatch_queued_events(event_queued_notify_recv,
                                    event_queue):
    # Wait to be notified that there are some
    # events pending in the queue

    while True:
        try:
            _c = None
            for i in range(5):
                LOG.debug("(block) reading from event_queued_notify_recv")

            # this should block until writer sends msg on pipe
            _c = event_queued_notify_recv.read(1)

            LOG.debug("read from event_queued_notify_recv")
        except ValueError as e:
            # will be raised when pipe's recv is closed
            LOG.error("event_queued_notify_recv is closed, read error %s", e)
            # continue

        try:
            assert _c
        except AssertionError as e:
            # EOF occurred. This could be because writer end of pipe is closed
            LOG.error("Reading event_queued_notify_recv returned EOF. "
                      "Possibly event_queued_notify_send (pipe's writer) "
                      "is closed.")

        process_queued_events(event_queue)
