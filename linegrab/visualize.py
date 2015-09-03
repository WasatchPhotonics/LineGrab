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
        #self.setCentralWidget(self.MainGraph)

        self.setGeometry(100, 100, 800, 600) 

    def render_graph(self, data_list):
        """ With a one dimensional list, create new curve, add it to the
        graph, replot the graph.
        """
        log.debug("Render graph")
        x_axis = range(len(data_list))
        self.curve = curve.CurveItem(self.chart_param)
        self.curve.set_data(x_axis, data_list)
        self.plot.add_item(self.curve)
        self.plot.do_autoscale()
        return True
