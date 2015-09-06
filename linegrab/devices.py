""" Real and simulated devices for providing stdin/stdout pipe based
communication with camera control devices.
"""

import numpy
import logging

log = logging.getLogger(__name__)

class SimulatedPipeDevice(object):
    """ Use the pipe device interface, return a cycling test pattern of
    data.
    """

    def __init__(self, pattern_jump=1, top_level=1000):
        log.debug("Startup")
        self.pattern_position = 0
        self.data_length = 1024
        self.top_level = top_level
        self.pattern_jump = pattern_jump

    def setup_pipe(self):
        log.info("Setup pipe device")
        return True

    def grab_pipe(self):
        """ Create a cycling test pattern based on the current position
        """
        log.debug("Grab pipe")
        start = self.pattern_position 
        end = self.pattern_position + self.top_level
        data = numpy.linspace(start, end, 1024)

        self.pattern_position += self.pattern_jump
        if self.pattern_position >= self.top_level:
            self.pattern_position = 0

        return True, data

    def close_pipe(self):
        log.info("Close pipe device")
        self.pattern_position = 0
        return True
