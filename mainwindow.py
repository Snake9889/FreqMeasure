# This Python file uses the following encoding: utf-8

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

        ui_path = os.path.dirname(os.path.abspath(__file__))
        self.ui = uic.loadUi(os.path.join(ui_path, 'MainWindow.ui'), self)

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

        self.buttonRead.clicked.connect(self.on_read_button)
        self.buttonSave.clicked.connect(self.on_save_button)

        self.plots_customization()

        self.controlWidgetX.boards_changed.connect(self.boards_X_changed)
        self.controlWidgetZ.boards_changed.connect(self.boards_Z_changed)

        self.data_curve1 = self.ui.plotX.plot(pen='r', title='Generated signal X_plot')
        self.data_curve2 = self.ui.plotFX.plot(pen='r', title='Fourier Transform X_plot')
        self.data_curve3 = self.ui.plotZ.plot(pen='b', title='Generated signal Z_plot')
        self.data_curve4 = self.ui.plotFZ.plot(pen='b', title='Fourier Transform Z_plot')

    def plots_customization(self):
        """   """
        label_str_x = "<span style=\"color:red;font-size:16px\">{}</span>"
        label_str_z = "<span style=\"color:blue;font-size:16px\">{}</span>"

        self.ui.plotX.setLabel('left', label_str_x.format("X"))
        self.customize_plot(self.ui.plotX)
        self.ui.plotX.setYRange(-4, 4)

        self.ui.plotFX.setTitle(label_str_x.format("Ax"))
        self.ui.plotFX.setYRange(0, 0.8, padding=0)
        self.FX = pg.LinearRegionItem([self.controlWidgetX.lboard, self.controlWidgetX.rboard])
        self.ui.plotFX.addItem(self.FX)
        self.FX.sigRegionChangeFinished.connect(self.region_X_changed)
        self.customize_plot(self.ui.plotFX)

        # vLine = pg.InfiniteLine(angle=90, movable=False)
        # hLine = pg.InfiniteLine(angle=0, movable=False)
        # p1.addItem(vLine, ignoreBounds=True)
        # p1.addItem(hLine, ignoreBounds=True)
        # vb = p1.vb

    # def mouseMoved(evt):
        # pos = evt[0]  ## using signal proxy turns original arguments into a tuple
        # if p1.sceneBoundingRect().contains(pos):
            # mousePoint = vb.mapSceneToView(pos)
            # index = int(mousePoint.x())
            # if index > 0 and index < len(data1):
                # label.setText("<span style='font-size: 12pt'>x=%0.1f,   <span style='color: red'>y1=%0.1f</span>,   <span style='color: green'>y2=%0.1f</span>" % (mousePoint.x(), data1[index], data2[index]))
            # vLine.setPos(mousePoint.x())


        self.ui.plotZ.setLabel('left', label_str_z.format("Z"))
        self.ui.plotZ.setYRange(-2, 2)
        self.customize_plot(self.ui.plotZ)

        self.ui.plotFZ.setTitle(label_str_z.format("Az"))
        self.ui.plotFZ.setYRange(0, 0.4)
        self.FZ = pg.LinearRegionItem([self.controlWidgetZ.lboard, self.controlWidgetZ.rboard])
        self.ui.plotFZ.addItem(self.FZ)
        self.FZ.sigRegionChangeFinished.connect(self.region_Z_changed)
        self.customize_plot(self.ui.plotFZ)

    @staticmethod
    def customize_plot(plot):
        """   """
        plot.setBackground('w')
        plot.showAxis('top')
        plot.showAxis('right')
        plot.getAxis('top').setStyle(showValues=False)
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

    @staticmethod
    def plot_mode(plot, scale):
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
        #x1 = float(self.FX.getRegion()[0])
        #x2 = float(self.FX.getRegion()[1])
        # x1 = float(self.controlWidgetX.boards[0])
        # x2 = float(self.controlWidgetX.boards[1])
        # self.controlWidgetX.rboardSBox.setValue(max(x1, x2))
        # self.controlWidgetX.lboardSBox.setValue(min(x1, x2))

        self.controlWidgetX.boards = self.FX.getRegion()
        print(self.controlWidgetX.boards)

    def region_Z_changed(self):
        """   """
        self.controlWidgetZ.boards = self.FZ.getRegion()
        print(self.controlWidgetZ.boards)

        # x1 = float(self.controlWidgetZ.boards[0])
        # x2 = float(self.controlWidgetZ.boards[1])
        #
        # self.controlWidgetZ.rboardSBox.setValue(max(x1, x2))
        # self.controlWidgetZ.lboardSBox.setValue(min(x1, x2))

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
        """   """
        if data_processor.warning == 0:
            self.ui.frq_x.setText('\u03BD<sub>x</sub> = {}'.format(data_processor.frq_founded))
        elif data_processor.warning == 1:
            self.ui.frq_x.setText(data_processor.warningText)
        else:
            self.ui.frq_x.setText('Warning number has unexpected value!')

    def on_freq_status_Z(self, data_processor):
        """   """
        if data_processor.warning == 0:
            self.ui.frq_z.setText('\u03BD<sub>z</sub> = {}'.format(data_processor.frq_founded))
        elif data_processor.warning == 1:
            self.ui.frq_z.setText(data_processor.warningText)
        else:
            self.ui.frq_z.setText('Warning number has unexpected value!')

# if __name__ == "__main__":
#     app = QApplication([])
#     window = MainWindow()
#     window.show()
#     sys.exit(app.exec_())
