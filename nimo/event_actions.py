from abc import ABCMeta, abstractmethod
import socket
import multiprocessing

import libvirt
import reconn

from oslo_config import cfg
from oslo_log import log as logging

from nimo import periodic_task as nimo_periodic_task
from nimo import states as nimo_states


CONF = cfg.CONF
LOG = logging.getLogger(__name__)


class EventActionProcessCollector(object):
    """Maps event to action process to track status
    of action process and perform clean up when they die"""
    __action_process_q = []

    @classmethod
    def add(cls, event, action_process):
        cls.__action_process_q.append((event, action_process))

    @classmethod
    @nimo_periodic_task.periodic_task(30)
    def clean(cls):
        index = 0
        for iter_index in range(len(cls.__action_process_q)):
            event, action_process = cls.__action_process_q[index]
            if not action_process.is_alive():
                action_process.join()
                LOG.info("Event action process %s exited %s",
                         action_process.name, action_process.exitcode)
                cls.__action_process_q.pop(index)
                index = index - 1
            index = index + 1


class EventActionMapper(object):
    """Decides what action to take for an event"""
    # Define mapping for (event type, event detail) to action
    _event_action_map = {}

    @classmethod
    def set_actions(cls):
        '''Create a map of event to action'''
        cls._event_action_map[
            (libvirt.VIR_DOMAIN_EVENT_STARTED,
             libvirt.VIR_DOMAIN_EVENT_STARTED_BOOTED
             )] = ReconnEventAction()

        LOG.info("NIMO monitoring for events: %s",
                 nimo_states.event_detail_to_str(
                     libvirt.VIR_DOMAIN_EVENT_STARTED,
                     libvirt.VIR_DOMAIN_EVENT_STARTED_BOOTED
                 ))

    @classmethod
    def get_action(cls, event_type, event_detail):
        return cls._event_action_map.get((event_type, event_detail))


class EventAction(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def setup(self, *args, **kwargs):
        pass

    @abstractmethod
    def execute(self, *args, **kwargs):
        pass

    @abstractmethod
    def destroy(self, *args, **kwargs):
        pass


class ReconnEventAction(EventAction):
    """Event action which performs reconnaissance on
    console.log file of the VM instance. Uses reconn
    module. A new daemon process is created to begin reconn.
    """
    _reconn_log_file = '/var/log/reconn/reconn.log'
    _reconn_msg_format = '''{{
                             "event_type": "compute.instance.{name}",
                             "priority": "INFO",
                             "publisher_id": "nimo.''' + socket.gethostname() + '''",
                             "payload": {{
                                "instance_id": "{uuid}"
                             }},
                             "line":"{line}",
                             "matched_pattern": "{matched_pattern}",
                             "timestamp": "{timestamp}" }}'''.replace(" ", "")

    def __init__(self,
                 config_file=None,
                 log_file=_reconn_log_file,
                 msg_format=_reconn_msg_format):
        if config_file is None:
            self.reconn_config_file = CONF.reconn_config_path
        else:
            self.reconn_config_file = config_file
        self.reconn_log_file = log_file
        self.reconn_msg_format = msg_format

    def setup(self, *args, **kwargs):
        pass

    def execute(self, target_file, user_data, *args, **kwargs):
        """Creates and returns a new daemon process which runs reconn."""
        reconn_process = multiprocessing.Process(
            name='reconn_%s' % target_file,
            target=reconn.start_reconn,
            args=(target_file,
                  self.reconn_config_file,
                  self.reconn_log_file,
                  self.reconn_msg_format,
                  user_data))
        reconn_process.daemon = True
        reconn_process.start()
        return reconn_process

    def destroy(self, *args, **kwargs):
        pass
