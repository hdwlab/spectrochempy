# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'examples/VideoTemplate.ui'
#
# Created: Wed Oct 26 09:21:01 2016
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(695, 798)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.downsampleCheck = QtGui.QCheckBox(self.centralwidget)
        self.downsampleCheck.setObjectName("downsampleCheck")
        self.gridLayout_2.addWidget(self.downsampleCheck, 8, 0, 1, 2)
        self.scaleCheck = QtGui.QCheckBox(self.centralwidget)
        self.scaleCheck.setObjectName("scaleCheck")
        self.gridLayout_2.addWidget(self.scaleCheck, 4, 0, 1, 1)
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.rawRadio = QtGui.QRadioButton(self.centralwidget)
        self.rawRadio.setObjectName("rawRadio")
        self.gridLayout.addWidget(self.rawRadio, 3, 0, 1, 1)
        self.gfxRadio = QtGui.QRadioButton(self.centralwidget)
        self.gfxRadio.setChecked(True)
        self.gfxRadio.setObjectName("gfxRadio")
        self.gridLayout.addWidget(self.gfxRadio, 2, 0, 1, 1)
        self.stack = QtGui.QStackedWidget(self.centralwidget)
        self.stack.setObjectName("stack")
        self.page = QtGui.QWidget()
        self.page.setObjectName("page")
        self.gridLayout_3 = QtGui.QGridLayout(self.page)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.graphicsView = GraphicsView(self.page)
        self.graphicsView.setObjectName("graphicsView")
        self.gridLayout_3.addWidget(self.graphicsView, 0, 0, 1, 1)
        self.stack.addWidget(self.page)
        self.page_2 = QtGui.QWidget()
        self.page_2.setObjectName("page_2")
        self.gridLayout_4 = QtGui.QGridLayout(self.page_2)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.rawImg = RawImageWidget(self.page_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.rawImg.sizePolicy().hasHeightForWidth())
        self.rawImg.setSizePolicy(sizePolicy)
        self.rawImg.setObjectName("rawImg")
        self.gridLayout_4.addWidget(self.rawImg, 0, 0, 1, 1)
        self.stack.addWidget(self.page_2)
        self.gridLayout.addWidget(self.stack, 0, 0, 1, 1)
        self.rawGLRadio = QtGui.QRadioButton(self.centralwidget)
        self.rawGLRadio.setObjectName("rawGLRadio")
        self.gridLayout.addWidget(self.rawGLRadio, 4, 0, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 1, 0, 1, 4)
        self.dtypeCombo = QtGui.QComboBox(self.centralwidget)
        self.dtypeCombo.setObjectName("dtypeCombo")
        self.dtypeCombo.addItem("")
        self.dtypeCombo.addItem("")
        self.dtypeCombo.addItem("")
        self.gridLayout_2.addWidget(self.dtypeCombo, 3, 2, 1, 1)
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 3, 0, 1, 1)
        self.rgbLevelsCheck = QtGui.QCheckBox(self.centralwidget)
        self.rgbLevelsCheck.setObjectName("rgbLevelsCheck")
        self.gridLayout_2.addWidget(self.rgbLevelsCheck, 4, 1, 1, 1)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.minSpin2 = SpinBox(self.centralwidget)
        self.minSpin2.setEnabled(False)
        self.minSpin2.setObjectName("minSpin2")
        self.horizontalLayout_2.addWidget(self.minSpin2)
        self.label_3 = QtGui.QLabel(self.centralwidget)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_2.addWidget(self.label_3)
        self.maxSpin2 = SpinBox(self.centralwidget)
        self.maxSpin2.setEnabled(False)
        self.maxSpin2.setObjectName("maxSpin2")
        self.horizontalLayout_2.addWidget(self.maxSpin2)
        self.gridLayout_2.addLayout(self.horizontalLayout_2, 5, 2, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.minSpin1 = SpinBox(self.centralwidget)
        self.minSpin1.setObjectName("minSpin1")
        self.horizontalLayout.addWidget(self.minSpin1)
        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.maxSpin1 = SpinBox(self.centralwidget)
        self.maxSpin1.setObjectName("maxSpin1")
        self.horizontalLayout.addWidget(self.maxSpin1)
        self.gridLayout_2.addLayout(self.horizontalLayout, 4, 2, 1, 1)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.minSpin3 = SpinBox(self.centralwidget)
        self.minSpin3.setEnabled(False)
        self.minSpin3.setObjectName("minSpin3")
        self.horizontalLayout_3.addWidget(self.minSpin3)
        self.label_4 = QtGui.QLabel(self.centralwidget)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_3.addWidget(self.label_4)
        self.maxSpin3 = SpinBox(self.centralwidget)
        self.maxSpin3.setEnabled(False)
        self.maxSpin3.setObjectName("maxSpin3")
        self.horizontalLayout_3.addWidget(self.maxSpin3)
        self.gridLayout_2.addLayout(self.horizontalLayout_3, 6, 2, 1, 1)
        self.lutCheck = QtGui.QCheckBox(self.centralwidget)
        self.lutCheck.setObjectName("lutCheck")
        self.gridLayout_2.addWidget(self.lutCheck, 7, 0, 1, 1)
        self.alphaCheck = QtGui.QCheckBox(self.centralwidget)
        self.alphaCheck.setObjectName("alphaCheck")
        self.gridLayout_2.addWidget(self.alphaCheck, 7, 1, 1, 1)
        self.gradient = GradientWidget(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.gradient.sizePolicy().hasHeightForWidth())
        self.gradient.setSizePolicy(sizePolicy)
        self.gradient.setObjectName("gradient")
        self.gridLayout_2.addWidget(self.gradient, 7, 2, 1, 2)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem, 3, 3, 1, 1)
        self.fpsLabel = QtGui.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.fpsLabel.setFont(font)
        self.fpsLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.fpsLabel.setObjectName("fpsLabel")
        self.gridLayout_2.addWidget(self.fpsLabel, 0, 0, 1, 4)
        self.rgbCheck = QtGui.QCheckBox(self.centralwidget)
        self.rgbCheck.setObjectName("rgbCheck")
        self.gridLayout_2.addWidget(self.rgbCheck, 3, 1, 1, 1)
        self.label_5 = QtGui.QLabel(self.centralwidget)
        self.label_5.setObjectName("label_5")
        self.gridLayout_2.addWidget(self.label_5, 2, 0, 1, 1)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.framesSpin = QtGui.QSpinBox(self.centralwidget)
        self.framesSpin.setButtonSymbols(QtGui.QAbstractSpinBox.NoButtons)
        self.framesSpin.setProperty("value", 10)
        self.framesSpin.setObjectName("framesSpin")
        self.horizontalLayout_4.addWidget(self.framesSpin)
        self.widthSpin = QtGui.QSpinBox(self.centralwidget)
        self.widthSpin.setButtonSymbols(QtGui.QAbstractSpinBox.PlusMinus)
        self.widthSpin.setMaximum(10000)
        self.widthSpin.setProperty("value", 512)
        self.widthSpin.setObjectName("widthSpin")
        self.horizontalLayout_4.addWidget(self.widthSpin)
        self.heightSpin = QtGui.QSpinBox(self.centralwidget)
        self.heightSpin.setButtonSymbols(QtGui.QAbstractSpinBox.NoButtons)
        self.heightSpin.setMaximum(10000)
        self.heightSpin.setProperty("value", 512)
        self.heightSpin.setObjectName("heightSpin")
        self.horizontalLayout_4.addWidget(self.heightSpin)
        self.gridLayout_2.addLayout(self.horizontalLayout_4, 2, 1, 1, 2)
        self.sizeLabel = QtGui.QLabel(self.centralwidget)
        self.sizeLabel.setText("")
        self.sizeLabel.setObjectName("sizeLabel")
        self.gridLayout_2.addWidget(self.sizeLabel, 2, 3, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.stack.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.downsampleCheck.setText(QtGui.QApplication.translate("MainWindow", "Auto downsample", None, QtGui.QApplication.UnicodeUTF8))
        self.scaleCheck.setText(QtGui.QApplication.translate("MainWindow", "Scale Data", None, QtGui.QApplication.UnicodeUTF8))
        self.rawRadio.setText(QtGui.QApplication.translate("MainWindow", "RawImageWidget", None, QtGui.QApplication.UnicodeUTF8))
        self.gfxRadio.setText(QtGui.QApplication.translate("MainWindow", "GraphicsView + ImageItem", None, QtGui.QApplication.UnicodeUTF8))
        self.rawGLRadio.setText(QtGui.QApplication.translate("MainWindow", "RawGLImageWidget", None, QtGui.QApplication.UnicodeUTF8))
        self.dtypeCombo.setItemText(0, QtGui.QApplication.translate("MainWindow", "uint8", None, QtGui.QApplication.UnicodeUTF8))
        self.dtypeCombo.setItemText(1, QtGui.QApplication.translate("MainWindow", "uint16", None, QtGui.QApplication.UnicodeUTF8))
        self.dtypeCombo.setItemText(2, QtGui.QApplication.translate("MainWindow", "float", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("MainWindow", "Data type", None, QtGui.QApplication.UnicodeUTF8))
        self.rgbLevelsCheck.setText(QtGui.QApplication.translate("MainWindow", "RGB", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("MainWindow", "<--->", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("MainWindow", "<--->", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("MainWindow", "<--->", None, QtGui.QApplication.UnicodeUTF8))
        self.lutCheck.setText(QtGui.QApplication.translate("MainWindow", "Use Lookup  Table", None, QtGui.QApplication.UnicodeUTF8))
        self.alphaCheck.setText(QtGui.QApplication.translate("MainWindow", "alpha", None, QtGui.QApplication.UnicodeUTF8))
        self.fpsLabel.setText(QtGui.QApplication.translate("MainWindow", "FPS", None, QtGui.QApplication.UnicodeUTF8))
        self.rgbCheck.setText(QtGui.QApplication.translate("MainWindow", "RGB", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("MainWindow", "Image size", None, QtGui.QApplication.UnicodeUTF8))

from spectrochempy.extern.pyqtgraph.widgets.RawImageWidget import RawImageWidget
from spectrochempy.extern.pyqtgraph import SpinBox, GradientWidget, GraphicsView
