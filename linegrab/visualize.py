""" helper widgets for visualizing line spectra data.
"""

import logging

from PyQt4 import QtGui

from guiqwt import plot
from guiqwt import styles
from guiqwt import curve
from guiqwt import builder

from boardtester import visualize as broastervis

log = logging.getLogger(__name__)

class CleanCurveDialog(plot.CurveDialog):
    """ A curve dialog with no ok/cancel buttons and the grid item
    not displayed by default.
    """

    def __init__(self):
        super(CleanCurveDialog, self).__init__(edit=True)

        log.debug("new graph")

        # Don't show the grid by deleting it. Apparently you can't get
        # it back by deleting it
        grid_item = self.get_plot().get_items()[0]
        self.get_plot().del_item(grid_item)

        # Initial chart parameters for this graph
        self.chart_param = styles.CurveParam()
        self.chart_param.label = "Data"
        self.chart_param.line.color = "Green"

        # Load an apply this widget's style sheets. Make sure the
        # application wide stylesheet is loaded first

        # Create a default line profile
        self.create_curve()

    def create_curve(self):
        data_list = range(2048)
        x_axis = range(len(data_list))
        self.curve = curve.CurveItem(self.chart_param)
        self.curve.set_data(x_axis, data_list)

        plot = self.get_plot()
        plot.add_item(self.curve)
        return True

    def install_button_layout(self):
        """ Do not show the ok, cancel buttons, yet retain the right
        click editing capabilities.
        """
        #print "No button layout"
        pass


class DualGraphs(QtGui.QWidget):
    """ A Qt widget with a line plot at the top and an waterfall view of
    the line plot data in the bottom frame. 
    """

    def __init__(self):
        super(DualGraphs, self).__init__()
        log.debug("setup ui")
        self.setupUI()
        self.show()

    def setupUI(self):
    
        #self.MainGraph = broastervis.SimpleLineGraph()
        self.MainGraph = CleanCurveDialog()
        chart_style = self.load_style_sheet("linegrab_custom.css")
        self.MainGraph.setStyleSheet(chart_style)
        

        self.MainImage = broastervis.SimpleHeatMap()

        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(self.MainGraph)
        vbox.addWidget(self.MainImage)
        self.setLayout(vbox)

        self.setGeometry(100, 100, 800, 600) 

    def reuse_image(self, data_list):
        """ Get the current image item (if it exists) from the
        simpleheatmap, change it's data and replot.
        """
        log.debug("reuse image")
       
        try:
            image = self.MainImage.image
            image.set_data(data_list)

        except AttributeError:
            log.info("Assuming image does not exist, creating")
            self.MainImage.render_image(data_list)
        
        #self.MainImage.plot.do_autoscale()
        self.MainImage.plot.replot()
      

    def update_graph(self, data_list):
        """ Get the current line plot from the available line graph, 
        change it's data and replot.
        """
        log.debug("render graph")
        x_axis = range(len(data_list))
            
        self.MainGraph.curve.set_data(x_axis, data_list)
            
        self.MainGraph.get_plot().do_autoscale()
       
    def load_style_sheet(self, filename):
        """ Load the qss stylesheet into a string suitable for passing
        to the main widget.
        """
        qss_file = open("linegrab/ui/%s" % filename)
        temp_string = ""
        for line in qss_file.readlines():
            temp_string += line
           
        return temp_string
