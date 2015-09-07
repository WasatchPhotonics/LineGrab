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

    def setup_pipe_timer(self):
        """ This is a non-threaded application that uses qtimers with
        zero length delays to continuously poll the devices for data,
        while staying responsive to user events.
        """
        self.dataTimer = QtCore.QTimer()
        self.dataTimer.timeout.connect(self.update_visuals)
        self.dataTimer.start(500)

    def update_visuals(self):
        """ Attempt to read from the pipe, update the graph.
        """

        result, data = self.dev.grab_pipe()

        if not result:
            log.warn("Problem reading from pipe")
        
        self.update_graph(data)
        self.curve_render += 1

        if self.args.testing:
            log.debug("render curve %s Start:%s End:%s" \
                      % (self.curve_render, data[0], data[-1]))

        self.update_image(data)

        self.dataTimer.start(0)

    def update_graph(self, data_list):
        """ Get the current line plot from the available line graph, 
        change it's data and replot.
        """
        log.debug("render graph")
        x_axis = range(len(data_list))

        mcw = self.DarkGraphs.MainCurveWidget
        mcw.curve.set_data(x_axis, data_list)
            
        mcw.get_plot().do_autoscale()
      
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

        mci = self.DarkGraphs.MainImageDialog
        mci.image.set_data(new_data)
        mci.get_plot().do_autoscale()

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
        """ Handle any bad arguments, then set defaults
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

    def run(self):
        log.debug("Create application")
        self.app = QtGui.QApplication([])
        self.DarkGraphs = visualize.DarkGraphs()
        self.setup_pipe_timer()

        if self.args.testing:
            self.delay_close()

        self.DarkGraphs.show()
        sys.exit(self.app.exec_())

    def delay_close(self):
        """ For testing purposes, create a qtimer that triggers the
        DarkGraphs's close event after a delay.
        """
        log.debug("Trigger delay close")
        self.closeTimer = QtCore.QTimer()
        self.closeTimer.timeout.connect(self.DarkGraphs.close)
        self.closeTimer.start(3000)

def main(argv=None):
    if argv is None: 
        from sys import argv as sys_argv 
        argv = sys_argv 
   
    argv = argv[1:] 
    log.debug("Clip arguments to: %s" % argv)

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
