import os
import sys
import threading

from eventlet import greenio

from oslo_config import cfg
from oslo_log import log as logging

from nimo import version


LOG = logging.getLogger(__name__)
CONF = cfg.CONF


def log_native_threads():
    '''Log native threads to log file
    '''
    out = "%d active threads: " % threading.active_count()
    for t in threading.enumerate():
        out = out + "'%s', " % t.name

    LOG.info("%s", out.rstrip(", "))


def oslo_logger_config_setup():
    '''Register oslo logger opts.
    Initialize oslo config CONF
    '''

    logging.register_options(CONF)
    CONF(sys.argv[1:], project='nimo',
         version=version.version_string())
    logging.setup(CONF, "nimo")


def create_green_pipe():
    """Create a green pipe for threads to synchronize on.
    """
    rpipe, wpipe = os.pipe()
    write_file_obj = greenio.GreenPipe(wpipe, 'wb', 0)
    read_file_obj = greenio.GreenPipe(rpipe, 'rb', 0)
    return (read_file_obj, write_file_obj)


def create_pipe():
    """Create a pipe for threads to synchronize on.
    Returns read and write file objects for pipe ends.
    """
    rpipe, wpipe = os.pipe()
    write_file_obj = os.fdopen(wpipe, 'wb', 0)
    read_file_obj = os.fdopen(rpipe, 'rb', 0)
    return (read_file_obj, write_file_obj)
