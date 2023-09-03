# This Python file uses the following encoding: utf-8

from PyQt5.QtCore import QCoreApplication, QSettings, QSize
from PyQt5.QtGui import QIcon
import signal
from FreqMeasure.Modules.MainWindow.mainwindow import *
from FreqMeasure.Modules.dataprocessor import DataProcessor
from FreqMeasure.Modules.settingscontrol import SettingsControl
from FreqMeasure.Modules.command_parser import TerminalParser
from FreqMeasure.Modules.DataSources.datasources_all import BPMDataAll
import FreqMeasure.Modules.DataSources.datasources_bpm as ds_bpm
import FreqMeasure.Modules.DataSources.datasources as ds_model

pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')

# Allow CTRL+C and/or SIGTERM to kill us (PyQt blocks it otherwise)
signal.signal(signal.SIGINT, signal.SIG_DFL)
signal.signal(signal.SIGTERM, signal.SIG_DFL)

if __name__ == "__main__":
    """   """
    import sys

    QCoreApplication.setOrganizationName("Denisov")
    QCoreApplication.setApplicationName("BTMS")
    QSettings.setDefaultFormat(QSettings.IniFormat)

    app = QApplication(sys.argv)
    app.setStyle('Cleanlooks')

    argument_parser = TerminalParser()
    bpm_name_parsed = argument_parser.bpm_name_parsed
    data_source = None

    if bpm_name_parsed == "model":
        data_source = ds_model.BPMData()

    elif bpm_name_parsed == "all":
        data_source = BPMDataAll()

    else:
        data_source = ds_bpm.BPMData(bpm_name=bpm_name_parsed)

    if data_source is None:
        print("Data source doesn't exists!!! You can't use this program!!!")
        exit()

    data_proc_X = DataProcessor("X")
    data_proc_Z = DataProcessor("Z")
    settingsControl = SettingsControl()

    mw = MainWindow(data_source, data_proc_X, data_proc_Z, settingsControl, bpm_name_parsed)
    mw.setWindowTitle('BTMS ({})'.format(bpm_name_parsed))

    icon_path = os.path.dirname(os.path.abspath(__file__))
    mw_icon = QIcon()
    mw_icon.addFile(os.path.join(icon_path, 'etc/icons/app_icon_color.png'), QSize(32, 32))
    mw.setWindowIcon(mw_icon)

    data_source.data_ready.connect(mw.on_data1_ready)
    data_source.data_ready.connect(mw.on_data4_ready)
    data_source.data_ready.connect(data_proc_X.on_data_recv)
    data_source.data_ready.connect(data_proc_Z.on_data_recv)


    settingsControl.add_object(mw)
    settingsControl.add_object(mw.controlWidgetX)
    settingsControl.add_object(mw.controlWidgetZ)
    settingsControl.add_object(data_source)
    settingsControl.read_settings()

    data_proc_X.data_processed.connect(mw.on_freq_status_X)
    data_proc_Z.data_processed.connect(mw.on_freq_status_Z)
    data_proc_X.data_processed.connect(mw.on_phase_status_X)
    data_proc_Z.data_processed.connect(mw.on_phase_status_Z)

    mw.controlWidgetX.signature.connect(data_source.force_data_ready)
    mw.controlWidgetZ.signature.connect(data_source.force_data_ready)

    mw.show()
    print(mw.scale_x, mw.scale_z, mw.fx_rect, mw.fz_rect)
    sys.exit(app.exec_())
