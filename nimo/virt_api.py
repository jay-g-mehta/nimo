"""This file interacts with libvirt to register and use event loop"""
import libvirt

from eventlet import patcher


native_threading = patcher.original("threading")


def _runVirDefaultEventLoop():
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

    # Register libvirts default event loop implementation
    libvirt.virEventRegisterDefaultImpl()

    event_loop_thread = native_threading.Thread(target=_runVirDefaultEventLoop,
                                                name="libvirtEventLoop")
    event_loop_thread.setDaemon(True)
    event_loop_thread.start()

    return event_loop_thread
