""" tests for a wasatch photonics cobra over dalsa card.
"""

import unittest
import logging

from linegrab.devices import DalsaBaslerDevice

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger()

class Test(unittest.TestCase):

    def setUp(self):
        self.dev = DalsaBaslerDevice()

    def test_pipe_cycle(self):
        self.assertTrue(self.dev.setup_pipe())

        result, data = self.dev.grab_pipe()
        self.assertTrue(result)
        self.assertEqual(len(data), 2048)

        self.assertTrue(self.dev.close_pipe())

if __name__ == "__main__":
    unittest.main()

