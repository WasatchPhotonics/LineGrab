""" Tests for LineGrab gui
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

        
# Application level positions of the various widgets. See the test cases
# below for why this is necessary
continue_pos = QtCore.QPoint(33, 28)
pause_pos = QtCore.QPoint(88, 28)
select_pos = QtCore.QPoint(152, 28)
zoom_pos = QtCore.QPoint(200, 28)
extent_pos = QtCore.QPoint(257, 28)
reset_pos = QtCore.QPoint(305, 28)

class ArgsSimulation(object):
    """ Simulation of parser args in LineGrab.
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

    def test_graph_buttons(self):
        args = ArgsSimulation()
        self.form.set_parameters(args)
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

        # Click zoom icon, make sure auto scale turns off
        child = self.form.childAt(zoom_pos)
        QtTest.QTest.mouseClick(child, QtCore.Qt.LeftButton)
        self.assertFalse(self.form.auto_scale)

        # Click reset tool, make sure auto scale is on
        child = self.form.childAt(reset_pos)
        QtTest.QTest.mouseClick(child, QtCore.Qt.LeftButton)
        self.assertTrue(self.form.auto_scale)
   
        # Click the full extent graph, verify auto scale is off and the
        # range is 12 bit
        child = self.form.childAt(extent_pos)
        QtTest.QTest.mouseClick(child, QtCore.Qt.LeftButton)
        self.assertFalse(self.form.auto_scale)

        local_plot = self.form.main_curve_dialog.get_plot()
        self.assertEqual(local_plot.get_axis_limits(0)[0], 0)
        self.assertEqual(local_plot.get_axis_limits(0)[1], 4096)
        
    def test_live_button(self):
        args = ArgsSimulation()
        self.form.set_parameters(args)
        QtTest.QTest.qWait(100)
        local_curve = self.form.main_curve_dialog.curve

        # Click live again, make sure it stays in live mode
        pre_count = self.form.curve_render
        child = self.form.childAt(continue_pos)
        QtTest.QTest.mouseClick(child, QtCore.Qt.LeftButton)
        QtTest.QTest.qWait(100)
        post_count = self.form.curve_render
        self.assertGreater(post_count, pre_count)
        
        

    def test_pause_button(self):
        args = ArgsSimulation()
        self.form.set_parameters(args)
        QtTest.QTest.qWait(100)
        local_curve = self.form.main_curve_dialog.curve

        # Click the pause button, get the data from the chart
        child = self.form.childAt(pause_pos)
        QtTest.QTest.mouseClick(child, QtCore.Qt.LeftButton)

        begin_first = local_curve.get_data()[1][0]
        begin_last = local_curve.get_data()[1][-1]
        begin_count = self.form.curve_render


        # Wait 500 ms, make sure the total render variable has not
        # increased and the data is exactly the same
        QtTest.QTest.qWait(200)

        end_first = local_curve.get_data()[1][0]
        end_last = local_curve.get_data()[1][-1]
        end_count = self.form.curve_render

        self.assertEqual(begin_count, end_count)
        self.assertEqual(begin_first, end_first)
        self.assertEqual(begin_last, end_last)

        # Click the pause button again, make sure it stays in pause mode
        child = self.form.childAt(pause_pos)
        QtTest.QTest.mouseClick(child, QtCore.Qt.LeftButton)
        QtTest.QTest.qWait(200)
        post_count = self.form.curve_render
        self.assertEqual(end_count, post_count)

        # Click the live button, wait another 5ms. Make sure the data is
        # not exactly the same, and that the curve render count has gone
        # up
        child = self.form.childAt(continue_pos)
        QtTest.QTest.mouseClick(child, QtCore.Qt.LeftButton)
        QtTest.QTest.qWait(200)

        live_first = local_curve.get_data()[1][0]
        live_last = local_curve.get_data()[1][-1]
        live_count = self.form.curve_render

        self.assertGreater(live_count, end_count)
        self.assertNotEqual(end_first, live_first)
        self.assertNotEqual(end_last, live_last)

if __name__ == "__main__":
    unittest.main()
