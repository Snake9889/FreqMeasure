from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
import os.path
from PyQt5 import uic
from scipy.spatial import distance
import numpy as np

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

        self.X_sort = None
        self.PX_sort = None
        self.Z_sort = None
        self.PZ_sort = None

        self.plots_customization()
        self.data_curve_X = self.ui.PhaseX.scatterPlot(pen='k', title='X_phase', symbol='o', size=3, brush='r')
        self.data_curve_Z = self.ui.PhaseZ.scatterPlot(pen='k', title='Z_phase', symbol='o', size=3, brush='b')

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
        #self.PhaseX.setXRange(-6, 6)
        #self.PhaseX.setYRange(-6, 6)
        self.PhaseX.setAspectLocked(True)

        plot = self.ui.PhaseZ
        self.customize_plot(plot)
        self.customise_label(plot, pg.TextItem(), label_str_z.format("Z"))
        #self.PhaseZ.setXRange(-2, 4)
        #self.PhaseZ.setYRange(-1, 3)
        self.PhaseZ.setAspectLocked(True)

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
        self.X_sort, self.PX_sort = self.reduction(data_processor.dataX_averaged[0:len(data_processor.momentum)], data_processor.momentum)
        self.data_curve_X.setData(self.X_sort, self.PX_sort)

    def phase_plot_Z(self, data_processor):
        """   """
        self.Z_sort, self.PZ_sort = self.reduction(data_processor.dataZ_averaged[0:len(data_processor.momentum)], data_processor.momentum)
        self.data_curve_Z.setData(self.Z_sort, self.PZ_sort)
        #self.data_curve_Z.setData(data_processor.dataZ_averaged[0:len(data_processor.momentum)], data_processor.momentum)

    def reduction(self, M1, M2):
        """   """
        Mas = np.zeros(len(M2))
        for i in range(len(M2)):
            Mas[i] = distance.euclidean([0, 0], [M1[i], M2[i]])

        if len(M2) >= 500:
            border = int(1 * len(M2))
        else:
            border = 100

        indecies = np.zeros(border)
        MasCoord = np.zeros(border)
        MasP = np.zeros(border)
        indecies = np.argsort(Mas)[-border:]
        for i in range (0, border):
            MasCoord[i] = M1[indecies[i]]
            MasP[i] = M2[indecies[i]]
        return MasCoord, MasP

