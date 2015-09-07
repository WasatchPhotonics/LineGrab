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

class SimulatedSpectraDevice(SimulatedPipeDevice):
    """ Given a class of spectra, create a default waveform, and return
    randomized data along that waveform.
    """
    def __init__(self, spectra_type="raman"):
        super(SimulatedSpectraDevice, self).__init__()
        self.spectra_type = spectra_type

        if self.spectra_type == "raman":
            self.waveform = self.generate_raman()

    def generate_raman(self):
        """ A raman waveform in this context is a baseline with peaks at
        various extents.
        """
        self.raman_peaks = 3
        self.baseline = 100
        self.noise_floor = 50
        self.noise_ceiling = 150

        # First make a pass at the baseline
        nru = numpy.random.uniform
        low_data = nru(100, 200, 2048)

        blk = numpy.linspace(0, 0, 2048)
        for item in range(self.raman_peaks):
            # get a random position for the peak
            peak_pos = nru(100, 2037, 1)
            peak_height = nru(self.baseline, 4000, 1)

            blk = numpy.linspace(0, 0, 2048)
            blk[peak_pos] = peak_height
        
        self.base_data = low_data + blk

    def grab_pipe(self):
        """ Apply randomness at each grab.
        """
        
        nru = numpy.random.uniform
        noise_data = nru(self.noise_floor, self.noise_ceiling, 2048)
        new_data = self.base_data + noise_data
        return True, new_data
            
