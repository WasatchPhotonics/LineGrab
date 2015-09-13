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

from linegrab import utils

log = logging.getLogger(__name__)

class CleanImageDialog(plot.ImageDialog):
    """ An guiqwt imagedialog with the grid removed, base data
    visualized, colormap applied, and stylesheet applied.
    """

    def __init__(self):
        super(CleanImageDialog, self).__init__(toolbar=False, edit=True)

        # If you delete the grid item this way, apparently you can't get
        # it back even though the imagedialog makes it available
        grid_item = self.get_plot().get_items()[0]
        self.get_plot().del_item(grid_item)

        self.create_image()

        # Don't show the right side colormap axis
        local_plot = self.get_plot()
        local_plot.enableAxis(local_plot.colormap_axis, False)

        # Note that this disagrees with the documentation
        local_plot.set_axis_direction("left", False)

        # Load an apply this widget's style sheets. Make sure the
        # application wide stylesheet is loaded first
        self.chart_style = utils.load_style_sheet("linegrab_custom.css")
        self.setStyleSheet(self.chart_style)


    def create_image(self):
        """ Create a 2D test pattern image, apply it to the view area.
        """
        base_data = range(50)

        position = 0
        while position < len(base_data):
            base_data[position] = numpy.linspace(0, 100, 1024)
            position += 1

        new_data = numpy.array(base_data).astype(float)

        bmi = builder.make.image
        self.image = bmi(new_data, colormap="gist_earth")
        local_plot = self.get_plot()
        local_plot.add_item(self.image)
        local_plot.do_autoscale()

    def install_button_layout(self):
        """ Do not show the ok, cancel buttons, yet retain the right
        click editing capabilities.
        """
        pass

class CleanCurveDialog(plot.CurveDialog):
    """ A curve dialog with no ok/cancel buttons and the grid item
    not displayed by default.
    """

    def __init__(self):
        super(CleanCurveDialog, self).__init__(edit=True)
        log.debug("new graph")

        # Don't show the grid by deleting it. Apparently you can't get
        # it back after deleting it
        grid_item = self.get_plot().get_items()[0]
        self.get_plot().del_item(grid_item)

        # Initial chart parameters for this graph
        self.chart_param = styles.CurveParam()
        self.chart_param.label = "Data"
        self.chart_param.line.color = "#00cc00"

        # Create a default line profile
        self.create_curve()

        # Load an apply this widget's style sheets. Make sure the
        # application wide stylesheet is loaded first
        self.chart_style = utils.load_style_sheet("linegrab_custom.css")
        self.setStyleSheet(self.chart_style)


    def create_curve(self):
        """ Create a placeholder curve, add it to the current plot.
        """
        data_list = range(1024)
        x_axis = range(len(data_list))
        self.curve = curve.CurveItem(self.chart_param)
        self.curve.set_data(x_axis, data_list)

        local_plot = self.get_plot()
        local_plot.add_item(self.curve)
        return True

    def install_button_layout(self):
        """ Do not show the ok, cancel buttons, yet retain the right
        click editing capabilities.
        """
        pass


class SignalObject(QtCore.QObject):
    """ Simple wrapper of a qobject to be used in custom signal tools
    for emitting a string describing state.
    """
    clicked = QtCore.pyqtSignal(QtCore.QString)


class SelectSignalTool(tools.SelectTool):
    """ Add signals to the toolklass object for application wide usage
    as well as the plot context.
    """

    def __init__(self, *args, **kwargs):
        super(SelectSignalTool, self).__init__(*args, **kwargs)

        self.wrap_sig = SignalObject()

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

    def tool_clicked(self):
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
        self.wrap_sig = SignalObject()

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

    def tool_clicked(self):
        """ Convenience signal wrapper to emit the boolean of the action
        checked status.
        """
        status = self.action.isChecked()
        self.wrap_sig.clicked.emit("%s" % status)

