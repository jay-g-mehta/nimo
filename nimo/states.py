import libvirt

# https://libvirt.org/html/libvirt-libvirt-domain.html#virDomainEventType

vir_domain_event_type = {
    libvirt.VIR_DOMAIN_EVENT_DEFINED: 'VIR_DOMAIN_EVENT_DEFINED',
    libvirt.VIR_DOMAIN_EVENT_UNDEFINED: 'VIR_DOMAIN_EVENT_UNDEFINED',
    libvirt.VIR_DOMAIN_EVENT_STARTED: 'VIR_DOMAIN_EVENT_STARTED',
    libvirt.VIR_DOMAIN_EVENT_SUSPENDED: 'VIR_DOMAIN_EVENT_SUSPENDED',
    libvirt.VIR_DOMAIN_EVENT_RESUMED: 'VIR_DOMAIN_EVENT_RESUMED',
    libvirt.VIR_DOMAIN_EVENT_STOPPED: 'VIR_DOMAIN_EVENT_STOPPED',
    libvirt.VIR_DOMAIN_EVENT_SHUTDOWN: 'VIR_DOMAIN_EVENT_SHUTDOWN',
    libvirt.VIR_DOMAIN_EVENT_PMSUSPENDED: 'VIR_DOMAIN_EVENT_PMSUSPENDED',
    libvirt.VIR_DOMAIN_EVENT_CRASHED: 'VIR_DOMAIN_EVENT_CRASHED',
    # The following are commented as not define for libvirt-python,
    # but are defined in libvirt c module
    # libvirt.VIR_DOMAIN_EVENT_LAST: 'VIR_DOMAIN_EVENT_LAST'
}


def event_type_to_str(virtDomEventType):
    '''Returns str format of domain event type.
    Returns None for failures/unknown event types
    '''
    return vir_domain_event_type.get(virtDomEventType)


virDomainEventDefinedDetailType = {
    libvirt.VIR_DOMAIN_EVENT_DEFINED_ADDED:
        'VIR_DOMAIN_EVENT_DEFINED_ADDED: Newly created config file',
    libvirt.VIR_DOMAIN_EVENT_DEFINED_UPDATED:
        'VIR_DOMAIN_EVENT_DEFINED_UPDATED: Changed config file',
    # The following are commented as not define for libvirt-python,
    # but are defined in libvirt c module
    # libvirt.VIR_DOMAIN_EVENT_DEFINED_RENAMED:
    #    'VIR_DOMAIN_EVENT_DEFINED_RENAMED: Domain was renamed',
    # libvirt.VIR_DOMAIN_EVENT_DEFINED_FROM_SNAPSHOT:
    #    'VIR_DOMAIN_EVENT_DEFINED_FROM_SNAPSHOT: '
    #    'Config was restored from a snapshot',
    # libvirt.VIR_DOMAIN_EVENT_DEFINED_LAST:
    #    'VIR_DOMAIN_EVENT_DEFINED_LAST',
}

virDomainEventUndefinedDetailType = {
    libvirt.VIR_DOMAIN_EVENT_UNDEFINED_REMOVED:
        'VIR_DOMAIN_EVENT_UNDEFINED_REMOVED: Deleted the config file',
    # The following are commented as not define for libvirt-python,
    # but are defined in libvirt c module
    # libvirt.VIR_DOMAIN_EVENT_UNDEFINED_RENAMED:
    #    'VIR_DOMAIN_EVENT_UNDEFINED_RENAMED: Domain was renamed',
    # libvirt.VIR_DOMAIN_EVENT_UNDEFINED_LAST:
    #    'VIR_DOMAIN_EVENT_UNDEFINED_LAST'
}

virDomainEventStartedDetailType = {
    libvirt.VIR_DOMAIN_EVENT_STARTED_BOOTED:
        'VIR_DOMAIN_EVENT_STARTED_BOOTED: Normal startup from boot',
    libvirt.VIR_DOMAIN_EVENT_STARTED_MIGRATED:
        'VIR_DOMAIN_EVENT_STARTED_MIGRATED: '
        'Incoming migration from another host',
    libvirt.VIR_DOMAIN_EVENT_STARTED_RESTORED:
        'VIR_DOMAIN_EVENT_STARTED_RESTORED: Restored from a state file',
    libvirt.VIR_DOMAIN_EVENT_STARTED_FROM_SNAPSHOT:
        'VIR_DOMAIN_EVENT_STARTED_FROM_SNAPSHOT: Restored from snapshot',
    libvirt.VIR_DOMAIN_EVENT_STARTED_WAKEUP:
        'VIR_DOMAIN_EVENT_STARTED_WAKEUP: Started due to wakeup event',
    # The following are commented as not define for libvirt-python,
    # but are defined in libvirt c module
    # libvirt.VIR_DOMAIN_EVENT_STARTED_LAST: 'VIR_DOMAIN_EVENT_STARTED_LAST'
}

virDomainEventSuspendedDetailType = {
    libvirt.VIR_DOMAIN_EVENT_SUSPENDED_PAUSED:
        'VIR_DOMAIN_EVENT_SUSPENDED_PAUSED: Normal suspend due to admin pause',
    libvirt.VIR_DOMAIN_EVENT_SUSPENDED_MIGRATED:
        'VIR_DOMAIN_EVENT_SUSPENDED_MIGRATED: Suspended for offline migration',
    libvirt.VIR_DOMAIN_EVENT_SUSPENDED_IOERROR:
        'VIR_DOMAIN_EVENT_SUSPENDED_IOERROR: '
        'Suspended due to a disk I/O error',
    libvirt.VIR_DOMAIN_EVENT_SUSPENDED_WATCHDOG:
        'VIR_DOMAIN_EVENT_SUSPENDED_WATCHDOG: '
        'Suspended due to a watchdog firing',
    libvirt.VIR_DOMAIN_EVENT_SUSPENDED_RESTORED:
        'VIR_DOMAIN_EVENT_SUSPENDED_RESTORED: Restored from paused state file',
    libvirt.VIR_DOMAIN_EVENT_SUSPENDED_FROM_SNAPSHOT:
        'VIR_DOMAIN_EVENT_SUSPENDED_FROM_SNAPSHOT: '
        'Restored from paused snapshot',
    libvirt.VIR_DOMAIN_EVENT_SUSPENDED_API_ERROR:
        'VIR_DOMAIN_EVENT_SUSPENDED_API_ERROR: '
        'suspended after failure during libvirt API call',
    # The following are commented as not define for libvirt-python,
    # but are defined in libvirt c module
    # libvirt.VIR_DOMAIN_EVENT_SUSPENDED_POSTCOPY:
    #    'VIR_DOMAIN_EVENT_SUSPENDED_POSTCOPY: '
    #    'suspended for post-copy migration',
    # libvirt.VIR_DOMAIN_EVENT_SUSPENDED_POSTCOPY_FAILED:
    #    'VIR_DOMAIN_EVENT_SUSPENDED_POSTCOPY_FAILED: '
    #    'suspended after failed post-copy',
    # libvirt.VIR_DOMAIN_EVENT_SUSPENDED_LAST:
    #    'VIR_DOMAIN_EVENT_SUSPENDED_LAST',
}

virDomainEventResumedDetailType = {
    libvirt.VIR_DOMAIN_EVENT_RESUMED_UNPAUSED:
        'VIR_DOMAIN_EVENT_RESUMED_UNPAUSED: '
        'Normal resume due to admin unpause',
    libvirt.VIR_DOMAIN_EVENT_RESUMED_MIGRATED:
        'VIR_DOMAIN_EVENT_RESUMED_MIGRATED: '
        'Resumed for completion of migration',
    libvirt.VIR_DOMAIN_EVENT_RESUMED_FROM_SNAPSHOT:
        'VIR_DOMAIN_EVENT_RESUMED_FROM_SNAPSHOT: Resumed from snapshot',
    # The following are commented as not define for libvirt-python,
    # but are defined in libvirt c module
    # libvirt.VIR_DOMAIN_EVENT_RESUMED_POSTCOPY:
    #    'VIR_DOMAIN_EVENT_RESUMED_POSTCOPY: '
    #    'Resumed, but migration is still running in post-copy mode',
    # libvirt.VIR_DOMAIN_EVENT_RESUMED_LAST: 'VIR_DOMAIN_EVENT_RESUMED_LAST'
}

virDomainEventStoppedDetailType = {
    libvirt.VIR_DOMAIN_EVENT_STOPPED_SHUTDOWN:
        'VIR_DOMAIN_EVENT_STOPPED_SHUTDOWN: Normal shutdown',
    libvirt.VIR_DOMAIN_EVENT_STOPPED_DESTROYED:
        'VIR_DOMAIN_EVENT_STOPPED_DESTROYED: Forced poweroff from host',
    libvirt.VIR_DOMAIN_EVENT_STOPPED_CRASHED:
        'VIR_DOMAIN_EVENT_STOPPED_CRASHED: Guest crashed',
    libvirt.VIR_DOMAIN_EVENT_STOPPED_MIGRATED:
        'VIR_DOMAIN_EVENT_STOPPED_MIGRATED: Migrated off to another host',
    libvirt.VIR_DOMAIN_EVENT_STOPPED_SAVED:
        'VIR_DOMAIN_EVENT_STOPPED_SAVED: Saved to a state file',
    libvirt.VIR_DOMAIN_EVENT_STOPPED_FAILED:
        'VIR_DOMAIN_EVENT_STOPPED_FAILED: Host emulator/mgmt failed',
    libvirt.VIR_DOMAIN_EVENT_STOPPED_FROM_SNAPSHOT:
        'VIR_DOMAIN_EVENT_STOPPED_FROM_SNAPSHOT: offline snapshot loaded',
    # The following are commented as not define for libvirt-python,
    # but are defined in libvirt c module
    # libvirt.VIR_DOMAIN_EVENT_STOPPED_LAST: 'VIR_DOMAIN_EVENT_STOPPED_LAST'
}

virDomainEventShutdownDetailType = {
    libvirt.VIR_DOMAIN_EVENT_SHUTDOWN_FINISHED:
        'VIR_DOMAIN_EVENT_SHUTDOWN_FINISHED: Guest finished shutdown sequence',
    # The following are commented as not define for libvirt-python,
    # but are defined in libvirt c module
    # libvirt.VIR_DOMAIN_EVENT_SHUTDOWN_GUEST:
    #    'VIR_DOMAIN_EVENT_SHUTDOWN_GUEST: '
    #    'Domain finished shutting down after request from '
    #    'the guest itself (e.g. hardware-specific action)',
    # libvirt.VIR_DOMAIN_EVENT_SHUTDOWN_HOST:
    #    'VIR_DOMAIN_EVENT_SHUTDOWN_HOST: '
    #    'Domain finished shutting down after request from the '
    #    'host (e.g. killed by a signal)',
    # libvirt.VIR_DOMAIN_EVENT_SHUTDOWN_LAST: 'VIR_DOMAIN_EVENT_SHUTDOWN_LAST'
}

virDomainEventPMSuspendedDetailType = {
    libvirt.VIR_DOMAIN_EVENT_PMSUSPENDED_MEMORY:
        'VIR_DOMAIN_EVENT_PMSUSPENDED_MEMORY: '
        'Guest was PM suspended to memory',
    libvirt.VIR_DOMAIN_EVENT_PMSUSPENDED_DISK:
        'VIR_DOMAIN_EVENT_PMSUSPENDED_DISK: Guest was PM suspended to disk',
    # The following are commented as not define for libvirt-python,
    # but are defined in libvirt c module
    # libvirt.VIR_DOMAIN_EVENT_PMSUSPENDED_LAST:
    #     'VIR_DOMAIN_EVENT_PMSUSPENDED_LAST'
}

virDomainEventCrashedDetailType = {
    libvirt.VIR_DOMAIN_EVENT_CRASHED_PANICKED:
        'VIR_DOMAIN_EVENT_CRASHED_PANICKED: Guest was panicked',
    # The following are commented as not define for libvirt-python,
    # but are defined in libvirt c module
    # libvirt.VIR_DOMAIN_EVENT_CRASHED_LAST: 'VIR_DOMAIN_EVENT_CRASHED_LAST'
}

vir_domain_event_type_detail_map = {
    libvirt.VIR_DOMAIN_EVENT_DEFINED: virDomainEventDefinedDetailType,
    libvirt.VIR_DOMAIN_EVENT_UNDEFINED: virDomainEventUndefinedDetailType,
    libvirt.VIR_DOMAIN_EVENT_STARTED: virDomainEventStartedDetailType,
    libvirt.VIR_DOMAIN_EVENT_SUSPENDED: virDomainEventSuspendedDetailType,
    libvirt.VIR_DOMAIN_EVENT_RESUMED: virDomainEventResumedDetailType,
    libvirt.VIR_DOMAIN_EVENT_STOPPED: virDomainEventStoppedDetailType,
    libvirt.VIR_DOMAIN_EVENT_SHUTDOWN: virDomainEventShutdownDetailType,
    libvirt.VIR_DOMAIN_EVENT_PMSUSPENDED: virDomainEventPMSuspendedDetailType,
    libvirt.VIR_DOMAIN_EVENT_CRASHED: virDomainEventCrashedDetailType,
}


def event_detail_to_str(event_type, event_detail):
    type_detail_dict = vir_domain_event_type_detail_map.get(event_type, {})
    return type_detail_dict.get(event_detail, None)
