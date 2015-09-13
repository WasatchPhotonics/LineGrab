""" test just the layout of the visualize interface
"""

import os
import unittest

from PyQt4 import QtGui, QtTest, QtCore

from guiqwt import plot

from linegrab import visualize
from linegrab import utils
from linegrab import controller

from linegrab import LineGrab

app = QtGui.QApplication([])


class ArgsSimulation(object):
    """ Simulation of parser args in LineGrab.
    """
    def __init__(self):
        self.testing = True 
        self.source = "simulation"

class TestLineGrabScript(unittest.TestCase):

    def setUp(self):
        self.log_filename = "LineGrab_log.txt"

    def tearDown(self):
        # This cleans up old windows from rapid tests
        app.closeAllWindows()

    def test_log_file_created_auto_close(self):
        # To use this test, make sure --nologcapture is on
        return
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
        

class TestController(unittest.TestCase):

    def setUp(self):
        self.form = controller.CurveImage()
        # Application level positions of the various widgets. See the test cases
        # below for why this is necessary
        self.continue_pos = QtCore.QPoint(33, 28)
        self.pause_pos = QtCore.QPoint(88, 28)
        self.select_pos = QtCore.QPoint(152, 28)
        self.zoom_pos = QtCore.QPoint(200, 28)
        self.extent_pos = QtCore.QPoint(257, 28)
        self.reset_pos = QtCore.QPoint(305, 28)

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
        child = self.form.childAt(self.zoom_pos)
        QtTest.QTest.mouseClick(child, QtCore.Qt.LeftButton)
        self.assertFalse(self.form.auto_scale)

        # Click reset tool, make sure auto scale is on
        child = self.form.childAt(self.reset_pos)
        QtTest.QTest.mouseClick(child, QtCore.Qt.LeftButton)
        self.assertTrue(self.form.auto_scale)
   
        # Click the full extent graph, verify auto scale is off and the
        # range is 12 bit
        child = self.form.childAt(self.extent_pos)
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
        child = self.form.childAt(self.continue_pos)
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
        child = self.form.childAt(self.pause_pos)
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
        child = self.form.childAt(self.pause_pos)
        QtTest.QTest.mouseClick(child, QtCore.Qt.LeftButton)
        QtTest.QTest.qWait(200)
        post_count = self.form.curve_render
        self.assertEqual(end_count, post_count)

        # Click the live button, wait another 5ms. Make sure the data is
        # not exactly the same, and that the curve render count has gone
        # up
        child = self.form.childAt(self.continue_pos)
        QtTest.QTest.mouseClick(child, QtCore.Qt.LeftButton)
        QtTest.QTest.qWait(200)

        live_first = local_curve.get_data()[1][0]
        live_last = local_curve.get_data()[1][-1]
        live_count = self.form.curve_render

        self.assertGreater(live_count, end_count)
        self.assertNotEqual(end_first, live_first)
        self.assertNotEqual(end_last, live_last)

class TestFPS(unittest.TestCase):
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


class TestVisualize(unittest.TestCase):

    def tearDown(self):
        app.closeAllWindows()
        
    def test_line_and_image(self):
        # Verify that the line graph and image graph are available and
        # have useful dimensions
        main_curve_dialog = visualize.CleanCurveDialog() 
        main_image_dialog = visualize.CleanImageDialog() 

        curve_x = main_curve_dialog.width()
        curve_y = main_curve_dialog.height()
        self.assertEqual(curve_x, 640) 
        self.assertEqual(curve_y, 480)

        image_x = main_image_dialog.width()
        image_y = main_image_dialog.height()
        self.assertEqual(image_x, 640)
        self.assertEqual(image_y, 480)

    def test_tool_signals(self):
        # With a dark graphs main window, connect to the select tool and
        # zoom tool signals. Call their click function, and make sure
        # the result is as expected
        my_form = QtGui.QMainWindow()

        main_curve_dialog = visualize.CleanCurveDialog() 
        manager = plot.PlotManager(my_form)
        manager.add_plot(main_curve_dialog.get_plot())

        curve_toolbar = my_form.addToolBar("Testtools")
        manager.add_toolbar(curve_toolbar, id(curve_toolbar))

        # If you do this, you get all of the other tools
        #manager.register_all_curve_tools()

        # Add the custom tool classes with wrapper signals
        select_tool = manager.add_tool(visualize.SelectSignalTool)
        zoom_tool = manager.add_tool(visualize.ZoomSignalTool)

        select_tool.wrap_sig.clicked.connect(self.process_select)
        select_tool.tool_clicked()
        self.assertEqual(self.select_result, "False")

        zoom_tool.wrap_sig.clicked.connect(self.process_zoom)
        zoom_tool.tool_clicked()
        self.assertEqual(self.zoom_result, "False")
    
    def process_zoom(self, event):
        print "zoom signal is: %s" % event
        self.zoom_result = event
    
    def process_select(self, event):
        print "select signal is: %s" % event
        self.select_result = event

if __name__ == "__main__":
    unittest.main()
