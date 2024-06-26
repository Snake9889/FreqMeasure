# This Python file uses the following encoding: utf-8

import os.path
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
from PyQt5.QtCore import pyqtSignal, QRectF, Qt, QSettings, QSize, QPoint
from PyQt5 import uic
import pyqtgraph as pg
from FreqMeasure.Modules.MainWindow.helpwidget import HelpWidget
from FreqMeasure.Modules.MainWindow.PhaseWidget.phasewidget import PhaseWidget
# from FreqMeasure.Modules.MainWindow.WaveletWidget.waveletwidget import WaveletWidget
from FreqMeasure.Modules.MainWindow.StatusWidget.statuswidget import StatusWidget


class MainWindow(QMainWindow):
    """   """
    region_changed = pyqtSignal(object)

    def __init__(self, data_source, data_proc_X, data_proc_Z, settings_control, bpm_name, parent=None):
        super().__init__(parent)

        ui_path = os.path.dirname(os.path.abspath(__file__))
        self.ui = uic.loadUi(os.path.join(ui_path, 'MainWindow.ui'), self)

        self.window_str = "None"
        self.scale_x = "None"
        self.scale_z = "None"
        self.bpm = bpm_name

        if self.bpm == "all":
            """ Replace one widget with another """
            old_statusWidget = self.statusWidget
            new_statusWidget = data_source.get_status_widget()
            new_statusWidget.setParent(self.centralwidget)

            self.ui.verticalLayout.replaceWidget(old_statusWidget, new_statusWidget)
            old_statusWidget.deleteLater()
            self.statusWidget = new_statusWidget

        else:
            """ Creating phase button """
            old_Widget = self.statusWidget
            self.phasebtn = QPushButton('Phase', self)
            self.phase_widget = PhaseWidget(os.path.join(ui_path))
            self.phasebtn.clicked.connect(self.phase_widget.show)
            self.ui.verticalLayout.replaceWidget(old_Widget, self.phasebtn)
            old_Widget.deleteLater()

        self.images_list = []
        self.sig_rect = None
        self.fx_rect = None
        self.i_rect = None
        self.fz_rect = None

        self.data_source = data_source
        self.data_proc_X = data_proc_X
        self.data_proc_Z = data_proc_Z
        self.settingsControl = settings_control

        self.data_proc_X.data_processed.connect(self.on_data2_ready)
        self.data_proc_Z.data_processed.connect(self.on_data3_ready)

        self.controlWidgetX.window_changed_str.connect(self.data_proc_X.on_wind_changed)
        self.controlWidgetX.filter_changed_str.connect(self.data_proc_X.on_filter_changed)
        self.controlWidgetX.groupBox.setTitle("X Controller")
        self.controlWidgetX.set_str_id("Data_X")
        self.controlWidgetX.scale_changed_obj.connect(self.on_scale_changing)

        self.controlWidgetZ.window_changed_str.connect(self.data_proc_Z.on_wind_changed)
        self.controlWidgetZ.filter_changed_str.connect(self.data_proc_Z.on_filter_changed)
        self.controlWidgetZ.groupBox.setTitle("Z Controller")
        self.controlWidgetZ.set_str_id("Data_Z")
        self.controlWidgetZ.scale_changed_obj.connect(self.on_scale_changing)

        self.controlWidgetX.method_changed_str.connect(self.data_proc_X.on_method_changed)
        self.controlWidgetX.boards_changed.connect(self.data_proc_X.on_boards_changed)

        self.controlWidgetZ.method_changed_str.connect(self.data_proc_Z.on_method_changed)
        self.controlWidgetZ.boards_changed.connect(self.data_proc_Z.on_boards_changed)

        self.actionSave.triggered.connect(self.on_save_button)
        self.actionRead.triggered.connect(self.on_read_button)

        self.actionExit.triggered.connect(self.on_exit_button)
        self.actionExit.triggered.connect(QApplication.instance().quit)

        self.help_widget = HelpWidget(os.path.join(ui_path, 'etc/icons/Help_1.png'))
        self.actionHelp.triggered.connect(self.help_widget.show)

        # self.wavelet_widget = WaveletWidget(os.path.join(ui_path))
        # self.waveletbtn.clicked.connect(self.wavelet_widget.show)

        self.controlWidgetX.boards_changed.connect(self.boards_X_changed)
        self.controlWidgetZ.boards_changed.connect(self.boards_Z_changed)

        self.ui.nu_x_label.setText('\u03BD<sub>x</sub> = ')
        self.ui.nu_z_label.setText('\u03BD<sub>z</sub> = ')

        self.plots_customization()

        self.data_curve11 = self.ui.plotSig.plot(pen='r', title='X_plot')
        self.data_curve12 = self.ui.plotSig.plot(pen='b', title='Z_plot')
        self.data_curve2 = self.ui.plotFX.plot(pen='r', title='Fourier Transform X_plot')
        self.data_curve3 = self.ui.plotI.plot(pen='k', title='I_plot')
        self.data_curve4 = self.ui.plotFZ.plot(pen='b', title='Fourier Transform Z_plot')

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
        label_str_i = "<span style=\"color:black;font-size:16px\">{}</span>"

        plot = self.ui.plotSig
        self.customize_plot(plot)
        self.customise_label(plot, pg.TextItem(), label_str_i.format("Sig"))

        plot = self.ui.plotI
        self.customize_plot(plot)
        self.customise_label(plot, pg.TextItem(), label_str_i.format("I"))

        plot = self.ui.plotFX
        self.customize_plot(plot)
        self.customise_label(plot, pg.TextItem(), label_str_x.format("Ax"))

        self.FX = pg.LinearRegionItem([self.controlWidgetX.lboard, self.controlWidgetX.rboard])
        self.FX.setBounds([0,0.5])
        plot.addItem(self.FX)
        self.FX.sigRegionChangeFinished.connect(self.region_X_changed)

        plot = self.ui.plotFZ
        self.customize_plot(plot)
        self.customise_label(plot, pg.TextItem(), label_str_z.format("Az"))

        self.FZ = pg.LinearRegionItem([self.controlWidgetZ.lboard, self.controlWidgetZ.rboard])
        self.FZ.setBounds([0,0.5])
        plot.addItem(self.FZ)
        self.FZ.sigRegionChangeFinished.connect(self.region_Z_changed)

        """ Here can be the cross-marker on plots """
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
            self.scale_x = scale
            self.plot_mode(self.ui.plotFX, self.scale_x)
        elif control_widget.str_id == "Data_Z":
            self.scale_z = scale
            self.plot_mode(self.ui.plotFZ, self.scale_z)
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
        self.controlWidgetX.on_boards_changed_ext(self.FX.getRegion())

    def region_Z_changed(self):
        """   """
        self.controlWidgetZ.on_boards_changed_ext(self.FZ.getRegion())

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
        self.data_curve11.setData(data_source.dataT, data_source.dataX)
        self.data_curve12.setData(data_source.dataT, data_source.dataZ)
        self.sig_rect = self.ui.plotSig.viewRange()

    def on_data4_ready(self, data_source):
        """   """
        self.data_curve3.setData(data_source.dataT, data_source.dataI)
        self.i_rect = self.ui.plotI.viewRange()

    def on_data2_ready(self, data_processor):
        """   """
        self.data_curve2.setData(data_processor.fftwT, data_processor.fftw_to_process)
        self.fx_rect = self.ui.plotFX.viewRange()

    def on_data3_ready(self, data_processor):
        """   """
        self.data_curve4.setData(data_processor.fftwT, data_processor.fftw_to_process)
        self.fz_rect = self.ui.plotFZ.viewRange()

    def on_freq_status_X(self, data_processor):
        """   """
        if data_processor.warning == 0:
            self.ui.frq_x.setText('{:.5f}'.format(data_processor.frq_founded))
        elif data_processor.warning == 1:
            self.ui.frq_x.setText(data_processor.warningText)
        else:
            self.ui.frq_x.setText('Unexpected value!')

    def on_freq_status_Z(self, data_processor):
        """   """
        if data_processor.warning == 0:
            self.ui.frq_z.setText('{:.5f}'.format(data_processor.frq_founded))
        elif data_processor.warning == 1:
            self.ui.frq_z.setText(data_processor.warningText)
        else:
            self.ui.frq_z.setText('Unexpected value!')

    def on_phase_status_X(self, data_processor):
        """   """
        if self.bpm == "all":
            pass
        else:
            self.phase_widget.phase_plot_X(data_processor)

    def on_phase_status_Z(self, data_processor):
        """   """
        if self.bpm == "all":
            pass
        else:
            self.phase_widget.phase_plot_Z(data_processor)

    def on_wavelet_data_ready_X(self, data_source):
        """   """
        if self.bpm == "all":
            pass
        else:
            self.wavelet_widget.wavelet_plot_X(data_source)

    def on_wavelet_data_ready_Z(self, data_source):
        """   """
        if self.bpm == "all":
            pass
        else:
            self.wavelet_widget.wavelet_plot_Z(data_source)

    def save_settings(self):
        """   """
        settings = QSettings()
        settings.beginGroup(self.bpm)
        settings.beginGroup("Plots")
        settings.setValue("sig_zoom", self.sig_rect)
        settings.setValue("i_zoom", self.i_rect)
        settings.setValue("scale_x", self.scale_x)
        settings.setValue("scale_z", self.scale_z)
        settings.setValue("fx_zoom", self.fx_rect)
        settings.setValue("fz_zoom", self.fz_rect)
        settings.setValue('size', self.size())
        settings.setValue('pos', self.pos())
        settings.endGroup()
        settings.endGroup()
        settings.sync()

    def read_settings(self):
        """   """
        rect_def = [[0, 0.5], [0, 1]]
        settings = QSettings()
        settings.beginGroup(self.bpm)
        settings.beginGroup("Plots")
        self.sig_rect = settings.value("sig_zoom", rect_def)
        self.i_rect = settings.value("i_zoom", rect_def)
        self.scale_x = settings.value("scale_x", "Normal")
        self.scale_z = settings.value("scale_z", "Normal")
        self.fx_rect = settings.value("fx_zoom", rect_def)
        self.fz_rect = settings.value("fz_zoom", rect_def)
        self.resize(settings.value('size', QSize(500, 500)))
        self.move(settings.value('pos', QPoint(60, 60)))
        settings.endGroup()
        settings.endGroup()

        self.plot_mode(self.ui.plotFX, self.scale_x)
        self.plot_mode(self.ui.plotFZ, self.scale_z)

        self.ui.plotSig.setRange(xRange=self.sig_rect[0], yRange=self.sig_rect[1])
        self.ui.plotI.setRange(xRange=self.i_rect[0], yRange=self.i_rect[1])

        self.ui.plotFX.setRange(xRange=self.fx_rect[0], yRange=self.fx_rect[1])
        if self.scale_z == "Log_Y":
            self.ui.plotFZ.setRange(xRange=self.fz_rect[0], yRange=list(map(lambda x:pow(10,x), self.fz_rect[1])))
        else:
            self.ui.plotFZ.setRange(xRange=self.fz_rect[0], yRange=self.fz_rect[1])

