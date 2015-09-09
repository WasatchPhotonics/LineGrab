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
        curve_x = self.form.MainCurveDialog.width()
        curve_y = self.form.MainCurveDialog.height()
        self.assertEqual(curve_x, 1080) 
        self.assertEqual(curve_y, 395)

        image_x = self.form.MainImageDialog.width()
        image_y = self.form.MainImageDialog.height()
        self.assertEqual(image_x, 1080)
        self.assertEqual(image_y, 240)


if __name__ == "__main__":
    unittest.main()
