# This Python file uses the following encoding: utf-8
#


from PyQt5.QtCore import Qt, QObject

   import argparse
from mainwindow import *

class TerminalParser(QObject):
    """   """

    def __init__(self, parent=None):
        super(TerminalParser, self).__init__(parent)

        self.parser = argparse.ArgumentParser(description = 'Startup settings for software')

        self.parser.add_argument('-bn', action = 'store', default = 'model', dest = 'bpm_name', help = 'name of bpm, that can be bpm_0N, where N - number of bpm, or model - model of the signal by Denisov and Rogovsky!')
        self.parser.add_argument('-mt', action = 'store', default = 'peak', dest = 'method_name', help = 'type of method - can be naff, peak or gass - Gassior method')

        self.results = self.parser.parse_args()
        self.bpm_name_parsed = self.results.bpm_name
        self.method_name_parsed = self.results.method_name

        print(self.parser.parse_args())

