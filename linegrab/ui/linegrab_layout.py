# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'linegrab/ui/linegrab_layout.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(1080, 600)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/images/LineGrab_Icon.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.frameCurve = QtGui.QFrame(self.centralwidget)
        self.frameCurve.setFrameShape(QtGui.QFrame.NoFrame)
        self.frameCurve.setFrameShadow(QtGui.QFrame.Plain)
        self.frameCurve.setLineWidth(0)
        self.frameCurve.setObjectName(_fromUtf8("frameCurve"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.frameCurve)
        self.verticalLayout_3.setMargin(0)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.verticalLayoutCurve = QtGui.QVBoxLayout()
        self.verticalLayoutCurve.setObjectName(_fromUtf8("verticalLayoutCurve"))
        self.labelCurvePlaceholder = QtGui.QLabel(self.frameCurve)
        self.labelCurvePlaceholder.setObjectName(_fromUtf8("labelCurvePlaceholder"))
        self.verticalLayoutCurve.addWidget(self.labelCurvePlaceholder)
        self.verticalLayout_3.addLayout(self.verticalLayoutCurve)
        self.verticalLayout.addWidget(self.frameCurve)
        self.frameImage = QtGui.QFrame(self.centralwidget)
        self.frameImage.setMinimumSize(QtCore.QSize(0, 150))
        self.frameImage.setMaximumSize(QtCore.QSize(16777215, 150))
        self.frameImage.setFrameShape(QtGui.QFrame.NoFrame)
        self.frameImage.setFrameShadow(QtGui.QFrame.Plain)
        self.frameImage.setLineWidth(0)
        self.frameImage.setObjectName(_fromUtf8("frameImage"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.frameImage)
        self.horizontalLayout_3.setMargin(0)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.verticalLayoutImage = QtGui.QVBoxLayout()
        self.verticalLayoutImage.setSpacing(0)
        self.verticalLayoutImage.setObjectName(_fromUtf8("verticalLayoutImage"))
        self.labelImagePlaceholder = QtGui.QLabel(self.frameImage)
        self.labelImagePlaceholder.setText(_fromUtf8(""))
        self.labelImagePlaceholder.setPixmap(QtGui.QPixmap(_fromUtf8(":/images/example_heatmap_with_axis.png")))
        self.labelImagePlaceholder.setScaledContents(True)
        self.labelImagePlaceholder.setObjectName(_fromUtf8("labelImagePlaceholder"))
        self.verticalLayoutImage.addWidget(self.labelImagePlaceholder)
        self.horizontalLayout_3.addLayout(self.verticalLayoutImage)
        self.verticalLayout.addWidget(self.frameImage)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1080, 25))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.toolBar = QtGui.QToolBar(MainWindow)
        self.toolBar.setMinimumSize(QtCore.QSize(0, 0))
        self.toolBar.setIconSize(QtCore.QSize(48, 48))
        self.toolBar.setObjectName(_fromUtf8("toolBar"))
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.actionPause_Live_Updates = QtGui.QAction(MainWindow)
        self.actionPause_Live_Updates.setCheckable(True)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/greys/greys/pause.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionPause_Live_Updates.setIcon(icon1)
        self.actionPause_Live_Updates.setObjectName(_fromUtf8("actionPause_Live_Updates"))
        self.actionContinue_Live_Updates = QtGui.QAction(MainWindow)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/greys/greys/forward.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionContinue_Live_Updates.setIcon(icon2)
        self.actionContinue_Live_Updates.setObjectName(_fromUtf8("actionContinue_Live_Updates"))
        self.actionZoom_graph = QtGui.QAction(MainWindow)
        self.actionZoom_graph.setCheckable(True)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8(":/greys/greys/zoom.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionZoom_graph.setIcon(icon3)
        self.actionZoom_graph.setObjectName(_fromUtf8("actionZoom_graph"))
        self.actionReset_Graph = QtGui.QAction(MainWindow)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(_fromUtf8(":/greys/greys/reset.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionReset_Graph.setIcon(icon4)
        self.actionReset_Graph.setObjectName(_fromUtf8("actionReset_Graph"))
        self.actionFrameratetext = QtGui.QAction(MainWindow)
        self.actionFrameratetext.setObjectName(_fromUtf8("actionFrameratetext"))
        self.toolBar.addAction(self.actionContinue_Live_Updates)
        self.toolBar.addAction(self.actionPause_Live_Updates)
        self.toolBar.addAction(self.actionZoom_graph)
        self.toolBar.addAction(self.actionReset_Graph)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionFrameratetext)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "LineGrab", None))
        self.labelCurvePlaceholder.setText(_translate("MainWindow", "Main curve plot area", None))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar", None))
        self.actionPause_Live_Updates.setText(_translate("MainWindow", "Pause Live Updates", None))
        self.actionPause_Live_Updates.setToolTip(_translate("MainWindow", "Stop the curve and image updates", None))
        self.actionContinue_Live_Updates.setText(_translate("MainWindow", "Continue Live Updates", None))
        self.actionContinue_Live_Updates.setToolTip(_translate("MainWindow", "Restart display of data on curve and image", None))
        self.actionZoom_graph.setText(_translate("MainWindow", "Zoom graph", None))
        self.actionZoom_graph.setToolTip(_translate("MainWindow", "Activate zoom control", None))
        self.actionReset_Graph.setText(_translate("MainWindow", "Reset Graph", None))
        self.actionReset_Graph.setToolTip(_translate("MainWindow", "Restore curve and image settings to default", None))
        self.actionFrameratetext.setText(_translate("MainWindow", "frameratetext", None))
        self.actionFrameratetext.setToolTip(_translate("MainWindow", "Curve and Image render FPS", None))

import iconagraphy_rc
