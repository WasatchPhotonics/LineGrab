#!/usr/bin/env python
""" LineGrab - use various communication methods to display large line
graphs of data from cameras.
"""

import sys
import logging
import argparse

from PyQt4 import QtGui, QtCore

from linegrab import visualize

logging.basicConfig(filename="LineGrab_log.txt", level=logging.DEBUG)
log = logging.getLogger()

class LineGrabApplication(object):
    """ Create the window with the graphs, setup communication based on
    the specified device.
    """
    def __init__(self):
        super(LineGrabApplication, self).__init__()
        log.debug("LineGrabApplication startup")
        self.parser = self.create_parser()

    def parse_args(self, argv):
        """ Handle any bad arguments, then set defaults
        """
        self.args = self.parser.parse_args(argv)
        return self.args


    def create_parser(self):
        desc = "acquire from specified device, display line graph"
        parser = argparse.ArgumentParser(description=desc)
    
        parser.add_argument("-t", "--testing", action="store_true",
            help="Automatically terminate the program for testing")

        parser.add_argument("-e", "--e2v", action="store_true",
            help="Use E2V camera")

        parser.add_argument("-c", "--cobra", action="store_true",
            help="Use Wasatch Photonics Cobra camera")
    
        return parser

    def run(self):
        log.debug("Create application")
        self.app = QtGui.QApplication([])
        self.form = visualize.DualGraphs()

        if self.args.testing:
            self.delay_close()

        self.form.show()
        sys.exit(self.app.exec_())

    def delay_close(self):
        """ For testing purposes, create a qtimer that triggers the
        form's close event after a delay.
        """
        log.debug("Trigger delay close")
        self.closeTimer = QtCore.QTimer()
        self.closeTimer.timeout.connect(self.form.close)
        self.closeTimer.start(1000)

def main(argv=None):
    if argv is None: 
        from sys import argv as sys_argv 
        argv = sys_argv 

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