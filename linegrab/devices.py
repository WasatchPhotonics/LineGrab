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
 
            # get a random width of the peak
            peak_width = 30

            # generate a new, blank array, add the peaks

            peak_start = peak_pos - (peak_width / 2)
            peak_stop = peak_pos + (peak_width / 2)

            heights = numpy.linspace(0, 0, peak_width)
            for item in range(peak_width/2):
                heights[item] = peak_height / (item + 1)

            for item in range(peak_width/2):
                offset = (peak_width - 1 - item)
                heights[offset] = peak_height / (item + 1)

            position = peak_start
            while position < peak_stop:
                sub_pos = 0
                for item in range(len(heights)):
                    blk[int(position) + sub_pos] = heights[item]
                    sub_pos += 1
                position += 1
                


        
        self.base_data = low_data + blk

    def grab_pipe(self):
        """ Apply randomness at each grab.
        """
        
        nru = numpy.random.uniform
        noise_data = nru(self.noise_floor, self.noise_ceiling, 2048)
        new_data = self.base_data + noise_data
        return True, new_data
            
