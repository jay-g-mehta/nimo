import sys
import threading

from oslo_config import cfg
from oslo_log import log as logging

from nimo import version


LOG = logging.getLogger(__name__)
CONF = cfg.CONF


def log_naitve_threads():
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
