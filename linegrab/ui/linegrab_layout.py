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
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1080, 23))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.toolBar = QtGui.QToolBar(MainWindow)
        self.toolBar.setMinimumSize(QtCore.QSize(0, 0))
        self.toolBar.setIconSize(QtCore.QSize(24, 24))
        self.toolBar.setObjectName(_fromUtf8("toolBar"))
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        MainWindow.insertToolBarBreak(self.toolBar)
        self.actionTestaction = QtGui.QAction(MainWindow)
        self.actionTestaction.setCheckable(True)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/material/material/ic_play_arrow_black_48px.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionTestaction.setIcon(icon)
        self.actionTestaction.setObjectName(_fromUtf8("actionTestaction"))
        self.actionSecondary = QtGui.QAction(MainWindow)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/material/material/ic_vertical_align_top_black_48px.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSecondary.setIcon(icon1)
        self.actionSecondary.setObjectName(_fromUtf8("actionSecondary"))
        self.actionBiglongone = QtGui.QAction(MainWindow)
        self.actionBiglongone.setCheckable(True)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/material/material/ic_center_focus_strong_black_48px.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionBiglongone.setIcon(icon2)
        self.actionBiglongone.setObjectName(_fromUtf8("actionBiglongone"))
        self.actionBiglongone_2 = QtGui.QAction(MainWindow)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8(":/material/material/ic_pause_circle_outline_black_48px.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionBiglongone_2.setIcon(icon3)
        self.actionBiglongone_2.setObjectName(_fromUtf8("actionBiglongone_2"))
        self.actionPauseDisplay = QtGui.QAction(MainWindow)
        self.actionPauseDisplay.setCheckable(True)
        self.actionPauseDisplay.setIcon(icon)
        self.actionPauseDisplay.setObjectName(_fromUtf8("actionPauseDisplay"))
        self.actionAutoScale = QtGui.QAction(MainWindow)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(_fromUtf8(":/material/material/ic_play_circle_outline_black_48px.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionAutoScale.setIcon(icon4)
        self.actionAutoScale.setObjectName(_fromUtf8("actionAutoScale"))
        self.actionFull_Extent = QtGui.QAction(MainWindow)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(_fromUtf8(":/material/material/ic_vertical_align_center_black_48px.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionFull_Extent.setIcon(icon5)
        self.actionFull_Extent.setObjectName(_fromUtf8("actionFull_Extent"))
        self.toolBar.addAction(self.actionAutoScale)
        self.toolBar.addAction(self.actionBiglongone_2)
        self.toolBar.addAction(self.actionFull_Extent)
        self.toolBar.addAction(self.actionTestaction)
        self.toolBar.addAction(self.actionSecondary)
        self.toolBar.addAction(self.actionBiglongone)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.labelCurvePlaceholder.setText(_translate("MainWindow", "Main curve plot area", None))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar", None))
        self.actionTestaction.setText(_translate("MainWindow", "testaction", None))
        self.actionSecondary.setText(_translate("MainWindow", "secondary", None))
        self.actionBiglongone.setText(_translate("MainWindow", "biglongone", None))
        self.actionBiglongone.setToolTip(_translate("MainWindow", "tooltip for big long one", None))
        self.actionBiglongone_2.setText(_translate("MainWindow", "biglongone", None))
        self.actionBiglongone_2.setToolTip(_translate("MainWindow", "tooltip for big long one", None))
        self.actionPauseDisplay.setText(_translate("MainWindow", "PauseDisplay", None))
        self.actionPauseDisplay.setToolTip(_translate("MainWindow", "Pause the rendering of data", None))
        self.actionAutoScale.setText(_translate("MainWindow", "AutoScale", None))
        self.actionAutoScale.setToolTip(_translate("MainWindow", "Toggle auto scaling", None))
        self.actionFull_Extent.setText(_translate("MainWindow", "Full Extent", None))
        self.actionFull_Extent.setToolTip(_translate("MainWindow", "Show the full extent of data", None))

import iconagraphy_rc
