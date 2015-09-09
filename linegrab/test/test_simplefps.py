""" tests for the fps computation object.
"""

import sys
import unittest

from PyQt4 import QtGui, QtTest

from linegrab import utils

app = QtGui.QApplication(sys.argv)

class Test(unittest.TestCase):
    
    def setUp(self):
        # Create a barebones widget app to go with the qapplication for
        # testing
        form = QtGui.QWidget()
        form.show()
       
    def tearDown(self):
        app.closeAllWindows() 
 
    def test_fps_creation(self):
        # Create the object
        fps = utils.SimpleFPS()

        # Verify current rate is -1
        self.assertEqual(fps.rate(), -1)

        # Let the app run for one second, verify it's still -1
        QtTest.QTest.qWait(1000) 
        self.assertEqual(fps.rate(), 0)

    def test_fps_updates(self):
        # Create the object
        fps = utils.SimpleFPS()

        # Send it some ticks
        for i in range(10):
            fps.tick()

        # verify they match the expected count after a delay
        QtTest.QTest.qWait(500) 
        self.assertEqual(fps.rate(), 10)

        # Wait another second, verify that the rate drops to zero
        QtTest.QTest.qWait(1000) 
        self.assertEqual(fps.rate(), 0)

if __name__ == "__main__":
    unittest.main()
