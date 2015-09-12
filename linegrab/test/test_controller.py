""" Tests for LGController gui
"""

import time
import unittest

from PyQt4 import QtGui, QtTest, QtCore

from linegrab import controller

       
# Create one reusable instance of the QApplication. You will see all
# sorts of various hangs and segfaults if you put this in setUp or in a
# class setup method. The idea to split it out of the test setup was 
#from: http://snorf.net/blog/2014/01/04/\
#    writing-unit-tests-for-qgis-python-plugins/
app = QtGui.QApplication([])

class ArgsSimulation(object):
    """ Simulation of parser args in LGController.
    """
    def __init__(self):
        self.testing = True 

class Test(unittest.TestCase):

    def setUp(self):
        self.form = controller.CurveImage()

    def tearDown(self):
        # This cleans up old windows from rapid tests
        app.closeAllWindows()

    def test_auto_close(self):
        # Display the form

        # Set the application parameters 
        args = ArgsSimulation()
        self.form.set_parameters(args)

        # Wait 2 seconds, make sure application is closed
        QtTest.QTest.qWait(2000)
        self.assertFalse(self.form.isVisible())

if __name__ == "__main__":
    unittest.main()
