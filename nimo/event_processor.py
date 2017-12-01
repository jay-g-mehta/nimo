from oslo_log import log as logging

from nimo import event_actions as nimo_event_actions
from nimo import utils as nimo_utils


LOG = logging.getLogger(__name__)


def act_on_event(event):
    LOG.debug("Acting on event: %s", event)
    action = nimo_event_actions.EventActionMapper.get_action(event.event,
                                                             event.detail)
    if action is not None:
        target_file = nimo_utils.form_reconn_target_file_path(
            event.dom.UUIDString())
        actor_process = action.execute(target_file,
                                       "uuid:%s" % event.dom.UUIDString())

        nimo_event_actions.EventActionProcessCollector.add(event,
                                                           actor_process)


def process_queued_events(event_q):

    # Process as many events as possible currently queued.
    # Currently serially processing, but can implement green pool here.

    while not event_q.empty():
        event = event_q.get()
        act_on_event(event)


def wait_and_dispatch_queued_events(event_queued_notify_recv,
                                    event_q):
    # Wait to be notified that there are some
    # events pending in the queue

    while True:
        try:
            _c = None
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

        process_queued_events(event_q)
