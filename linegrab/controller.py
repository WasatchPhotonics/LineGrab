#!/usr/bin/env python
""" controller.py - provide a qtmainwindow and controlling logic for
acquiring data from a variety of cameras.
"""

import numpy
import logging

from PyQt4 import QtGui, QtCore

from guiqwt import plot

from linegrab import visualize
from linegrab import utils

from wasatchcameralink import DALSA
from wasatchcameralink import simulation

log = logging.getLogger(__name__)

class CurveImage(QtGui.QMainWindow):
    """ The main interface for the LineGrab application. Can be created
    from unittest or a main() for full test coverage.
    """
    def __init__(self):
        super(CurveImage, self).__init__()
        log.debug("CurveImage creation")

        from linegrab.ui.linegrab_layout import Ui_MainWindow
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setGeometry(450, 350, 1080, 600)

        # Make sure the system wide style sheet is applied before the
        # curve and image widgets style sheets overwrite
        self.qss_string = utils.load_style_sheet("qdarkstyle.css")
        self.setStyleSheet(self.qss_string)

        self.replace_widgets()

        # Align the image with the curve above it
        self.main_image_dialog.setContentsMargins(17, 0, 0, 0)

        self.add_manager_and_tools()
    
        # Timer to auto-close the application
        self.close_timer = QtCore.QTimer()
        self.close_timer.timeout.connect(self.closeEvent)

        self.set_app_defaults()

        self.show()

    def replace_widgets(self):
        """ From: http://stackoverflow.com/questions/4625102/\
            how-to-replace-a-widget-with-another-using-qt
        Replace the current placeholders from qt designer with the
        custom widgets.
        """

        # Create the widget
        self.main_curve_dialog = visualize.CleanCurveDialog()

        # Remove the placeholder widget from the layout
        lcph = self.ui.labelCurvePlaceholder
        vlc = self.ui.verticalLayoutCurve
        vlc.removeWidget(lcph)
        lcph.close()

        # Add the new widget to the layout
        vlc.insertWidget(0, self.main_curve_dialog)
        vlc.update()


        # Create the widget
        self.main_image_dialog = visualize.CleanImageDialog()

        # Remove the placeholder widget from the layout
        liph = self.ui.labelImagePlaceholder
        vli = self.ui.verticalLayoutImage
        vli.removeWidget(liph)
        liph.close()

        # Add the new widget to the layout
        vli.insertWidget(0, self.main_image_dialog)
        vli.update()

    def add_manager_and_tools(self):
        """ Create the required plot manager to give access to the item
        list, graph tools, etc.
        """
        # Create a new plot manager, add plots to the plot manager.
        # There is already a plot manager associated with the
        # curvedialog, just create a new one for simplicity.
        manager = plot.PlotManager(self)
        manager.add_plot(self.main_curve_dialog.get_plot())

        # Add a panel to the plot manager - this apparently is not
        # required to enable the tool linkage. Was in here based on
        # example code. If you add this back in it creates an invisible
        # widget over at least the 'play' button.
        #manager.add_panel(plot.PlotItemList(self))

        # Associate the toolbar with the plot manager, this is created
        # along with the qmainwindow toolbars
        curve_toolbar = self.addToolBar("Curve tools")
        curve_toolbar.setIconSize(QtCore.QSize(36, 36))
        manager.add_toolbar(curve_toolbar, id(curve_toolbar))

        # If you do this, you get all of the other tools
        #manager.register_all_curve_tools()

        # Add the custom tool classes with wrapper signals
        self.select_tool = manager.add_tool(visualize.SelectSignalTool)
        self.zoom_tool = manager.add_tool(visualize.ZoomSignalTool)

        # Store a reference for use by the application
        self.curve_toolbar = curve_toolbar

    def set_parameters(self, args):
        """ Assign the startup environment parameters for this
        application run. Data source simulation/e2v, etc.
        """
        if args.testing:
            self.delay_close()

        if args.source == "simulation":
            log.info("Create simulated spectra device")
            self.dev = simulation.SimulatedSpectraDevice()
                
        elif args.source == "cobra":
            log.info("Create DALSA cobra device")
            #self.dev = devices.DalsaCobraDevice()
            self.dev = DALSA.Cobra()
                
        elif args.source == "basler":
            log.info("Create DALSA basler device")
            #self.dev = devices.DalsaBaslerDevice()
            self.dev = DALSA.BaslerSprint4K()
            
            
        self.dev.setup_pipe()
        self.setup_pipe_timer()

    def delay_close(self):
        """ For testing purposes, create a qtimer that triggers the
        close event after a delay.
        """
        log.debug("Trigger delay close")
        self.close_timer.start(1000)

    def closeEvent(self, event=None):
        """ Cleanup the application on widget close
        close the pipes, stop all the timers.
        """
        log.debug("Cleanup close")
        log.info("Attempt to close pipe")
        result = self.dev.close_pipe()
        log.info("Close pipe result: %s" % result)
        self.data_timer.stop()
        self.close()


    def create_actions(self):
        """ Runtime generated toolbars to link guiqwt graph controls
        with the mainwindow level toolbars.
        """
        dgct = self.curve_toolbar.addAction

        agfe = dgct(QtGui.QIcon(":/greys/greys/full_extent.svg"),
                    "Full extent graph"
                   )
        self.action_graph_full_extent = agfe

        agr = dgct(QtGui.QIcon(":/greys/greys/reset.svg"),
                   "Reset graph parameters"
                  )
        self.action_graph_reset = agr

        spacer = QtGui.QWidget()
        spacer.setSizePolicy(QtGui.QSizePolicy.Expanding,
                             QtGui.QSizePolicy.Expanding)
        self.curve_toolbar.addWidget(spacer)

        act_name = "Instantaneous performance"
        self.action_fps_display = QtGui.QAction(act_name, self)
        self.curve_toolbar.addAction(self.action_fps_display)

        # Remove the placeholder toolbar
        self.ui.toolBar_GraphControls.setVisible(False)

    def setup_signals(self):
        """ Hook into graph emitted signals for controller level.
        """

        # Hook the play/pause buttons
        self.ui.actionContinue_Live_Updates.triggered.connect(self.on_live)
        self.ui.actionPause_Live_Updates.triggered.connect(self.on_pause)

        # Custom graph buttons
        self.action_graph_reset.triggered.connect(self.reset_graph)
        self.action_graph_full_extent.triggered.connect(self.full_extent)

        # Custom tools generated in visualize that are not actions
        self.zoom_tool.wrap_sig.clicked.connect(self.process_zoom)
        self.select_tool.wrap_sig.clicked.connect(self.process_select)

    def on_live(self, action):
        """ Live and pause buttons are the equivalent of toggle buttons.
        Only one can be enabled at a time.
        """
        log.info("Click live updates")
        if action == False:
            self.ui.actionContinue_Live_Updates.setChecked(True)

        self.ui.actionPause_Live_Updates.setChecked(False)
        self.live_updates = True

    def on_pause(self, action):
        """ Pause and live buttons are the equivalent of toggle buttons.
        Only one can be enabled at a time.
        """
        log.info("Pause live updates: %s", action)
        if action == False:
            self.ui.actionPause_Live_Updates.setChecked(True)

        self.ui.actionContinue_Live_Updates.setChecked(False)
        self.live_updates = False

    def full_extent(self):
        """ Set the x axis to the full data range (12-bit), and set auto
        scale off.
        """
        log.debug("Set full extent")
        self.auto_scale = False
        local_plot = self.main_curve_dialog.get_plot()
        local_plot.set_axis_limits(0, 0, 4096)
        local_plot.replot()

    def reset_graph(self):
        """ Reset curve, image visualizations to the default. Trigger a
        auto scale replot manually in case pause mode is active.
        """
        log.debug("reset graph")
        self.auto_scale = True
        self.select_tool.action.setChecked(True)

        dgplot = self.main_curve_dialog.get_plot()
        dgplot.do_autoscale()

        dgimage = self.main_curve_dialog.get_plot()
        dgimage.do_autoscale()

    def process_select(self, status):
        """ Provide a default tool for panning the graph and to get out
        of zoom mode.
        """
        log.debug("Select tool clicked %s", status)

    def process_zoom(self, status):
        """ Zoom clicked, turn off auto scaling. The linkage with the
        guiqwt control handles cursor updates and actual zoom
        functionality.
        """
        log.debug("Zoom tool clicked %s", status)
        if status == "True":
            self.auto_scale = False

    def set_app_defaults(self):
        """ Call the various application control setup functions.
        """
        self.curve_render = 0
        self.image_render = 0
        self.image_height = 50
        self.image_data = []
        self.auto_scale = True

        self.create_actions()
        self.setup_signals()
        self.reset_graph()

        self.fps = utils.SimpleFPS()

        # Click the live button
        self.ui.actionContinue_Live_Updates.trigger()

    def setup_pipe_timer(self):
        """ This is a non-threaded application that uses qtimers with
        zero length delays to continuously poll the devices for data,
        while staying responsive to user events.
        """
        self.data_timer = QtCore.QTimer()
        self.data_timer.timeout.connect(self.update_visuals)
        self.data_timer.start(0)

    def update_visuals(self):
        """ Attempt to read from the pipe, update the graph.
        """

        result, data = self.dev.grab_pipe()

        if self.live_updates == True:
            self.update_graph(data)
            self.curve_render += 1
            self.update_image(data)
            self.check_image(self.curve_render)

        #if self.args.testing:
            #log.debug("render curve %s Start:%s End:%s" \
                      #% (self.curve_render, data[0], data[-1]))

        self.update_fps()
        self.data_timer.start(0)

    def check_image(self, render_count):
        """ Provide post-data population and form showing alignment and
        rendering of the image area.
        """
        if render_count != 1:
            return

        # If it's the first render, autoscale to make sure it lines up
        # properly. See update_image for why this is necessary
        local_plot = self.main_image_dialog.get_plot()
        local_plot.do_autoscale()

        # divided by the width of the image 1.0 / 0.4 is a guessed
        # value that seems to provide appropriate balance between
        # startup looks and non-breaking functionality when the
        # image is clicked.
        ratio = 1.0 / 0.4
        local_plot.set_aspect_ratio(ratio, lock=False)

        # Change the plot axis to have 0 in the lower left corner
        local_plot.set_axis_limits(0, -20, 50)

    def update_fps(self):
        """ Add tick, display the current rate.
        """
        self.fps.tick()
        fps_text = "Update: %s FPS" % self.fps.rate()
        self.action_fps_display.setText(fps_text)

    def update_graph(self, data_list):
        """ Get the current line plot from the available line graph,
        change it's data and replot.
        """
        #log.debug("render graph")
        x_axis = range(len(data_list))

        mcd = self.main_curve_dialog
        mcd.curve.set_data(x_axis, data_list)

        if self.auto_scale:
            mcd.get_plot().do_autoscale()
        else:
            mcd.get_plot().replot()

    def update_image(self, data):
        """ Add the line of data to the image data, if it is greater
        than the desired display size, roll it.
        """
        self.image_data.append(data)
        if len(self.image_data) > self.image_height:
            self.image_data = self.image_data[1:]

        img_data = range(len(self.image_data))

        position = 0
        while position < len(img_data):
            img_data[position] = self.image_data[position]
            position += 1

        new_data = numpy.array(img_data).astype(float)

        mid = self.main_image_dialog
        mid.image.set_data(new_data)

        # If you do autoscale here, it tends to jump around in appearing
        # to stretch to the window and be in 'normal' size
        mid.get_plot().replot()

        self.image_render += 1
        #if self.args.testing:
            #log.debug("render image %s Start:%s End:%s" \
                      #% (self.image_render, new_data[0][0],
                         #new_data[-1][-1]
                        #)
                     #)
