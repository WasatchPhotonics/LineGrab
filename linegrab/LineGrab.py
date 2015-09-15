#!/usr/bin/env python
""" LineGrab - use various communication methods to display large line
graphs of data from cameras.
"""

import sys
import logging
import argparse

from PyQt4 import QtGui

from linegrab import controller

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
        self.form = None
        self.args = None

    def parse_args(self, argv):
        """ Handle any bad arguments, then set defaults.
        """
        log.debug("Process args: %s", argv)
        self.args = self.parser.parse_args(argv)
        return self.args

    def create_parser(self):
        """ Create the parser with arguments specific to this
        application.
        """
        desc = "acquire from specified device, display line graph"
        parser = argparse.ArgumentParser(description=desc)

        help_str = "Automatically terminate the program for testing"
        parser.add_argument("-t", "--testing", action="store_true",
                            help=help_str)

        help_str = "Data source for visualization"
        choices = ["simulation", "e2v", "cobra", "basler"]
        parser.add_argument("-s", "--source", required=True,
                            default="simulation",
                            choices=choices,
                            help=help_str)

        return parser

    def run(self):
        """ This is the application code that is called by the main
        function. The architectural idea is to have as little code in
        main as possible and create the qapplication here so the
        nosetests can function. Only create the application if not using
        the unittest generated controller.
        """
        if not self.args.testing:
            app = QtGui.QApplication([])

        self.form = controller.CurveImage()
        self.form.set_parameters(self.args)

        if not self.args.testing:
            sys.exit(app.exec_())


def main(argv=None):
    """ main calls the wrapper code around the application objects with
    as little framework as possible. See:
    https://groups.google.com/d/msg/comp.lang.python/j_tFS3uUFBY/\
        ciA7xQMe6TMJ
    """
    if argv is None:
        from sys import argv as sys_argv
        argv = sys_argv

    argv = argv[1:]
    log.debug("Arguments: %s", argv)

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
