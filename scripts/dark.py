#!/usr/bin/env python
""" testing area for dark themed, application wide style-sheets
"""

import sys
import numpy
import logging
import argparse

from PyQt4 import QtGui, QtCore

from guiqwt import plot
from guiqwt import styles
from guiqwt import curve
from guiqwt import builder


from linegrab import devices

logging.basicConfig(filename="LineGrab_log.txt", filemode="w",
                    level=logging.DEBUG)
log = logging.getLogger()

class DarkTestApplication(QtGui.QMainWindow):
    """ Import the generated py file from the qt-designer created .ui
    file. Apply the system-wide style sheet. Integrate with actual
    guiqwt curve and image controls.
    """

    def __init__(self):
        super(DarkTestApplication, self).__init__()

        self.load_style_sheet()

        from linegrab.ui.linegrab_layout import Ui_MainWindow
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.insert_curves()
        self.setGeometry(450, 350, 1080, 600)

        #self.green_on_black = "background-color: rgba(0,0,0,255);\n" + \
                              #"color: rgba(0,255,0,255);"
        #self.mainCurveDialog.setStyleSheet(self.green_on_black)
        self.setStyleSheet(self.qss_string)

        self.show()


        self.setup_chart()
        self.dev = devices.SimulatedPipeDevice()
        result = self.dev.setup_pipe()
        self.dataTimer = QtCore.QTimer()
        self.dataTimer.timeout.connect(self.dark_update)
        self.dataTimer.start(300)
       
    def load_style_sheet(self, filename="linegrab/ui/linegrab.css"):
        """ Load the qss stylesheet into a string suitable for passing
        to the main widget.
        """
        qss_file = open(filename)
        self.qss_string = ""
        for line in qss_file.readlines():
            self.qss_string += line
        #print "style sheet: %s" % self.qss_string

    def setup_chart(self):
        self.chart_param = styles.CurveParam()
        self.chart_param.label = "Data"
        self.chart_param.line.color = "Blue"

    def insert_curves(self):
        # From: http://stackoverflow.com/questions/4625102/\
        # how-to-replace-a-widget-with-another-using-qt
      
        self.mainCurveDialog = plot.CurveDialog(toolbar=False,
            wintitle="Main Dialog")
 
        lcph = self.ui.labelCurvePlaceholder
        vlc = self.ui.verticalLayoutCurve
        vlc.removeWidget(lcph)
        lcph.close()

        vlc.insertWidget(0, self.mainCurveDialog)
        vlc.update()
        print "What is the curve: %r" % self.mainCurveDialog
        


        self.mainImageDialog = plot.ImageDialog(toolbar=False,
            wintitle="Image dialog")

        liph = self.ui.labelImagePlaceholder
        vli = self.ui.verticalLayoutImage
        vli.removeWidget(liph)
        liph.close()
        
        vli.insertWidget(0, self.mainImageDialog)
        vli.update()

        #spcf = self.build_spectra_frame()
        #self.ui.layout_vertical_curves.removeWidget(self.ui.curve_widget_top)
        #self.ui.curve_widget_top.close()
        #self.ui.curve_widget_top = spcf
        #self.ui.layout_vertical_curves.insertWidget(0, self.ui.curve_widget_top)
        #self.ui.layout_vertical_curves.update()


    def dark_update(self):
        result, data = self.dev.grab_pipe()
        self.reuse_graph(data)
        #self.update_image(data)
        self.dataTimer.start(0)

    def reuse_graph(self, data_list):
        log.debug("Reuse graph")
        x_axis = range(len(data_list))
        try:
            self.curve.set_data(x_axis, data_list)

        except AttributeError:
            log.info("Assuming graph does not exist, creating")
            self.render_graph(data_list) 
            
        plot = self.mainCurveDialog.get_plot()
        plot.do_autoscale()

    def render_graph(self, data_list):
        x_axis = range(len(data_list))
        self.curve = curve.CurveItem(self.chart_param)
        self.curve.set_data(x_axis, data_list)

        plot = self.mainCurveDialog.get_plot()
        plot.add_item(self.curve)
        plot.do_autoscale()
        return True
      
def main(argv=None):
    app = QtGui.QApplication(argv)
    darkapp = DarkTestApplication()
    sys.exit(app.exec_())

if __name__ == "__main__":
    sys.exit(main(sys.argv))
