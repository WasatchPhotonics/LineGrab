""" helper widgets for visualizing line spectra data.
"""

import logging

from PyQt4 import QtGui

from boardtester import visualize as broastervis

log = logging.getLogger(__name__)

class CleanCurveDialog(plot.CurveDialog):
    def __init__(self):
        """ A curve dialog with no ok/cancel buttons and the grid item
        not displayed by default.
        """
        super(CleanCurveDialog, self).__init__(edit=True)

        # Don't show the grid by deleting it. Apparently you can't get
        # it back by deleting it
        grid_item = self.get_plot().get_items()[0]
        self.get_plot().del_item(grid_item)

    def install_button_layout(self):
        """ Do not show the ok, cancel buttons, yet retain the right
        click editing capabilities.
        """
        #print "No button layout"
        pass


class DualGraphs(QtGui.QWidget):
    """ A Qt mainwindow that has a curve plot and image plot wrapper as
    defined in the broaster.
    """

    def __init__(self):
        super(DualGraphs, self).__init__()
        log.debug("setup ui")
        self.setupUI()
        self.show()

    def setupUI(self):
    
        #self.MainGraph = broastervis.SimpleLineGraph()
        self.MainGraph = CleanCurveDialog()
        self.MainImage = broastervis.SimpleHeatMap()

        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(self.MainGraph)
        vbox.addWidget(self.MainImage)
        self.setLayout(vbox)

        self.setGeometry(100, 100, 800, 600) 

    def reuse_graph(self, data_list):
        """ Get the current line plot from the simplelinegraph, change
        it's data and replot.
        """
        log.debug("Reuse graph")
        x_axis = range(len(data_list))
        try:
            curve = self.MainGraph.curve
            curve.set_data(x_axis, data_list)

        except AttributeError:
            log.info("Assuming graph does not exist, creating")
            self.MainGraph.render_graph(data_list) 
            
        self.MainGraph.plot.do_autoscale()

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
