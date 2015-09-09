#!/usr/bin/env python
""" LineGrab - use various communication methods to display large line
graphs of data from cameras.
"""

import sys
import numpy
import logging
import argparse

from PyQt4 import QtGui, QtCore

from linegrab import visualize
from linegrab import devices
from linegrab import utils

logging.basicConfig(filename="LineGrab_log.txt", filemode="w",
                    level=logging.DEBUG)
log = logging.getLogger()

class LineGrabApplication(object):
    """ Create the window with the graphs, setup communication based on
    the specified device.
    """
    def __init__(self):
        super(LineGrabApplication, self).__init__()
        log.debug("LineGrabApplication startup")
        self.parser = self.create_parser()
        self.curve_render = 0
        self.image_render = 0
        self.image_height = 50
        self.image_data = []
        self.auto_scale = True

    def setup_pipe_timer(self):
        """ This is a non-threaded application that uses qtimers with
        zero length delays to continuously poll the devices for data,
        while staying responsive to user events.
        """
        self.dataTimer = QtCore.QTimer()
        self.dataTimer.timeout.connect(self.update_visuals)
        self.dataTimer.start(0)

    def update_visuals(self):
        """ Attempt to read from the pipe, update the graph.
        """

        result, data = self.dev.grab_pipe()

        if not result:
            log.warn("Problem reading from pipe")
        
        if self.live_updates == True:
            self.update_graph(data)
            self.curve_render += 1
            self.update_image(data)
            self.check_image(self.curve_render)

        if self.args.testing:
            log.debug("render curve %s Start:%s End:%s" \
                      % (self.curve_render, data[0], data[-1]))

        self.update_fps()
        self.dataTimer.start(0)

    def check_image(self, render_count):
        """ Provide post-data population and form showing alignment and
        rendering of the image area.
        """
        if render_count != 1:
            return

        # If it's the first render, autoscale to make sure it lines up
        # properly. See update_image for why this is necessary
        local_plot = self.DarkGraphs.MainImageDialog.get_plot()
        local_plot.do_autoscale()

        # divided by the width of the image 1.0 / 0.4 is a guessed
        # value that seems to provide appropriate balance between
        # startup looks and non-breaking functionality when the
        # image is clicked.
        ratio = 1.0 / 0.4
        local_plot.set_aspect_ratio(ratio, lock=False)
        
        # Change the plot axis to have 0 in the lower left corner
        local_plot.set_axis_limits(0, -5, 50)

    def update_fps(self):
        """ Add tick, display the current rate.
        """
        self.fps.tick()
        fps_text = "Update: %s FPS" % self.fps.rate()
        self.actionFPSDisplay.setText(fps_text)

    def update_graph(self, data_list):
        """ Get the current line plot from the available line graph, 
        change it's data and replot.
        """
        #log.debug("render graph")
        x_axis = range(len(data_list))

        mcd = self.DarkGraphs.MainCurveDialog
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
        for item in img_data:
            img_data[position] = self.image_data[position]
            position += 1

        new_data = numpy.array(img_data).astype(float)

        mid = self.DarkGraphs.MainImageDialog
        mid.image.set_data(new_data)

        # If you do autoscale here, it tends to jump around in appearing
        # to stretch to the window and be in 'normal' size
        mid.get_plot().replot()

        self.image_render += 1
        if self.args.testing:
            log.debug("render image %s Start:%s End:%s" \
                      % (self.image_render, new_data[0][0],
                         new_data[-1][-1]
                        )
                     )
 
    def closeEvent(self):
        """ close the pipes, stop all the timers.
        """
        log.info("Attempt to close pipe")
        result = self.dev.close_pipe()
        log.info("Close pipe result: %s" % result)
        self.dataTimer.stop()


    def parse_args(self, argv):
        """ Handle any bad arguments, then set defaults. Creates
        connection to pipe data source.
        """
        self.args = self.parser.parse_args(argv)

        if self.args.source == "simulation":
            log.info("Create simulated spectra device")
            self.dev = devices.SimulatedSpectraDevice()

        result = self.dev.setup_pipe()
        log.info("Result of pipe setup: %s" % result)

        return self.args


    def create_parser(self):
        desc = "acquire from specified device, display line graph"
        parser = argparse.ArgumentParser(description=desc)
    
        parser.add_argument("-t", "--testing", action="store_true",
            help="Automatically terminate the program for testing")
    
        parser.add_argument("-s", "--source", required=True,
            default="simulation", 
            choices=["simulation", "e2v", "cobra"],
            help="Data source for visualization")
    
        return parser

    def create_actions(self):
        """ Runtime generated toolbars to link guiqwt graph controls
        with the mainwindow level toolbars.
        """
        dg = self.DarkGraphs
        dgct = self.DarkGraphs.curve_toolbar.addAction

        agfe = dgct(QtGui.QIcon(":/greys/greys/full_extent.svg"),
                    "Full extent graph"
                   )
        self.actionGraphFullExtent = agfe

        agr = dgct(QtGui.QIcon(":/greys/greys/reset.svg"),
                   "Reset graph parameters"
                  )
        self.actionGraphReset = agr

        spacer = QtGui.QWidget()
        spacer.setSizePolicy(QtGui.QSizePolicy.Expanding,
                             QtGui.QSizePolicy.Expanding)
        dg.curve_toolbar.addWidget(spacer)

        act_name = "Instantaneous performance"
        self.actionFPSDisplay = QtGui.QAction(act_name, self.app)
        dg.curve_toolbar.addAction(self.actionFPSDisplay)

        # Remove the placeholder toolbar
        dg.ui.toolBar_GraphControls.setVisible(False)

    def setup_signals(self):
        """ Hook into darkgraphs emitted signals for controller level.
        """
        dg = self.DarkGraphs

        # Hook the play/pause buttons
        dg.ui.actionContinue_Live_Updates.triggered.connect(self.on_live)
        dg.ui.actionPause_Live_Updates.triggered.connect(self.on_pause)
       
        # Custom graph buttons 
        self.actionGraphReset.triggered.connect(self.reset_graph)
        self.actionGraphFullExtent.triggered.connect(self.full_extent)

        # Custom tools generated in visualize that are not actions
        dg.zoom_tool.wrap_sig.clicked.connect(self.process_zoom)
        dg.select_tool.wrap_sig.clicked.connect(self.process_select)

    def on_live(self, action):
        """ Live and pause buttons are the equivalent of toggle buttons.
        Only one can be enabled at a time.
        """
        log.info("Click live updates")
        dgui = self.DarkGraphs.ui
        if action == False:
            dgui.actionContinue_Live_Updates.setChecked(True)

        self.DarkGraphs.ui.actionPause_Live_Updates.setChecked(False)
        self.live_updates = True

    def on_pause(self, action):
        """ Pause and live buttons are the equivalent of toggle buttons.
        Only one can be enabled at a time.
        """
        log.info("Pause live updates: %s" % action)
        dgui = self.DarkGraphs.ui
        if action == False:
            dgui.actionPause_Live_Updates.setChecked(True)

        self.DarkGraphs.ui.actionContinue_Live_Updates.setChecked(False)
        self.live_updates = False

    def full_extent(self):
        """ Set the x axis to the full data range (12-bit), and set auto
        scale off.
        """
        log.debug("Set full extent")
        self.auto_scale = False
        local_plot = self.DarkGraphs.MainCurveDialog.get_plot()
        local_plot.set_axis_limits(0, 0, 4096)
        local_plot.replot()

    def reset_graph(self):
        """ Reset curve, image visualizations to the default. Trigger a
        auto scale replot manually in case pause mode is active.
        """
        log.debug("reset graph")
        self.auto_scale = True
        self.DarkGraphs.select_tool.action.setChecked(True)

        dgplot = self.DarkGraphs.MainCurveDialog.get_plot()
        dgplot.do_autoscale()

        dgimage = self.DarkGraphs.MainCurveDialog.get_plot()
        dgimage.do_autoscale()
 
    def process_select(self, status):
        """ Provide a default tool for panning the graph and to get out
        of zoom mode.
        """
        log.debug("Select tool clicked %s" % status)

    def process_zoom(self, status):
        """ Zoom clicked, turn off auto scaling. The linkage with the
        guiqwt control handles cursor updates and actual zoom
        functionality.
        """
        log.debug("Zoom tool clicked %s" % status)
        if status == "True":
            self.auto_scale = False

    def delay_close(self):
        """ For testing purposes, create a qtimer that triggers the
        DarkGraphs's close event after a delay.
        """
        log.debug("Trigger delay close")
        self.closeTimer = QtCore.QTimer()
        self.closeTimer.timeout.connect(self.DarkGraphs.close)
        self.closeTimer.start(3000)

    def set_app_defaults(self):
        """ Call the various application control setup functions.
        """
        self.create_actions()
        self.setup_signals()
        self.reset_graph()

        self.fps = utils.SimpleFPS()

        # Click the live button
        self.DarkGraphs.ui.actionContinue_Live_Updates.trigger()

    def run(self):
        """ This is the application code that is called by the main
        function. The architectural idea is to have as little code in
        main as possible and create the qapplication here so the
        nosetests can function.
        """
        self.app = QtGui.QApplication([])
        self.DarkGraphs = visualize.DarkGraphs()

        self.set_app_defaults()
        self.setup_pipe_timer()

        if self.args.testing:
            self.delay_close()

        self.DarkGraphs.show()
        sys.exit(self.app.exec_())


def main(argv=None):
    if argv is None: 
        from sys import argv as sys_argv 
        argv = sys_argv 
   
    argv = argv[1:] 
    log.debug("Arguments: %s" % argv)

    exit_code = 0
    try:
        lngapp = LineGrabApplication()
        lngapp.parse_args(argv)
        lngapp.run()

    except SystemExit, exc:
        exit_code = exc.code
    
    return exit_code 

if __name__ == "__main__":
    sys.exit(main(sys.argv))
