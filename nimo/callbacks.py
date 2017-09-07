from nimo import event_queue as nimo_event_queue


# queue to store libvirt events to process later
event_q = None

# pipe between 2 threads.
event_queued_notify_send = None
event_queued_notify_recv = None


def _queue_virt_lifecycle_event(conn, dom, event, detail, opaque_userdata):
    global event_q
    global event_queued_notify_send
    global event_queued_notify_recv

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

    event_q.put(virt_event)

    # Lets wake up the dispatchers thread
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

    _queue_virt_lifecycle_event(conn, dom, event, detail, opaque_userdata)
    print "returned from domain_lifecycle_event_callback"
