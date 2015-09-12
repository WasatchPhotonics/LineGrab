""" test_LGController.py tests the interface as run by the user
"""

import os
import unittest

from scripts import LGController

from PyQt4 import QtGui

app = QtGui.QApplication([])

class Test(unittest.TestCase):

    def setUp(self):
        self.log_filename = "LineGrab_log.txt"
        pass

    def tearDown(self):
        print "DO you need close all windows?"

    def test_log_file_created_auto_close(self):
        self.assertTrue(os.path.isfile(self.log_filename))
        orig_size = os.path.getsize(self.log_filename)

        result = LGController.main(["unittest exec", "-t"])

        new_size = os.path.getsize(self.log_filename)
        self.assertGreater(new_size, orig_size)

    def test_parser(self):
        # Accept two options: testing, which causes the form to close
        # itself which should only be used with the unittest as the
        # controller. source is the data source the application should
        # use
        lgapp = LGController.LineGrabApplication()  

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
        # Verify that main run with the testing option auto-closes the
        # application
        # Run without testing mode initially for test build out
        result = LGController.main(["unittest", "-s", "simulation"])

        #result = LGController.main(["unittest", "-s", "-t"])
        self.assertEquals(0, result)
        
if __name__ == "__main__":
    unittest.main()
