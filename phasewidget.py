import sys
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtCore import QSize, QCoreApplication
from PyQt5.QtGui import QPixmap, QIcon
import os.path
from PyQt5 import uic

class PhaseWidget(QWidget):
    """   """
    def __init__(self, file_name):
        super(PhaseWidget, self).__init__()
        ui_path = os.path.dirname(os.path.abspath(__file__))
        self.ui = uic.loadUi(os.path.join(ui_path, 'PhaseWidget.ui'), self)

        icon_path = os.path.dirname(os.path.abspath(__file__))
        phase_icon = QIcon()
        phase_icon.addFile(os.path.join(icon_path, 'etc/icons/Psi.png'), QSize(32, 32))
        self.setWindowIcon(phase_icon)
        self.setWindowTitle('Phase')

        self.plots_customization()
        self.data_curve_X = self.ui.PhaseX.plot(pen='r', title='X_phase')
        self.data_curve_Z = self.ui.PhaseZ.plot(pen='b', title='Z_phase')

    @staticmethod
    def customise_label(plot, text_item, html_str):
        """   """
        plot_vb = plot.getViewBox()
        text_item.setHtml(html_str)
        text_item.setParentItem(plot_vb)

    def plots_customization(self):
        """   """
        label_str_x = "<span style=\"color:red; font-size:16px\">{}</span>"
        label_str_z = "<span style=\"color:blue;font-size:16px\">{}</span>"

        plot = self.ui.PhaseX
        self.customize_plot(plot)
        self.customise_label(plot, pg.TextItem(), label_str_x.format("X"))

        plot = self.ui.PhaseZ
        self.customize_plot(plot)
        self.customise_label(plot, pg.TextItem(), label_str_z.format("Z"))

    @staticmethod
    def customize_plot(plot):
        """   """
        plot.setBackground('w')
        plot.showAxis('top')
        plot.showAxis('right')
        plot.getAxis('top').setStyle(showValues=False)
        plot.getAxis('right').setStyle(showValues=False)
        plot.showGrid(x=True, y=True)

    def phase_plot_X(self, data_processor):
        """   """
        self.data_curve_X.setData(data_processor.dataX[0:len(data_processor.momentum)], data_processor.momentum)
        #self.fx_rect = self.ui.PhaseX.viewRange()

    def phase_plot_Z(self, data_processor):
        """   """
        self.data_curve_Z.setData(data_processor.dataZ[0:len(data_processor.momentum)], data_processor.momentum)
        #self.fz_rect = self.ui.PhaseZ.viewRange()
