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
        self.source = "simulation"

class Test(unittest.TestCase):

    def setUp(self):
        self.form = controller.CurveImage()

    def tearDown(self):
        # This cleans up old windows from rapid tests
        app.closeAllWindows()

    def test_auto_close(self):
        # Set the application parameters 
        args = ArgsSimulation()
        self.form.set_parameters(args)

        # Wait 2 seconds, make sure application is closed
        QtTest.QTest.qWait(2000)
        self.assertFalse(self.form.isVisible())

    def test_select_zoom_toggle(self):
        args = ArgsSimulation()
        self.form.set_parameters(args)

        # Wait, click the zoom icon
        QtTest.QTest.qWait(100)

        # You'd think you could do: 
        # mouseClick(self.form.zoom_tool, QtCore.QtLeftButton)
        # but that responds with argument in unexpected type
        # ZoomSignalTool. 
        # You'd also think you can specify global application
        # coordinates and click. But that does nothing. No feedback,
        # nothing.
        # http://stackoverflow.com/questions/20394236/\
        #   qtest-mouseclick-on-a-qpushbutton
        # shows that you should use coordinates, look up the child, then
        # the click works.

        # 200, 28 of the main form window location of the zoom tool
        zoom_pos = QtCore.QPoint(200, 28)
        child = self.form.childAt(zoom_pos)
        QtTest.QTest.mouseClick(child, QtCore.Qt.LeftButton, delay=1)

        # Make sure auto scale is off
        QtTest.QTest.qWait(500)
        self.assertFalse(self.form.auto_scale)
        

if __name__ == "__main__":
    unittest.main()
