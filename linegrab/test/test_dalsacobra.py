""" tests for a wasatch photonics cobra over dalsa card.
"""

import unittest

from linegrab.devices import DalsaCobraDevice

class Test(unittest.TestCase):

    def setUp(self):
        self.dev = DalsaCobraDevice()
        #self.log_capture = LogCapture()
        #self.log_name = "linegrab.devices"
        pass

    def tearDown(self):
        pass

    def test_pipe_cycle(self):
        self.assertTrue(self.dev.setup_pipe())

        result, data = self.dev.grab_pipe()
        self.assertTrue(result)
        self.assertEqual(len(data), 1024)

        self.assertTrue(self.dev.close_pipe())

if __name__ == "__main__":
    unittest.main()

