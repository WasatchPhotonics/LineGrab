""" test just the layout of the visualize interface
"""

import numpy
import unittest

from PyQt4 import QtGui, QtTest

from linegrab import visualize

app = QtGui.QApplication([])

class Test(unittest.TestCase):

    def setUp(self):
        self.form = visualize.DualGraphs()

    def tearDown(self):
        app.closeAllWindows()
        
    def test_line_and_image(self):
        # Verify that the line graph and image graph are available and
        # have useful dimensions
        curve_x = self.form.MainGraph.x()
        curve_y = self.form.MainGraph.y()
        self.assertEqual(curve_x, 11)
        self.assertEqual(curve_y, 11)

        image_x = self.form.MainImage.x()
        image_y = self.form.MainImage.y()
        self.assertEqual(image_x, 11)
        self.assertEqual(image_y, 303)

        curve_data = numpy.linspace(0, 1000, 1024)
        self.form.MainGraph.render_gaps(curve_data)

        img_data = range(200)

        position = 0
        for item in img_data:
            img_data[position] = numpy.linspace(50, 0, 1024)
            position += 1

        data = numpy.array(img_data).astype(float)

        self.form.MainImage.render_image(data)
        


if __name__ == "__main__":
    unittest.main()
