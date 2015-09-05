#!/usr/bin/env python
""" testing area for dark themed, application wide style-sheets
"""

import sys
import numpy
import logging
import argparse

from PyQt4 import QtGui, QtCore

logging.basicConfig(filename="LineGrab_log.txt", filemode="w",
                    level=logging.DEBUG)
log = logging.getLogger()

class DarkTestApplication(QtGui.QMainWindow):
    """ Import the generated py file from the qt-designer created .ui
    file. Apply the system-wide style sheet. Integrate with actual
    guiqwt curve and image controls.
    """

    def __init__(self):
        super(DarkTestApplication, self).__init__()

        from linegrab.ui.linegrab_layout import Ui_MainWindow
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.show()


def main(argv=None):
    app = QtGui.QApplication(argv)
    darkapp = DarkTestApplication()
    darkapp.run()
    sys.exit(darkapp.exec_())

if __name__ == "__main__":
    sys.exit(main(sys.argv))
