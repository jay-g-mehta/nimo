import eventlet
# green the world
eventlet.monkey_patch()

import libvirt

from oslo_config import cfg
from oslo_log import log as logging

from eventlet import patcher

from nimo import utils as nimo_utils
from nimo import states as nimo_states
from nimo import event_queue as nimo_event_queue
from nimo import event_processor as nimo_event_processor
from nimo import dispatcher as nimo_dispatcher


CONF = cfg.CONF
LOG = logging.getLogger(__name__)

native_threading = patcher.original("threading")


eventLoopThread = None
event_queue = None
event_queued_notify_send = None
event_queued_notify_recv = None


def queue_virt_lifecycle_event(conn, dom, event, detail, opaque_userdata):
    # NOTE(jay): Native threads cannot use LOG.
    # In particular any use of logging is forbidden, since it will confuse
    # eventlet's greenthread integration.
    # Due to limitations with eventlet locking we cannot use the
    # logging API inside the called function.

    virt_event = nimo_event_queue.VirtLifeCycleEvent(conn, dom,
                                                     event, detail,
                                                     opaque_userdata)
    # print "Queuing virt event: %s" % virt_event
    # LOG.debug("Queuing virt event: %s", virt_event)

    event_queue.put(virt_event)

    # Lets wake up the green thread dispatchers
    c = ' '.encode()
    event_queued_notify_send.write(c)
    event_queued_notify_send.flush()
    # LOG.debug("wake up queued event dispatchers...")
    # print "wake up queued event dispatchers..."


def domain_lifecycle_event_callback(conn, dom, event, detail, opaque_userdata):
    ''' callback invoked when a domain lifecycle event occurs
    * @conn: virConnect connection
    * @dom: The domain on which the event occurred
    * @event: The specific virDomainEventType which occurred
    * @detail: event specific detail information. int type.
    * @opaque: opaque user data
    '''
    # NOTE(jay): Native threads cannot use LOG.
    # In particular any use of logging is forbidden, since it will confuse
    # eventlet's greenthread integration.
    # Due to limitations with eventlet locking we cannot use the
    # logging API inside the called function.
    """
    LOG.info("Event type= '%s', detail= '%s' "
             "occured on domain= '%s' UUID= '%s'",
             nimo_states.event_type_to_str(event),
             nimo_states.event_detail_to_str(event, detail),
             dom.name(), dom.UUIDString())
    """
    # Current thread = Thread libvirtEventLoop

    queue_virt_lifecycle_event(conn, dom, event, detail, opaque_userdata)
    print "returned from domain_lifecycle_event_callback"


def runVirDefaultEventLoop():
    '''Run Libvirt default event loop
    implementaion forever
    '''
    # NOTE(jay): Native threads cannot use LOG.
    # In particular any use of logging is forbidden, since it will confuse
    # eventlet's greenthread integration.
    # Due to limitations with eventlet locking we cannot use the
    # logging API inside the called function.

    while True:
        # Thread blocks until event occurs or times out. virEventPollRunOnce()
        libvirt.virEventRunDefaultImpl()
        # Current thread = Thread libvirtEventLoop
        # Loop another round to get call back for next event/timeout


def startVirEventLoop():
    '''Register Libvirt default event loop
    implementation and call to run event loop on a
    separate native thread forever.
    '''
    global eventLoopThread

    # Register libvirts default event loop implementation
    libvirt.virEventRegisterDefaultImpl()

    eventLoopThread = native_threading.Thread(target=runVirDefaultEventLoop,
                                              name="libvirtEventLoop")
    eventLoopThread.setDaemon(True)
    eventLoopThread.start()


def register_libvirt_opts():
    '''Register libvirt opts'''

    libvirt_opts = [
        cfg.StrOpt('uri',
                   default=None,
                   help='uri of the hypervisor. Used to connect'
                        ' to the hypervisor. URI format is:'
                        'driver[+transport]://[username@][hostname]'
                        '[:port]/[path][?extraparameters]'), ]

    libvirt_opt_group = cfg.OptGroup(name='libvirt',
                                     title='Libvirt  opts group')

    CONF.register_group(libvirt_opt_group)
    CONF.register_opts(libvirt_opts, group=libvirt_opt_group)


def init_nimo():
    nimo_utils.oslo_logger_config_setup()
    register_libvirt_opts()

    # Lets create a queue to store libvirt events to process later
    global event_queue
    event_queue = nimo_event_queue.VirtEventQueue()


def nimo_main(nimo_mode):

    init_nimo()

    global event_queue

    # initialize pipe between 2 threads.
    global event_queued_notify_send
    global event_queued_notify_recv

    if nimo_mode == 'greenthread':
        event_queued_notify_recv, event_queued_notify_send = \
            nimo_utils.create_green_pipe()
    else:
        event_queued_notify_recv, event_queued_notify_send = \
            nimo_utils.create_pipe()

    # Start and run libvirt default event loop implementation
    startVirEventLoop()

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
                                domain_lifecycle_event_callback,
                                {'prog': __file__, 'name': __name__})

    conn.setKeepAlive(5, 3)

    dispatcher_thread = None
    dispatcher_thread_type = nimo_mode

    while conn.isAlive() == 1:

        # Create dispatcher thread to read queue and dispatch events
        dispatcher_thread = nimo_dispatcher.Dispatcher.create(
            dispatcher_thread_type,
            nimo_event_processor.wait_and_dispatch_queued_events,
            event_queued_notify_recv,
            event_queue)
        # TODO(jay): Implement sighandlers, when nimo mode = 'nativethread'

        if nimo_mode == 'nativethread':
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


def native_nimo():
    '''When NIMO is to be run using all native threads'''
    # NOTE(jay): monkey_patch() should not be called,
    # otherwise LOG cannot be used.
    nimo_main('nativethread')


def green_nimo():
    '''Creates green dispatcher, and, main & VirtEventLoop is native thread'''
    # NOTE(jay): monkey_patch() should be called.
    # All native threads, including main, are not safe to use LOG
    nimo_main('greenthread')


def main():
    '''Call either green_nimo() or native_nimo()'''
    green_nimo()


if __name__ == '__main__':
    main()
