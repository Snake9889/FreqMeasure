# This Python file uses the following encoding: utf-8

import sys
import os.path

from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import pyqtSignal
from PyQt5 import uic
import pyqtgraph as pg

class MainWindow(QMainWindow):
    """   """

    region_changed = pyqtSignal(object)

    def __init__(self, data_source, data_proc_X, data_proc_Z, settings_control):
        super(MainWindow, self).__init__()

        #self.ui = uic.loadUi(os.path.join(os.path.relpath('MainWindow_New.ui'), 'MainWindow_New.ui'), self)
        #self.ui = uic.loadUi((os.path.realpath('MainWindow_New.ui'), self)
        #self.ui = uic.loadUi('MainWindow_New.ui', self)

        ui_path = os.path.dirname(os.path.abspath(__file__))
        self.ui = uic.loadUi(os.path.join(ui_path, 'MainWindow_New.ui'),self)

        #self.setWindowTitle('FrqM {}'.format(data_processor.frq_founded))
        self.window_str = "None"
        self.frq_founded = 0.0

        self.data_source = data_source

        self.data_proc_X = data_proc_X
        self.data_proc_Z = data_proc_Z

        self.settingsControl = settings_control

        self.buttonExit.clicked.connect(self.on_exit_button)
        self.buttonExit.clicked.connect(QApplication.instance().quit)

        self.data_proc_X.data_processed.connect(self.on_data2_ready)
        self.data_proc_Z.data_processed.connect(self.on_data4_ready)

        self.controlWidgetX.window_changed_str.connect(self.data_proc_X.on_wind_changed)
        self.controlWidgetX.groupBox.setTitle("X Controller")
        self.controlWidgetX.set_str_id("Data_X")
        self.controlWidgetX.scale_changed_obj.connect(self.on_scale_changing)

        self.controlWidgetZ.window_changed_str.connect(self.data_proc_Z.on_wind_changed)
        self.controlWidgetZ.groupBox.setTitle("Z Controller")
        self.controlWidgetZ.set_str_id("Data_Z")
        self.controlWidgetZ.scale_changed_obj.connect(self.on_scale_changing)

        self.controlWidgetX.method_changed_str.connect(self.data_proc_X.on_method_changed)
        self.controlWidgetX.boards_changed.connect(self.data_proc_X.on_boards_changed)

        self.controlWidgetZ.method_changed_str.connect(self.data_proc_Z.on_method_changed)
        self.controlWidgetZ.boards_changed.connect(self.data_proc_Z.on_boards_changed)

        #self.settingsControl = settings_control
        #self.settingsControl.add_object(self.controlWidgetX)
        #self.settingsControl.add_object(self.controlWidgetZ)
        self.buttonRead.clicked.connect(self.on_read_button)
        self.buttonSave.clicked.connect(self.on_save_button)
        #self.settingsControl.read_settings()

        self.plots_customization()

        self.controlWidgetX.boards_changed.connect(self.boards_X_changed)
        self.controlWidgetZ.boards_changed.connect(self.boards_Z_changed)


        self.data_curve1 = self.ui.plotX.plot(pen = 'r', title = 'Generated signal X_plot')
        self.data_curve2 = self.ui.plotFX.plot(pen = 'r', title = 'Fourier Transform X_plot')
        self.data_curve3 = self.ui.plotZ.plot(pen = 'b', title='Generated signal Z_plot')
        self.data_curve4 = self.ui.plotFZ.plot(pen = 'b', title='Fourier Transform Z_plot')

    def plots_customization(self):
        """   """
        label_str_x = "<span style=\"color:red;font-size:16px\">{}</span>"
        label_str_z = "<span style=\"color:blue;font-size:16px\">{}</span>"

        self.ui.plotX.setLabel('left', label_str_x.format("X"))
        self.customize_plot(self.ui.plotX)
        self.ui.plotX.setYRange(-4, 4)

        self.ui.plotFX.setLabel('left',label_str_x.format("Ax"))
        self.ui.plotFX.setYRange(0, 0.8, padding =0)
        self.FX = pg.LinearRegionItem([self.controlWidgetX.lboard, self.controlWidgetX.rboard])
        self.ui.plotFX.addItem(self.FX)
        self.FX.sigRegionChangeFinished.connect(self.region_X_changed)
        self.customize_plot(self.ui.plotFX)

        self.ui.plotZ.setLabel('left', label_str_z.format("Z"))
        self.ui.plotZ.setYRange(-2, 2)
        self.customize_plot(self.ui.plotZ)

        #self.ui.plotFZ.setLabel('left', label_str_z.format("Az"))
        self.ui.plotFZ.setTitle(label_str_z.format("Az"))
        self.ui.plotFZ.setYRange(0, 0.4)
        self.FZ = pg.LinearRegionItem([self.controlWidgetZ.lboard, self.controlWidgetZ.rboard])
        self.ui.plotFZ.addItem(self.FZ)
        self.FZ.sigRegionChangeFinished.connect(self.region_Z_changed)
        self.customize_plot(self.ui.plotFZ)

    def customize_plot(self, plot):
        """   """
        plot.setBackground('w')
        plot.showAxis('top')
        plot.showAxis('right')
        plot.getAxis('top').setStyle(showValues = False)
        plot.getAxis('right').setStyle(showValues=False)
        plot.showGrid(x=True, y=True)

    def on_scale_changing(self, control_widget):
        """   """
        scale = control_widget.scale
        if control_widget.str_id == "Data_X":
            self.plot_mode(self.ui.plotFX, scale)
        elif control_widget.str_id == "Data_Z":
            self.plot_mode(self.ui.plotFZ, scale)
        else:
            print("Error in control_widget!")

    def plot_mode(self, plot, scale):
        """   """
        if scale == "Normal":
            plot.setLogMode(False, False)
        if scale == 'Log_Y':
            plot.setLogMode(False, True)


    def boards_X_changed(self, dict):
        """   """
        self.FX.setRegion([dict.get("lboard", 0.1), dict.get("rboard", 0.5)])

    def boards_Z_changed(self, dict):
        """   """
        self.FZ.setRegion([dict.get("lboard", 0.1), dict.get("rboard", 0.5)])

    def region_X_changed(self):
        """   """
        self.controlWidgetX.boards = self.FX.getRegion()
        print(self.controlWidgetX.boards)

        x1=float(self.controlWidgetX.boards[0])
        x2=float(self.controlWidgetX.boards[1])

        self.controlWidgetX.lboardSBox.setValue(min(x1,x2))
        self.controlWidgetX.rboardSBox.setValue(max(x1,x2))

    def region_Z_changed(self):
        """   """
        self.controlWidgetZ.boards = self.FZ.getRegion()
        print(self.controlWidgetZ.boards)

        x1=float(self.controlWidgetZ.boards[0])
        x2=float(self.controlWidgetZ.boards[1])

        self.controlWidgetZ.lboardSBox.setValue(min(x1,x2))
        self.controlWidgetZ.rboardSBox.setValue(max(x1,x2))

    def on_exit_button(self):
        """   """
        print(self, ' Exiting... Bye...')

    def on_read_button(self):
        """   """
        self.settingsControl.read_settings()

    def on_save_button(self):
        """   """
        self.settingsControl.save_settings()

    def on_data1_ready(self, data_source):
        """   """
        self.data_curve1.setData(data_source.dataT, data_source.dataX)

    def on_data3_ready(self, data_source):
        """   """
        self.data_curve3.setData(data_source.dataT, data_source.dataZ)

    def on_data2_ready(self, data_processor):
        """   """
        self.data_curve2.setData(data_processor.fftwT, data_processor.fftw_to_process)

    def on_data4_ready(self, data_processor):
        """   """
        self.data_curve4.setData(data_processor.fftwT, data_processor.fftw_to_process)

    def on_freq_status_X(self, data_processor):
        if data_processor.warning == 0:
            self.ui.frq_x.setText('Frequency_X = {}'.format(data_processor.frq_founded))
        elif data_processor.warning == 1:
            self.ui.frq_x.setText(data_processor.warningText)
        else:
            self.ui.frq_x.setText('Warning number has unexpected value!')

        freq_textX = '{:7.6f}'.format(data_processor.frq_founded)
        #self.ui.freq_showX.display(freq_textX)

    def on_freq_status_Z(self, data_processor):
        if data_processor.warning == 0:
            self.ui.frq_z.setText('Frequency_Z = {}'.format(data_processor.frq_founded))
        elif data_processor.warning == 1:
            self.ui.frq_z.setText(data_processor.warningText)
        else:
            self.ui.frq_z.setText('Warning number has unexpected value!')

        freq_textZ = '{:7.6f}'.format(data_processor.frq_founded)
        #self.ui.freq_showZ.display(freq_textZ)


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
