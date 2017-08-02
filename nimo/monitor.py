import libvirt
import time
import threading

from oslo_config import cfg
from oslo_log import log as logging

from nimo import utils as nimo_utils
from nimo import states as nimo_states


CONF = cfg.CONF
LOG = logging.getLogger(__name__)
eventLoopThread = None


def domain_lifecycle_event_callback(conn, dom, event, detail, opaque_userdata):
    ''' callback invoked when a domain lifecycle event occurs
    * @conn: virConnect connection
    * @dom: The domain on which the event occurred
    * @event: The specific virDomainEventType which occurred
    * @detail: event specific detail information. int type.
    * @opaque: opaque user data
    '''
    LOG.info("Event type= '%s', detail= '%s' "
             "occured on domain= '%s' UUID= '%s'",
             nimo_states.event_type_to_str(event),
             nimo_states.event_detail_to_str(event, detail),
             dom.name(), dom.UUIDString())
    # Current thread = Thread libvirtEventLoop


def runVirDefaultEventLoop():
    '''Run Libvirt default event loop
    implementaion forever
    '''
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

    eventLoopThread = threading.Thread(target=runVirDefaultEventLoop,
                                       name="libvirtEventLoop")
    eventLoopThread.setDaemon(True)
    eventLoopThread.start()

    nimo_utils.log_naitve_threads()


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


def main():

    nimo_utils.oslo_logger_config_setup()
    register_libvirt_opts()

    startVirEventLoop()

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

    while conn.isAlive() == 1:
        time.sleep(1)


if __name__ == '__main__':
    main()
