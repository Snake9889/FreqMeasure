# -*- coding: utf-8 -*-

from PyQt5.QtCore import pyqtSignal, Qt, QSettings
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPalette, QColor
from PyQt5 import uic
import os.path


class StatusWidget(QWidget):
    """   """

    def __init__(self, parent=None):
        super(StatusWidget, self).__init__(parent)

        ui_path = os.path.dirname(os.path.abspath(__file__))
        self.ui = uic.loadUi(os.path.join(ui_path, 'StatusWidget_2.ui'), self)


    # def data_ready(self, data_source):
        # """   """
        # self.hash = data_source.hash
        # self.setStyleSheet("QLabel { color : black }")
        # self.changing_label(self.ui.status_1, self.hash[0], 1)
        # self.changing_label(self.ui.status_2, self.hash[1], 2)
        # self.changing_label(self.ui.status_3, self.hash[2], 3)
        # self.changing_label(self.ui.status_4, self.hash[3], 4)

    # def data_error(self, data_source):
        # """   """
        # pass
        # self.hash = data_source.hash
        # self.changing_label(self.ui.status_1, self.hash[0], 1)
        # self.changing_label(self.ui.status_2, self.hash[1], 2)
        # self.changing_label(self.ui.status_3, self.hash[2], 3)
        # self.changing_label(self.ui.status_4, self.hash[3], 4)

    # def changing_label(self, label, num, pos):
        # """   """
        # if num == 0:
            # label.setToolTip("Data wasn't received")
            # label.setStyleSheet("color : blue")
            # label.setText('BPM_{}: {}'.format(pos, num))
            # # label.setText('{}'.format(num))

        # elif num == 1:
            # label.setToolTip("Everything alright")
            # label.setStyleSheet("color : black")
            # label.setText('BPM_{}: {}'.format(pos, num))
            # label.setText(u'<span style="font-size: 32pt; color: red;">•</span>')

        # elif num >= 2:
            # label.setToolTip("BPM work incorrectly")
            # label.setStyleSheet("color : red")
            # label.setText('{}'.format(num))

        # else:
            # label.setToolTip("The program doesn't work correctly")
            # label.setStyleSheet("color : green")
            # label.setText('{}'.format(num))
        
