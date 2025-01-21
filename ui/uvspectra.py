# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'uvspectra.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_UVSpectra(object):
    def setupUi(self, UVSpectra):
        UVSpectra.setObjectName("UVSpectra")
        UVSpectra.resize(993, 700)
        self.centralwidget = QtWidgets.QWidget(UVSpectra)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.mplwidget = QtWidgets.QWidget(self.centralwidget)
        self.mplwidget.setMinimumSize(QtCore.QSize(0, 500))
        self.mplwidget.setObjectName("mplwidget")
        self.verticalLayout.addWidget(self.mplwidget)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.peaklabel = QtWidgets.QLabel(self.centralwidget)
        self.peaklabel.setObjectName("peaklabel")
        self.horizontalLayout_2.addWidget(self.peaklabel)
        self.peakwidth = QtWidgets.QSlider(self.centralwidget)
        self.peakwidth.setMinimum(1)
        self.peakwidth.setMaximum(20)
        self.peakwidth.setProperty("value", 7)
        self.peakwidth.setOrientation(QtCore.Qt.Horizontal)
        self.peakwidth.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.peakwidth.setTickInterval(1)
        self.peakwidth.setObjectName("peakwidth")
        self.horizontalLayout_2.addWidget(self.peakwidth)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.transitiontable = QtWidgets.QTableWidget(self.centralwidget)
        self.transitiontable.setObjectName("transitiontable")
        self.transitiontable.setColumnCount(0)
        self.transitiontable.setRowCount(0)
        self.transitiontable.horizontalHeader().setCascadingSectionResizes(True)
        self.transitiontable.horizontalHeader().setDefaultSectionSize(139)
        self.verticalLayout.addWidget(self.transitiontable)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.transnumber = QtWidgets.QSpinBox(self.centralwidget)
        self.transnumber.setProperty("value", 1)
        self.transnumber.setObjectName("transnumber")
        self.horizontalLayout.addWidget(self.transnumber)
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.horizontalLayout.addWidget(self.line)
        self.show_gaussian = QtWidgets.QCheckBox(self.centralwidget)
        self.show_gaussian.setChecked(True)
        self.show_gaussian.setObjectName("show_gaussian")
        self.horizontalLayout.addWidget(self.show_gaussian)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.savetransitions = QtWidgets.QPushButton(self.centralwidget)
        self.savetransitions.setObjectName("savetransitions")
        self.horizontalLayout.addWidget(self.savetransitions)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout.setStretch(0, 10)
        self.verticalLayout.setStretch(2, 3)
        UVSpectra.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(UVSpectra)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 993, 22))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuExperimental = QtWidgets.QMenu(self.menubar)
        self.menuExperimental.setObjectName("menuExperimental")
        UVSpectra.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(UVSpectra)
        self.statusbar.setObjectName("statusbar")
        UVSpectra.setStatusBar(self.statusbar)
        self.actionOpen_Output = QtWidgets.QAction(UVSpectra)
        self.actionOpen_Output.setObjectName("actionOpen_Output")
        self.actionClose = QtWidgets.QAction(UVSpectra)
        self.actionClose.setObjectName("actionClose")
        self.add_experiment_data = QtWidgets.QAction(UVSpectra)
        self.add_experiment_data.setObjectName("add_experiment_data")
        self.menuFile.addAction(self.actionOpen_Output)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionClose)
        self.menuExperimental.addAction(self.add_experiment_data)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuExperimental.menuAction())

        self.retranslateUi(UVSpectra)
        QtCore.QMetaObject.connectSlotsByName(UVSpectra)

    def retranslateUi(self, UVSpectra):
        _translate = QtCore.QCoreApplication.translate
        UVSpectra.setWindowTitle(_translate("UVSpectra", "UVSpectra"))
        self.label_2.setText(_translate("UVSpectra", "Peak width:"))
        self.peaklabel.setText(_translate("UVSpectra", "7"))
        self.label.setText(_translate("UVSpectra", "Total Peaks:"))
        self.show_gaussian.setText(_translate("UVSpectra", "Show gaussians"))
        self.savetransitions.setText(_translate("UVSpectra", "Save Transitions"))
        self.menuFile.setTitle(_translate("UVSpectra", "File"))
        self.menuExperimental.setTitle(_translate("UVSpectra", "Experimental"))
        self.actionOpen_Output.setText(_translate("UVSpectra", "Open Output"))
        self.actionClose.setText(_translate("UVSpectra", "Close"))
        self.add_experiment_data.setText(_translate("UVSpectra", "Add experiment data"))
