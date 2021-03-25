# This Python file uses the following encoding: utf-8
#

from PyQt5.QtCore import QCoreApplication, QSettings
import signal
import pyqtgraph as pg
from mainwindow import *

from dataprocessor import DataProcessor
from settingscontrol import SettingsControl
from controlwidget import ControlWidget
from command_parser import TerminalParser

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
    
    argument_parser = TerminalParser()
    bpm_name_parsed = argument_parser.bpm_name_parsed
    simulate_data = 0
    data_source = None

    if simulate_data:
        from datasources import BPMData
        data_source = BPMData(2048)
    else:
        from datasources_bpm import BPMData
        data_source = BPMData(bpm_name = bpm_name_parsed)

    if data_source is None:
        print("Fucking data source!!!")
        exit()
    
    data_proc_X = DataProcessor("X")
    data_proc_Z = DataProcessor("Z")
    settings_control = SettingsControl()
    mw = MainWindow(data_source, data_proc_X, data_proc_Z, settings_control)
    
    
    data_source.data_ready.connect(mw.on_data1_ready)
    data_source.data_ready.connect(mw.on_data3_ready)
    data_source.data_ready.connect(data_proc_X.on_data_recv)
    data_source.data_ready.connect(data_proc_Z.on_data_recv)


    mw.show()
    sys.exit(app.exec_())
