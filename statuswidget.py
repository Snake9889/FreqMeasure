# -*- coding: utf-8 -*-

from PyQt5.QtCore import pyqtSignal, Qt, QSettings
from PyQt5.QtWidgets import QWidget
from PyQt5 import uic
from command_parser import TerminalParser
import os.path


class StatusWidget(QWidget):
    """   """
    # window_changed_str = pyqtSignal(str)
    # method_changed_str = pyqtSignal(str)
    # boards_changed = pyqtSignal(object)
    # scale_changed_obj = pyqtSignal(object)
    # signature = pyqtSignal(bool)

    # default_str_id = "Warning"

    def __init__(self, parent=None):
        super(StatusWidget, self).__init__(parent)

        ui_path = os.path.dirname(os.path.abspath(__file__))
        self.ui = uic.loadUi(os.path.join(ui_path, 'StatusWidget.ui'), self)

        # argument_parser = TerminalParser()

        # self.window = "None"
        # self.method = argument_parser.method_name_parsed
        # self.bpm = argument_parser.bpm_name_parsed
        # self.boards = None
        # self.lboard = 0.01
        # self.rboard = 0.5
        # self.scale = "None"

        # self.str_id = self.default_str_id

        # buttons = [
            # self.usePeakBtn,
            # self.useGassiorBtn,
            # self.useNaffBtn,
        # ]

        # id = 1
        # for btn in buttons:
            # btn.setStyleSheet("QPushButton {background-color: none}"
                              # "QPushButton:checked {background-color: green}")
            # self.buttonGroup.setId(btn, id)
            # id = id + 1

        # self.lboardSBox.setValue(0.05)
        # self.rboardSBox.setValue(0.3)

        # self.checkWindowBox.currentIndexChanged.connect(self.on_window_checked)
        # self.buttonGroup.buttonClicked['int'].connect(self.on_method_checked)
        # self.lboardSBox.valueChanged.connect(self.on_lboardsbox_changed)
        # self.rboardSBox.valueChanged.connect(self.on_rboardsbox_changed)
        # self.log_mod.stateChanged.connect(self.on_plot_checked)

    # def on_window_checked(self, state):
        # """   """
        # if state == 0:
            # self.window = "None"
        # elif state == 1:
            # self.window = "Hann"
        # elif state == 2:
            # self.window = "Hamming"
        # else:
            # self.window = "None"

        # self.window_changed_str.emit(self.window)

    # def on_method_checked(self, state):
        # """   """
        # if state == 0:
            # self.method = "None"
        # elif state == 1:
            # self.method = "Peak"
        # elif state == 2:
            # self.method = "Gassior"
        # elif state == 3:
            # self.method = "Naff"
        # else:
            # self.method = "None"

        # self.method_changed_str.emit(self.method)

    # def on_lboardsbox_changed(self, value):
        # """   """
        # self.lboard = value
        # self.on_boards_changed()

    # def on_rboardsbox_changed(self, value):
        # """   """
        # self.rboard = value
        # self.on_boards_changed()

    # def on_plot_checked(self, state):
        # """   """
        # if state == Qt.Checked:
            # self.scale = "Log_Y"
        # else:
            # self.scale = "Normal"
        # self.scale_changed_obj.emit(self)

    # def on_boards_changed(self):
        # """   """
        # self.boards = {
            # "lboard": self.lboard,
            # "rboard": self.rboard
        # }
        # self.boards_changed.emit(self.boards)
        # self.signature.emit(True)

    # def set_str_id(self, str):
        # """   """
        # self.str_id = str
