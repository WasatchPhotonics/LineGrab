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


class DarkGraphs(QtGui.QMainWindow):
    """ Import the generated py file from the qt-designer created .ui
    file. Apply the system-wide style sheet. Integrate with actual
    guiqwt curve and image controls.
    """

    def __init__(self):
        super(DarkGraphs, self).__init__()

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
        #self.MainCurveWidget.setStyleSheet(self.green_on_black)
        self.setStyleSheet(self.qss_string)

        self.chart_style = self.load_style_sheet("linegrab_custom.css")
        self.MainCurveWidget.setStyleSheet(self.chart_style)
        #self.mainImageDialog.setStyleSheet(self.chart_style)

        # Image left, top, right, bottom
        #self.mainImageDialog.setContentsMargins(10, 0, 0, 0)

        #new_plot = self.MainCurveWidget.get_plot()
        #new_plot.set_axis_color(3, "Blue")

        self.show()


        self.setup_chart()
        #self.dev = devices.SimulatedPipeDevice(pattern_jump=50, 1000)
        #self.dev = devices.SimulatedPipeDevice(pattern_jump=100,
                                               #top_level=4096)
       
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
      

        #self.MainCurveWidget = plot.CurveWidget(gridparam=mygrid)

        #self.MainCurveWidget = plot.CurveDialog(toolbar=False, edit=True)
        self.MainCurveWidget = CleanCurveDialog()
 
        lcph = self.ui.labelCurvePlaceholder
        vlc = self.ui.verticalLayoutCurve
        vlc.removeWidget(lcph)
        lcph.close()

        vlc.insertWidget(0, self.MainCurveWidget)
        vlc.update()
        #print "What is the curve: %r" % self.MainCurveWidget
        


        #liph = self.ui.labelImagePlaceholder
        #vli = self.ui.verticalLayoutImage
        #vli.removeWidget(liph)
        #liph.close()
        
        #vli.insertWidget(0, self.mainImageDialog)
        #vli.update()



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
    
        self.MainGraph = CleanCurveDialog()
        chart_style = self.load_style_sheet("linegrab_custom.css")
        self.MainGraph.setStyleSheet(chart_style)
        

        self.MainImage = broastervis.SimpleHeatMap()

        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(self.MainGraph)
        vbox.addWidget(self.MainImage)
        self.setLayout(vbox)

        self.setGeometry(100, 100, 800, 600) 

       
    def load_style_sheet(self, filename):
        """ Load the qss stylesheet into a string suitable for passing
        to the main widget.
        """
        qss_file = open("linegrab/ui/%s" % filename)
        temp_string = ""
        for line in qss_file.readlines():
            temp_string += line
           
        return temp_string
