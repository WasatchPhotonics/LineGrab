""" helper widgets for visualizing line spectra data.
"""

from PyQt4 import QtGui

from guiqwt import plot
from guiqwt import styles
from guiqwt import curve
from guiqwt import builder

from boardtester import visualize as broastervis

class DualGraphs(QtGui.QWidget):
    """ A Qt mainwindow that has a curve plot and image plot wrapper as
    defined in the broaster.
    """

    def __init__(self):
        super(DualGraphs, self).__init__()
        self.setupUI()
        self.show()

    def setupUI(self):
    
        self.MainGraph = broastervis.SimpleLineGraph()

        self.MainImage = broastervis.SimpleHeatMap()

        #self.MainGraph = plot.CurveDialog(toolbar=True,
            #edit=True, wintitle="Main Dialog")
#
        #self.plot = self.MainGraph.get_plot()
        #
        #self.chart_param = styles.CurveParam()
        #self.chart_param.label = "Data"
        #self.chart_param.line.color = "Blue"
    
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
        x_axis = range(len(data_list))
        self.curve = curve.CurveItem(self.chart_param)
        self.curve.set_data(x_axis, data_list)
        self.plot.add_item(self.curve)
        self.plot.do_autoscale()
        return True
