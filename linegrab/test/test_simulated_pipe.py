""" simulated pipe device test cases
"""

import unittest

from testfixtures import LogCapture

from linegrab.devices import SimulatedPipeDevice
# don't forget to intercept the logging to test that as well
class Test(unittest.TestCase):
    
    def setUp(self):
        self.dev = SimulatedPipeDevice()
        self.log_capture = LogCapture()
        self.log_name = "linegrab.devices"

    def tearDown(self):
        self.log_capture.uninstall()

    def test_log_captures(self):
        # verification of log matching functionality
        from logging import getLogger
        getLogger().info('a message')
        self.log_capture.check(('root', 'INFO', 'a message'))

    def test_module_logging(self):
        self.assertTrue(self.dev.setup_pipe())

        gr = self.log_name
        self.log_capture.check(
            (gr, "INFO", "Create pipe device"),
            )


    def test_pipe_setup(self):
        self.assertTrue(self.dev.setup_pipe())

if __name__ == "__main__":
    unittest.main()
