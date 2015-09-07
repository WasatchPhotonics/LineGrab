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

class CleanImageDialog(plot.ImageDialog):
    def __init__(self):
        super(CleanImageDialog, self).__init__(toolbar=False, edit=True)
        grid_item = self.get_plot().get_items()[0]
        self.get_plot().del_item(grid_item)
        
        #for item in self.get_plot().get_scales():
            #print "scale: %r " % item

        plot = self.get_plot()
        base_data = range(50)

        position = 0
        for item in base_data:
            base_data[position] = numpy.linspace(0, 100, 1024)
            position += 1

        new_data = numpy.array(base_data).astype(float)

        bmi = builder.make.image
        image = bmi(new_data, colormap="bone")
        plot.add_item(image)
        plot.do_autoscale()
        
        #for item in plot.get_items():
            #print "Plot items: %s" % item

        #print "colormap axis: %s" % plot.colormap_axis
        plot.enableAxis(plot.colormap_axis, False)
        #for item in plot.get_active_axes():
            #print "axes: %s " % item
            #print "class: %s " % plot.get_axesparam_class(item)
            #print "direction : %s " % plot.get_axis_direction(item)
            #print "title: %s " % plot.get_axis_title(item)
            #print "unit: %s " % plot.get_axis_unit(item)
      
        # Note that this disagrees with the documentation 
        self.get_plot().set_axis_direction("left", False)

class CleanCurveDialog(plot.CurveDialog):
    def __init__(self):
        super(CleanCurveDialog, self).__init__(edit=True)

        # now that the curvedialog has been created, get the list of
        # items from the curveplot, which should only have a grid at
        # this point. Dont' show the grid. Can't get it back if you just
        # delete it...
        grid_item = self.get_plot().get_items()[0]
        self.get_plot().del_item(grid_item)

    def install_button_layout(self):
        """ Do not show the ok, cancel buttons, yet retain the right
        click editing capabilities.
        """
        #print "No button layout"
        pass

class DarkTestApplication(QtGui.QMainWindow):
    """ Import the generated py file from the qt-designer created .ui
    file. Apply the system-wide style sheet. Integrate with actual
    guiqwt curve and image controls.
    """

    def __init__(self):
        super(DarkTestApplication, self).__init__()

        self.qss_string = self.load_style_sheet("qdarkstyle.css")
        self.image_height = 50
        self.image_data = []

        from linegrab.ui.linegrab_layout import Ui_MainWindow
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.insert_curves()
        self.setGeometry(450, 350, 1080, 600)

        #self.green_on_black = "background-color: rgba(0,0,0,255);\n" + \
                              #"color: rgba(0,255,0,255);"
        #self.mainCurveWidget.setStyleSheet(self.green_on_black)
        self.setStyleSheet(self.qss_string)

        self.chart_style = self.load_style_sheet("linegrab_custom.css")
        self.mainCurveWidget.setStyleSheet(self.chart_style)
        self.mainImageDialog.setStyleSheet(self.chart_style)

        # Image left, top, right, bottom
        self.mainImageDialog.setContentsMargins(10, 0, 0, 0)

        new_plot = self.mainCurveWidget.get_plot()
        new_plot.set_axis_color(3, "Blue")

        self.show()


        self.setup_chart()
        #self.dev = devices.SimulatedPipeDevice(pattern_jump=50, 1000)
        #self.dev = devices.SimulatedPipeDevice(pattern_jump=100,
                                               #top_level=4096)

        self.dev = devices.SimulatedSpectraDevice()
        result = self.dev.setup_pipe()
        self.dataTimer = QtCore.QTimer()
        self.dataTimer.timeout.connect(self.dark_update)
        self.dataTimer.start(300)
       
    def load_style_sheet(self, filename):
        """ Load the qss stylesheet into a string suitable for passing
        to the main widget.
        """
        qss_file = open("linegrab/ui/%s" % filename)
        temp_string = ""
        for line in qss_file.readlines():
            temp_string += line
           
        return temp_string

    def setup_chart(self):
        self.chart_param = styles.CurveParam()
        self.chart_param.label = "Data"
        self.chart_param.line.color = "Green"

    def insert_curves(self):
        # From: http://stackoverflow.com/questions/4625102/\
        # how-to-replace-a-widget-with-another-using-qt
      

        #self.mainCurveWidget = plot.CurveWidget(gridparam=mygrid)

        #self.mainCurveWidget = plot.CurveDialog(toolbar=False, edit=True)
        self.mainCurveWidget = CleanCurveDialog()
 
        lcph = self.ui.labelCurvePlaceholder
        vlc = self.ui.verticalLayoutCurve
        vlc.removeWidget(lcph)
        lcph.close()

        vlc.insertWidget(0, self.mainCurveWidget)
        vlc.update()
        #print "What is the curve: %r" % self.mainCurveWidget
        


        #self.mainImageDialog = plot.ImageDialog(toolbar=False,
            #wintitle="Image dialog")
        self.mainImageDialog = CleanImageDialog()

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
        self.dark_update_image(data)
        self.dataTimer.start(0)

    def reuse_graph(self, data_list):
        log.debug("Reuse graph")
        x_axis = range(len(data_list))
        try:
            self.curve.set_data(x_axis, data_list)

        except AttributeError:
            log.info("Assuming graph does not exist, creating")
            self.render_graph(data_list) 
            
        plot = self.mainCurveWidget.get_plot()
        plot.do_autoscale()

    def render_graph(self, data_list):
        x_axis = range(len(data_list))
        self.curve = curve.CurveItem(self.chart_param)
        self.curve.set_data(x_axis, data_list)

        plot = self.mainCurveWidget.get_plot()
        plot.add_item(self.curve)
        plot.do_autoscale()
        return True
      
    def dark_update_image(self, data):
        self.image_data.append(data)
        if len(self.image_data) > self.image_height:
            self.image_data = self.image_data[1:]

        img_data = range(len(self.image_data))

        position = 0
        for item in img_data:
            img_data[position] = self.image_data[position]
            position += 1

        new_data = numpy.array(img_data).astype(float)

        try:
            image = self.image
            image.set_data(new_data)

        except AttributeError:
            log.info("Assuming image does not exist, creating")
            bmi = builder.make.image
            self.image = bmi(new_data, colormap="bone")
            self.mainImageDialog.get_plot().add_item(self.image)
            self.mainImageDialog.get_plot().do_autoscale()
        
        #self.MainImage.plot.do_autoscale()
        self.mainImageDialog.get_plot().replot()
 
      
def main(argv=None):
    app = QtGui.QApplication(argv)
    darkapp = DarkTestApplication()
    sys.exit(app.exec_())

if __name__ == "__main__":
    sys.exit(main(sys.argv))
