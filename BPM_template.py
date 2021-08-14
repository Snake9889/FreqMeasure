#
#
from PyQt5.QtCore import pyqtSignal, QObject
import numpy as np
import pycx4.qcda as cda


class BPMTemplate(QObject):
    """   """
    data_ready = pyqtSignal(object)


    def __init__(self, bpm_name='', parent=None):
        super(BPMTemplate, self).__init__(parent)

        # print("Template BPM name: {0}".format(bpm_name))

        self.bpm_name = bpm_name
        self.num_pts = 1024
        self.data_len = self.num_pts

        self.dataT = None
        self.dataX = None
        self.dataZ = None
        self.dataI = None

        self.lboard = 0.01
        self.rboard = 0.5


    def force_data_ready(self, signature):
        """   """
        if signature == True:
            if self.dataT is not None:
                self.data_ready.emit(self)
            else:
                pass
