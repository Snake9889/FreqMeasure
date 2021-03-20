# This Python file uses the following encoding: utf-8
#

from PyQt5.QtCore import QCoreApplication, QSettings
import signal
import pyqtgraph as pg
from mainwindow import *

#from datasources import BPMData
from datasources_bpm import BPMData

from dataprocessor import DataProcessor
from settingscontrol import SettingsControl
from controlwidget import ControlWidget

pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')


# Allow CTRL+C and/or SIGTERM to kill us (PyQt blocks it otherwise)
signal.signal(signal.SIGINT, signal.SIG_DFL)
signal.signal(signal.SIGTERM, signal.SIG_DFL)

if __name__ == "__main__":
    """   """
    import sys

    QCoreApplication.setOrganizationName("Denisov")
    QCoreApplication.setApplicationName("Freq_Online")
    QSettings.setDefaultFormat(QSettings.IniFormat)

    app = QApplication(sys.argv)
    
    # argument parser....

    data_source = BPMData(1024)
#    data_proc_X = DataProcessor("X")
#    data_proc_Z = DataProcessor("Z")

    mw = MainWindow(data_source)

    mw.show()
    sys.exit(app.exec_())
