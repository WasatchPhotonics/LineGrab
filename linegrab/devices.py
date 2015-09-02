""" Real and simulated devices for providing stdin/stdout pipe based
communication with camera control devices.
"""

import logging
log = logging.getLogger(__name__)

class SimulatedPipeDevice(object):

    def __init__(self):
        log.debug("Startup")

    def setup_pipe(self):
        log.info("Create pipe device")
        return True

