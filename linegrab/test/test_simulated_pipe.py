""" simulated pipe device test cases
"""

import unittest

from linegrab.devices import SimulatedPipeDevice
# don't forget to intercept the logging to test that as well
class Test(unittest.TestCase):
    
    def setUp(self):
        self.dev = SimulatedPipeDevice()

    def test_pipe_setup(self):
        self.assertTrue(self.dev.setup_pipe())

if __name__ == "__main__":
    unittest.main()
