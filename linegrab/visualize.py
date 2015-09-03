""" helper widgets for visualizing line spectra data.
"""

import logging

from PyQt4 import QtGui

from boardtester import visualize as broastervis

log = logging.getLogger(__name__)

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
    
        self.MainGraph = broastervis.SimpleLineGraph()
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
