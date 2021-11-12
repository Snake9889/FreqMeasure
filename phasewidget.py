import sys
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtCore import QSize, QCoreApplication
from PyQt5.QtGui import QPixmap, QIcon
import os.path


class PhaseWidget(QWidget):
    """   """
    def __init__(self, file_name):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.setMinimumSize(300,300)
        self.setGeometry(300, 300, 600, 500)
        self.setWindowTitle('Phase')

        #win = pg.GraphicsWindow(title="Basic plotting examples")
        pg.setConfigOptions(antialias=True)
        pw = pg.PlotWidget()
        
        #p2 = win.addPlot(title="Multiple curves")
        
        #self.data_curve_1 = PlotWidget()
            #self.show()
        icon_path = os.path.dirname(os.path.abspath(__file__))
        help_icon = QIcon()
        help_icon.addFile(os.path.join(icon_path, 'etc/icons/Psi.png'), QSize(32, 32))
        self.setWindowIcon(help_icon)

    def calculations(self):
        pass
    

        # pixmap = QPixmap(file_name)
        # self.label.setPixmap(pixmap)
        # self.resize(pixmap.width(), pixmap.height())
        #self.show()
