# This Python file uses the following encoding: utf-8
#

from PyQt5.QtCore import Qt, QObject
import argparse
from mainwindow import *

class TerminalParser(QObject):
    """   """

    def __init__(self, parent=None):
        super(TerminalParser, self).__init__(parent)

        self.parser = argparse.ArgumentParser(description = 'Startup settings')

        self.parser.add_argument('-bn', action = "store", dest = 'bpm_name', help = 'bpm_name')
        self.parser.add_argument('-mt', action="store", default = "Peak", dest="method", help = 'method type')

        self.results = self.parser.parse_args()
        self.bpm_name_parsed = self.results.bpm_name

        print(self.parser.parse_args())

