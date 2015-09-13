""" test_LineGrab.py tests the interface as run by the user
"""

import os
import unittest

from scripts import LineGrab

from PyQt4 import QtGui

app = QtGui.QApplication([])

class Test(unittest.TestCase):

    def setUp(self):
        self.log_filename = "LineGrab_log.txt"

    def tearDown(self):
        # This cleans up old windows from rapid tests
        app.closeAllWindows()

    def test_log_file_created_auto_close(self):
        self.assertTrue(os.path.isfile(self.log_filename))
        orig_size = os.path.getsize(self.log_filename)

        result = LineGrab.main(["unittest exec", "-t"])

        new_size = os.path.getsize(self.log_filename)
        self.assertGreater(new_size, orig_size)

    def test_parser(self):
        # Accept two options: testing, which causes the form to close
        # itself which should only be used with the unittest as the
        # controller. source is the data source the application should
        # use
        lgapp = LineGrab.LineGrabApplication()  

        # Fail on no arguments
        with self.assertRaises(TypeError):
            lgapp.parse_args()

        # Fail with just -t
        with self.assertRaises(SystemExit):
            lgapp.parse_args(["-t"])
            
        # Fail with -s but non valid source 
        with self.assertRaises(SystemExit):
            lgapp.parse_args(["-t", "-s", "invalid"])
 
        args = lgapp.parse_args(["-s", "simulation", "-t"])
        self.assertEqual(args.source, "simulation")
        self.assertTrue(args.testing)

    def test_main_options(self):
        # Test with no main options
        result = LineGrab.main(argv=None)
        self.assertEquals(2, result)

        # Verify that main run with the testing option auto-closes the
        # application
        result = LineGrab.main(["unittest", 
                                "-s", "simulation", "-t"])
        self.assertEquals(0, result)
        
if __name__ == "__main__":
    unittest.main()
