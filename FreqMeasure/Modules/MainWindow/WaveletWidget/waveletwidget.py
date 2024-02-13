import pyqtgraph as pg
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QSize, pyqtSignal
from PyQt5.QtGui import QIcon
import os.path
import pywt
import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import numpy as np

class MplFig(FigureCanvasQTAgg):
    """   """
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplFig, self).__init__(fig)


class WaveletWidget(QWidget):
    """   """
    wavelet_changed_str = pyqtSignal(str)

    def __init__(self, file_name):
        super(WaveletWidget, self).__init__()
        ui_path = os.path.dirname(os.path.abspath(__file__))
        self.ui = uic.loadUi(os.path.join(ui_path, 'WaveletWidget.ui'), self)

        icon_path = os.path.dirname(os.path.abspath(__file__))
        phase_icon = QIcon()
        phase_icon.addFile(os.path.join(icon_path, 'etc/icons/Psi.png'), QSize(32, 32))
        self.setWindowIcon(phase_icon)
        self.setWindowTitle('Wavelet')

        self.ui.WaveletX = self.widgets_replaced(self.ui.WaveletX)
        self.ui.WaveletZ = self.widgets_replaced(self.ui.WaveletZ)

        self.wavelet = "mexh"
        self.dataT = None
        self.dataWX = None
        self.dataFX = None
        self.dataWZ = None
        self.dataFZ = None

    def widgets_replaced(self, widget):
        """   """
        old_Widget = widget
        widget = MplFig(self, width=5, height=4, dpi=100)
        self.ui.verticalLayout.replaceWidget(old_Widget, widget)
        old_Widget.deleteLater()
        return widget

    def on_wavelet_checked(self, state):
        """   """
        if state == 0:
            self.wavelet = "mexh"
        elif state == 1:
            self.wavelet = "cmorl"
        elif state == 2:
            self.wavelet = "gausP"
        else:
            self.wavelet = "mexh"

        self.wavelet_changed_str.emit(self.wavelet)

    def wavelet_plot_X(self, data_source):
        """   """
        widget = self.ui.WaveletX
        title = 'Wavelet Transform of X-signal'
        cmap = plt.cm.seismic

        self.dataT, self.dataWX, self.dataFX = self.cwt_analysis(data_source.dataT, data_source.dataX)

        self.update_plot(widget, self.dataT, self.dataWX, self.dataFX, cmap, title)


    def wavelet_plot_Z(self, data_source):
        """   """
        widget = self.ui.WaveletZ
        title = 'Wavelet Transform of Z-signal'
        cmap = 'jet'

        self.dataT, self.dataWZ, self.dataFZ = self.cwt_analysis(data_source.dataT, data_source.dataZ)

        self.update_plot(widget, self.dataT, self.dataWZ, self.dataFZ, cmap, title)
        # widget.axes.contourf(self.dataT, self.dataFZ, np.log2((abs(self.dataWZ))**2),
        #                       cmap=cmap, levels=40)

        # widget.axes.set_title('Wavelet Transform (Power Spectrum) of signal-Z', fontsize=15)
        # widget.axes.set_ylabel('Frequency', fontsize=13)
        # widget.axes.set_xlabel('Turnover', fontsize=13)

    def update_plot(self, widget, dataT, dataW, dataF, cmap, title):

        widget.axes.cla()
        widget.axes.contourf(dataT, dataF, abs(dataW),
                             cmap=cmap, levels=5)
        widget.axes.set_title(title, fontsize=15)
        widget.axes.set_ylabel('Frequency', fontsize=13)
        # widget.axes.set_xlabel('Turnover', fontsize=13)
        widget.draw()

    def cwt_analysis(self, dataT, dataXZ):
        """   """
        dt = 1/len(dataT)
        frqs = np.fft.rfftfreq(len(dataT), 1.0)[int(len(dataT)/10):int(len(dataT)/5)]
        scales = pywt.frequency2scale('mexh', frqs)
        [coefficients, frequencies] = pywt.cwt(dataXZ, scales, self.wavelet, dt)

        return dataT, coefficients, frqs


