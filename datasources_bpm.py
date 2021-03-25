#
#
#

from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal, Qt, QObject

import numpy as np

import pycx4.qcda as cda


class BPMData(QObject):
    """   """
    data_ready = pyqtSignal(object)

    bpm_channel_template = "v2cx::hemera:4."

    def __init__(self, bpm_name = '', parent=None):
        super(BPMData, self).__init__(parent)

        self.bpm_name = bpm_name
        self.num_pts = 1024
        self.data_len = self.num_pts

        self.tmp = None
        self.dataT = None
        self.dataX = None
        self.dataZ = None
        self.dataI = None

        self.lboard = 0.01
        self.rboard = 0.5

        if   bpm_name == "bpm01":
            bpm_channel = 4
        elif bpm_name == "bpm02":
            bpm_channel = 5
        elif bpm_name == "bpm03":
            bpm_channel = 6
        elif bpm_name == "bpm04":
            bpm_channel = 7
        else:
            bpm_channel = -1

        bpm_data_name   = '{0}{1}{2}'.format(self.bpm_channel_template, bpm_channel, "@s")
        bpm_numpts_name = '{0}{1}{2}'.format(self.bpm_channel_template, bpm_channel, "@p10")

        print(bpm_data_name)
        print(bpm_numpts_name)

        self.bpmChan        = cda.VChan(bpm_data_name, max_nelems = 8 * 1024 * 4, dtype = cda.CXDTYPE_INT32)
        self.bpmChan_numpts = cda.IChan(bpm_numpts_name)

        self.bpmChan_numpts.valueMeasured.connect(self._on_numpts_update)
        self.bpmChan.valueMeasured.connect(self._on_signal_update)

    def _on_signal_update(self, chan):
        # print('Signal received ... = {}'.format(chan.val))
        print('Signal received ...')
        self.tmp = np.frombuffer(chan.val.data, dtype = np.dtype('f4'))

    def _on_numpts_update(self, chan):
        print('Numpts received ... = {}'.format(chan.val))
        self.num_pts = chan.val
        self.data_len = self.num_pts
        
        self.tmp = np.reshape(self.tmp, (4, self.num_pts))

        self.dataT = self.tmp[0]
        self.dataX = self.tmp[1]
        self.dataZ = self.tmp[2]
        self.dataI = self.tmp[3]

        self.data_ready.emit(self)
       
        
