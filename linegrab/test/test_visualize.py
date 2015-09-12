""" test just the layout of the visualize interface
"""

import numpy
import unittest

from PyQt4 import QtGui, QtTest

from linegrab import visualize

app = QtGui.QApplication([])

class Test(unittest.TestCase):

    def setUp(self):
        self.form = visualize.DarkGraphs()

    def tearDown(self):
        app.closeAllWindows()
        
    def test_line_and_image(self):
        # Verify that the line graph and image graph are available and
        # have useful dimensions
        curve_x = self.form.main_curve_dialog.width()
        curve_y = self.form.main_curve_dialog.height()
        self.assertEqual(curve_x, 1080) 
        self.assertEqual(curve_y, 395)

        image_x = self.form.main_image_dialog.width()
        image_y = self.form.main_image_dialog.height()
        self.assertEqual(image_x, 1080)
        self.assertEqual(image_y, 240)

    def test_tool_signals(self):
        # With a dark graphs main window, connect to the select tool and
        # zoom tool signals. Call their click function, and make sure
        # the result is as expected

        st = self.form.select_tool
        st.wrap_sig.clicked.connect(self.process_select)
        st.tool_clicked()
        self.assertEqual(self.select_result, "False")

        zt = self.form.zoom_tool
        zt.wrap_sig.clicked.connect(self.process_zoom)
        zt.tool_clicked()
        self.assertEqual(self.zoom_result, "False")

    
    def process_zoom(self, event):
        print "zoom signal is: %s" % event
        self.zoom_result = event
    
    def process_select(self, event):
        print "select signal is: %s" % event
        self.select_result = event

if __name__ == "__main__":
    unittest.main()
