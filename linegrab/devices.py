""" Real and simulated devices for providing stdin/stdout pipe based
communication with camera control devices.
"""

import sys
import numpy
import struct
import logging

from subprocess import Popen, PIPE

log = logging.getLogger(__name__)

class DalsaCobraDevice(object):
    """ Use a Dalsa frame grabber and the stdin/stdout customized
    example from Sapera.
    """
    def __init__(self):
        super(DalsaCobraDevice, self).__init__()
        log.debug("DCD Startup")


    def setup_pipe(self):
        """ Create a pipe connection to the csharp version of the single
        line grabber on the console example from Dalsa.
        """
        log.info("Setup pipe device")
        prefix = "linegrab\\GrabConsole\\CSharp\\bin\\Debug\\"

        cmd = "%s\\SapNETCSharpGrabConsole.exe" % prefix
        ccf = "%s\\prcinternal.ccf" % prefix
        log.debug("open %s, %s", cmd, ccf)
        try:
            opts = [cmd, 'grab', 'Xcelera-CL_LX1_1', '0', ccf]
            self.pipe = Popen(opts, stdin=PIPE, stdout=PIPE)
        except:
            log.critical("Failure to setup pipe: " + str(sys.exc_info()))
            return False

        return True


    def grab_pipe(self):
        """ Issue a newline, get a line of data over the pipes.
        """

        line = self.pipe.stdout.readline().replace('\n', '')
        log.info("READ " + str(line))
        log.info("WR enter to trigger snap")
        log.info("\n")
        self.pipe.stdin.write("\n")

        line = self.pipe.stdout.readline().replace('\n', '')
        log.info("READ " + str(line))
        log.info("WR enter to trigger save")
        log.info("\n")
        self.pipe.stdin.write("\n")

        line = self.pipe.stdout.readline().replace('\n', '')
        log.info("READ " + str(line))
        log.info("\n")

        #time.sleep(1)
        log.info("Open file")
        result, data = self.grab_data("test.raw")
        log.info(str(data[0:3]))
        log.info("Done file")
        #time.sleep(1)

        log.info("WR enter to trigger repeat")
        self.pipe.stdin.write("\n")
        line = self.pipe.stdout.readline().replace('\n', '')
        log.info("READ " + str(line))
        log.info("\n")

        return result, data

    def grab_data(self, in_filename="tools\\test.raw"):
        """ Read from the given raw pixel file as extracted from the
        DALSA command line example program. Return numpy array of pixel
        values.
        """
        img_data = []
        try:
            in_file = open(in_filename, 'rb')
            all_data = in_file.read()
            in_file.close()
            pos = 0
            while pos < 4095:
                pixel_one = all_data[pos] + all_data[pos+1]
                data_pak = struct.unpack("H", pixel_one)
                img_data.append(data_pak[0])
                pos += 2

            return 1, img_data
        except:
            log.critical("Problem reading " + str(in_filename) + \
                          str(sys.exc_info()))
            return 0, "fail"

        return 0, "done"


    def close_pipe(self):
        """ write multiple q's to close the stdout pipe.
        """
        log.info("Close pipe")
        # write a bunch of q's and read the lines to close it out
        try:
            for i in range(10):
                log.info("WR q" + str(i))
                self.pipe.stdin.write("q\n")
                line = self.pipe.stdout.readline().replace('\n','')
                
            self.pipe.stdin.flush()
            self.pipe.stdout.flush()
        except:
            log.warn("close pipe fail: " + str(sys.exc_info()))

        return 1



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
        """ Create a simulated connection.
        """
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
        """ Simulated the closing of the pipe.
        """
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
        self.raman_peaks = 10
        self.noise_floor = 50
        self.noise_ceiling = 150
        nru = numpy.random.uniform

        low_data = nru(100, 200, 2048)
        blk = numpy.linspace(0, 0, 2048)

        # up to half the width, add a value that is at least greater
        # than a threshold, then move the threshold up
        width = 10

        half = width / 2
        min_gap = 10


        for position in range(self.raman_peaks):

            # get a random peak within the range
            peak_pos = int(nru(100, 2037, 1))
            peak_height = int(nru(500, 1000, 1))

            floor = peak_height + min_gap
            peak_x = peak_pos

            for item in range(half):
                new_floor = floor + min_gap
                new_height = nru(floor, new_floor, 1)
                new_height = int(new_height)
                floor = new_floor
                blk[peak_x] = new_height
                peak_x += 1

            for item in range(half):
                new_floor = floor - min_gap
                new_height = nru(floor, new_floor, 1)
                new_height = int(new_height)
                floor = new_floor
                blk[peak_x] = new_height
                peak_x += 1

        self.base_data = low_data + blk


    def grab_pipe(self):
        """ Apply randomness at each grab.
        """

        nru = numpy.random.uniform
        noise_data = nru(self.noise_floor, self.noise_ceiling, 2048)
        new_data = self.base_data + noise_data
        return True, new_data
