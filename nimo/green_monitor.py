import eventlet
# green the world
eventlet.monkey_patch()

import libvirt
import reconn

from oslo_config import cfg
from oslo_log import log as logging

from nimo import utils as nimo_utils
from nimo import event_queue as nimo_event_queue
from nimo import event_processor as nimo_event_processor
from nimo import dispatcher as nimo_dispatcher
from nimo import event_actions as nimo_event_actions
from nimo import virt_api as nimo_virt_api
from nimo import callbacks as nimo_callbacks


CONF = cfg.CONF
LOG = logging.getLogger(__name__)


def init_nimo():
    reconn.setup_reconn()

    nimo_utils.oslo_logger_config_setup()
    nimo_utils.register_libvirt_opts()
    nimo_utils.register_default_nimo_opts()

    # Setup action to be taken when event occurs
    nimo_event_actions.EventActionMapper.set_actions()

    # Lets create a queue to store libvirt events to process later
    nimo_callbacks.event_q = nimo_event_queue.VirtEventQueue()

    nimo_callbacks.event_queued_notify_recv,\
        nimo_callbacks.event_queued_notify_send = \
        nimo_utils.create_green_pipe()


def nimo_main(nimo_mode):
    init_nimo()

    # Start and run libvirt default event loop implementation
    nimo_virt_api.startVirEventLoop()

    # In 'greenthread' nimo mode, not safe to call this,
    # but it is safe here as green thread are not yet spawned.
    # Lets log all native threads, before spawning green thread
    nimo_utils.log_native_threads()

    # In 'greenthread' nimo mode, not safe to use LOG,
    # but it is safe here as green thread are not yet spawned.
    LOG.info("Connecting to hypervisor using connection uri=%s",
             cfg.CONF.libvirt.uri)
    conn = libvirt.openReadOnly(cfg.CONF.libvirt.uri)
    if conn is None:
        LOG.error('Failed to open connection to uri=%s' %
                  cfg.CONF.libvirt.uri)
        exit(1)

    # Register a callback to receive notifications of domain lifecycle events
    # occurring on a connection
    conn.domainEventRegisterAny(None, libvirt.VIR_DOMAIN_EVENT_ID_LIFECYCLE,
                                nimo_callbacks.domain_lifecycle_event_callback,
                                {'prog': __file__, 'name': __name__})

    conn.setKeepAlive(5, 3)

    dispatcher_thread = None
    dispatcher_thread_type = nimo_mode

    while conn.isAlive() == 1:

        # Create dispatcher thread to read queue and dispatch events
        dispatcher_thread = nimo_dispatcher.Dispatcher.create(
            dispatcher_thread_type,
            nimo_event_processor.wait_and_dispatch_queued_events,
            nimo_callbacks.event_queued_notify_recv,
            nimo_callbacks.event_q)
        # TODO(jay): Implement sighandlers, when nimo mode = 'nativethread'

        LOG.debug("Main-thread waiting forever "
                  "on Dispatcher thread to finish")

        dispatcher_thread.join()

        # This should be safe as green thread is dead
        LOG.error("Dispatcher thread exited.")

        # at this point, spin back up a dispatcher thread or exit process
        eventlet.sleep(1)

    else:
        # If connection with hypervisor breaks, exit.
        # TODO(jay): Ideally, terminate all threads and recall this main().
        LOG.error("connection to Host is broken. Exiting")

        exit(1)


def main():
    '''Creates green dispatcher, and, main & VirtEventLoop is native thread'''
    # NOTE(jay): monkey_patch() should be called.
    # All native threads, including main, are not safe to use LOG
    nimo_main('greenthread')


if __name__ == '__main__':
    main()
