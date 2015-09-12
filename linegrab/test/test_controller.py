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

        # 200, 28 of the main form window, because inheriting from the
        # rectzoomtool apparently disguises the widgetness from the
        # qttest mouseclick. Can you fix this with a proxy widget?
        zoom_pos = QtCore.QPoint(200, 28)
        #QtTest.QTest.mouseClick(self.form, QtCore.Qt.LeftButton, pos=zoom_pos, delay=1)

        # Try find child at - won't that just return the same
        # rectzoomtool which does not respond to the click interface?
        child = self.form.childAt(zoom_pos)
        print "The child is: %s" % child
        QtTest.QTest.mouseClick(child, QtCore.Qt.LeftButton, delay=1)

        # Make sure auto scale is off
        QtTest.QTest.qWait(500)
        self.assertFalse(self.form.auto_scale)
        

if __name__ == "__main__":
    unittest.main()
