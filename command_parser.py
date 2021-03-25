# This Python file uses the following encoding: utf-8
#

from PyQt5.QtCore import Qt, QObject
import signal
import argparse
from mainwindow import *

from dataprocessor import DataProcessor
from settingscontrol import SettingsControl
from controlwidget import ControlWidget

class TerminalParser(QObject):
    """   """
    window_changed_str = pyqtSignal(str)

    def __init__(self, parent=None):
        super(TerminalParser, self).__init__(parent)

        self.parser = argparse.ArgumentParser(description='Startup settings')

        self.parser.add_argument('-bn', action="store", dest = 'bpm_name',help = 'bpm_name')
        #self.parser.add_argument('-mt', action="store", default = "Peak", dest="method", help = 'method type')

        slf.results = self.parser.parse_args()
        self.bpm_name_parsed = self.result.bpm_name

        print(self.parser.parse_args())

