""" tests for a wasatch photonics cobra over dalsa card.
"""

import unittest
import logging

from testfixtures import LogCapture

from linegrab.devices import DalsaCobraDevice

log = logging.getLogger()
logging.basicConfig(level=logging.DEBUG)
frmt = logging.Formatter()
hndl = logging.StreamHandler()

hndl.setFormatter(frmt)
log.addHandler(hndl)

class Test(unittest.TestCase):

    def setUp(self):
        self.dev = DalsaCobraDevice()
        #self.log_capture = LogCapture()
        #self.log_name = "linegrab.devices"

    #def tearDown(self):
        #self.log_capture.uninstall()

    #def test_log_captures(self):
        ## verification of log matching functionality
        #from logging import getLogger
        #getLogger().info('a message')
        #self.log_capture.check(('root', 'INFO', 'a message'))

    #def test_module_logging(self):
        #self.assertTrue(self.dev.setup_pipe())
#
        #gr = self.log_name
        #self.log_capture.check(
            ##(gr, "INFO", "Setup pipe device"),
            #)

    def test_pipe_cycle(self):
        self.assertTrue(self.dev.setup_pipe())

        result, data = self.dev.grab_pipe()
        self.assertTrue(result)
        self.assertEqual(len(data), 1024)

        self.assertTrue(self.dev.close_pipe())

if __name__ == "__main__":
    unittest.main()

