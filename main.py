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
    data_source = None
    #simulate_data = 0

    #if simulate_data:
    #    from datasources import BPMData
    #    data_source = BPMData(2048)

    if bpm_name_parsed == "model":
        from datasources import BPMData
        data_source =  BPMData(2048)

    else:
        from datasources_bpm import BPMData
        data_source = BPMData(bpm_name = bpm_name_parsed)

    if data_source is None:
        print("Data source doesn't exists!!! You can't use this program!!!")
        exit()

    data_proc_X = DataProcessor("X")
    data_proc_Z = DataProcessor("Z")
    settingsControl = SettingsControl()
    mw = MainWindow(data_source, data_proc_X, data_proc_Z, settingsControl)

    data_source.data_ready.connect(mw.on_data1_ready)
    data_source.data_ready.connect(mw.on_data3_ready)
    data_source.data_ready.connect(data_proc_X.on_data_recv)
    data_source.data_ready.connect(data_proc_Z.on_data_recv)

    #self.settingsControl = settings_control
    settingsControl.add_object(mw.controlWidgetX)
    settingsControl.add_object(mw.controlWidgetZ)
    #self.buttonRead.clicked.connect(mw.on_read_button)
    #self.buttonSave.clicked.connect(mw.on_save_button)
    settingsControl.read_settings()

    data_proc_X.data_processed.connect(mw.on_freq_status_X)
    data_proc_Z.data_processed.connect(mw.on_freq_status_Z)


    mw.show()
    sys.exit(app.exec_())
