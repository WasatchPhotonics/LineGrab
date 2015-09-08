""" helper widgets for visualizing line spectra data.
"""

import numpy
import logging

from PyQt4 import QtGui, QtCore

from guiqwt import plot
from guiqwt import styles
from guiqwt import curve
from guiqwt import builder
from guiqwt import tools


log = logging.getLogger(__name__)

class CleanImageDialog(plot.ImageDialog):
    """ An guiqwt imagedialog with the grid removed, base data
    visualized, colormap applied, and stylesheet applied.
    """
    def __init__(self):
        #options = {"lock_aspect_ratio": False}
        options = {"lock_aspect_ratio": True}

        super(CleanImageDialog, self).__init__(toolbar=False, edit=True,
                                               options=options)
        grid_item = self.get_plot().get_items()[0]
        self.get_plot().del_item(grid_item)
       
        self.create_image()

        # Don't show the right side colormap axis
        local_plot = self.get_plot()
        local_plot.enableAxis(local_plot.colormap_axis, False)
      
        # Note that this disagrees with the documentation 
        local_plot.set_axis_direction("left", False)

        self.chart_style = self.load_style_sheet("linegrab_custom.css")
        self.setStyleSheet(self.chart_style)


    def create_image(self):
        """ Create a 2D test pattern image, apply it to the view area.
        """ 
        base_data = range(50)

        position = 0
        for item in base_data:
            base_data[position] = numpy.linspace(0, 100, 1024)
            position += 1

        new_data = numpy.array(base_data).astype(float)

        bmi = builder.make.image
        self.image = bmi(new_data, colormap="gist_earth")
        local_plot = self.get_plot()
        local_plot.add_item(self.image)
        local_plot.do_autoscale()
        
        
       
    def load_style_sheet(self, filename):
        """ Load the qss stylesheet into a string suitable for passing
        to the main widget.
        """
        qss_file = open("linegrab/ui/%s" % filename)
        temp_string = ""
        for line in qss_file.readlines():
            temp_string += line
           
        return temp_string



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
        self.chart_param.line.color = "#00cc00"

        # Load an apply this widget's style sheets. Make sure the
        # application wide stylesheet is loaded first

        # Create a default line profile
        self.create_curve()
        self.chart_style = self.load_style_sheet("linegrab_custom.css")
        self.setStyleSheet(self.chart_style)


    def create_curve(self):
        """ Create a placeholder curve, add it to the current plot.
        """
        data_list = range(1024)
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
       
    def load_style_sheet(self, filename):
        """ Load the qss stylesheet into a string suitable for passing
        to the main widget.
        """
        qss_file = open("linegrab/ui/%s" % filename)
        temp_string = ""
        for line in qss_file.readlines():
            temp_string += line
           
        return temp_string

class SelectSignalTool(tools.SelectTool):
    """ Add signals to the toolklass object for application wide usage
    as well as the plot context.
    """

    def __init__(self, *args, **kwargs):
        super(SelectSignalTool, self).__init__(*args, **kwargs)

        class signalObject(QtCore.QObject):
            clicked = QtCore.pyqtSignal(QtCore.QString)
        self.wrap_sig = signalObject()
 
    def create_action(self, manager):
        """This is overriden here to add custom icons without calling
        guidata.get_icon
        """
        my_icon = QtGui.QIcon(":/greys/greys/select.svg")

        self.action = manager.create_action(self.TITLE,
                                       icon=my_icon,
                                       tip=self.TIP,
                                       triggered=self.activate)
        self.action.setCheckable(True)
        group = self.manager.get_tool_group("interactive")
        group.addAction(self.action)
        self.action.toggled.connect(self.tool_clicked)
        return self.action

    def tool_clicked(self, action):
        """ Convenience signal wrapper to emit the boolean of the action
        checked status.
        """
        status = self.action.isChecked()
        self.wrap_sig.clicked.emit("%s" % status)


class ZoomSignalTool(tools.RectZoomTool):
    """ Add signals to the toolklass object for application wide usage
    as well as the plot context.
    """

    def __init__(self, *args, **kwargs):
        super(ZoomSignalTool, self).__init__(*args, **kwargs)

        class signalObject(QtCore.QObject):
            clicked = QtCore.pyqtSignal(QtCore.QString)
        self.wrap_sig = signalObject()
 
    def create_action(self, manager):
        """This is overriden here to add custom icons without calling
        guidata.get_icon
        """
        my_icon = QtGui.QIcon(":/greys/greys/zoom.svg")

        action = manager.create_action(self.TITLE,
                                       icon=my_icon,
                                       tip=self.TIP,
                                       triggered=self.activate)
        action.setCheckable(True)
        group = self.manager.get_tool_group("interactive")
        group.addAction(action)
        self.action = action
        self.action.triggered.connect(self.tool_clicked)
        return self.action

    def tool_clicked(self, action):
        """ Convenience signal wrapper to emit the boolean of the action
        checked status.
        """
        status = self.action.isChecked()
        self.wrap_sig.clicked.emit("%s" % status)



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
        self.auto_scale = True

        from linegrab.ui.linegrab_layout import Ui_MainWindow
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setGeometry(450, 350, 1080, 600)

        # Make sure the system wide style sheet is applied before the
        # curve and image widgets style sheets overwrite
        self.setStyleSheet(self.qss_string)
        self.replace_widgets()

        # Align the image with the curve above
        self.MainImageDialog.setContentsMargins(17, 0, 0, 0)

        self.add_manager_and_tools()

        self.show()

    def add_manager_and_tools(self):
        """ Create the required plot manager to give access to the item
        list, graph tools, etc.
        """
        # Create a new plot manager, add plots to the plot manager.
        # There is already a plot manager associated with the
        # curvedialog, just create a new one for simplicity.
        self.curve_plot_manager = plot.PlotManager(self)
        main_curve_plot = self.MainCurveDialog.get_plot()
        self.curve_plot_manager.add_plot(main_curve_plot)

        # Add a panels to the plot manager
        self.item_list = plot.PlotItemList(self)
        self.curve_plot_manager.add_panel(self.item_list)

        # Associate the toolbar with the plot manager, this is created
        # along with the qmainwindow toolbars
        curve_toolbar = self.addToolBar("Curve tools")
        curve_toolbar.setIconSize(QtCore.QSize(36, 36))
        self.curve_plot_manager.add_toolbar(curve_toolbar,
                                            id(curve_toolbar))

        # If you do this, you get all of the other tools
        #self.curve_plot_manager.register_all_curve_tools()

        cpm = self.curve_plot_manager
        self.select_tool = cpm.add_tool(SelectSignalTool)
        self.zoom_tool = cpm.add_tool(ZoomSignalTool)

        # Store a reference for use by the application
        self.curve_toolbar = curve_toolbar

    def load_style_sheet(self, filename):
        """ Load the qss stylesheet into a string suitable for passing
        to the main widget.
        """
        qss_file = open("linegrab/ui/%s" % filename)
        temp_string = ""
        for line in qss_file.readlines():
            temp_string += line
           
        return temp_string

    def replace_widgets(self):
        # From: http://stackoverflow.com/questions/4625102/\
        # how-to-replace-a-widget-with-another-using-qt

        self.MainCurveDialog = CleanCurveDialog()
 
        lcph = self.ui.labelCurvePlaceholder
        vlc = self.ui.verticalLayoutCurve
        vlc.removeWidget(lcph)
        lcph.close()

        vlc.insertWidget(0, self.MainCurveDialog)
        vlc.update()
        

        self.MainImageDialog = CleanImageDialog()

        liph = self.ui.labelImagePlaceholder
        vli = self.ui.verticalLayoutImage
        vli.removeWidget(liph)
        liph.close()
       
        vli.insertWidget(0, self.MainImageDialog)
        vli.update()



