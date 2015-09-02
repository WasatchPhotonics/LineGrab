#!/usr/bin/env python
""" LineGrab - use various communication methods to display large line
graphs of data from cameras.
"""

import sys
import logging
import argparse

log = logging.getLogger(__name__)


class LineGrabApplication(object):
    """ Create the window with the graphs, setup communication based on
    the specified device.
    """
    def __init__(self):
        super(LineGrabApplication, self).__init__()
        log.debug("LineGrabApplication startup")
        self.parser = self.create_parser()

    def parse_args(self, argv):
        """ Handle any bad arguments, the set defaults
        """
        log.warn("clear args")
        self.args = self.parser.parse_args([])
        return self.args


    def create_parser(self):
        desc = "acquire from specified device, display line graph"
        parser = argparse.ArgumentParser(description=desc)
    
        parser.add_argument("-e", "--e2v", action="store_true",
            help="Use E2V camera")

        parser.add_argument("-c", "--cobra", action="store_true",
            help="Use Wasatch Photonics Cobra camera")
    
        return parser
    

def main(argv=None):
    if argv is None: 
        from sys import argv as sys_argv 
        argv = sys_argv 

    try:
        
        wsdapp = WasatchDeviceApplication()
        wsdapp.parse_args(argv)
        wsdapp.run()
    except SystemExit, exc:
        exit_code = exc.code
    
    return exit_code 

if __name__ == "__main__":
    sys.exit(main(sys.argv))
