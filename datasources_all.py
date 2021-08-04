#
#
from PyQt5.QtCore import pyqtSignal, QObject
import numpy as np
import pycx4.qcda as cda
from datasources import BPMData


class BPMData(QObject):
    """   """
    data_ready = pyqtSignal(object)

    bpm_channel_template = "v2cx::hemera:4."

    def __init__(self, bpm_name='', parent=None):
        super(BPMData, self).__init__(parent)

        BPM1 = BPMData(2048)

        # if bpm_name == "bpm01":
            # bpm_channel = 4
        # elif bpm_name == "bpm02":
            # bpm_channel = 5
        # elif bpm_name == "bpm03":
            # bpm_channel = 6
        # elif bpm_name == "bpm04":
            # bpm_channel = 7
        # elif bpm_name == "all":
            # bpm_channel = 8
        # else:
            # bpm_channel = -1

            

        # bpm_data_name = '{0}{1}{2}'.format(self.bpm_channel_template, bpm_channel, "@s")
        # bpm_numpts_name = '{0}{1}{2}'.format(self.bpm_channel_template, bpm_channel, "@p10")

        # print(bpm_data_name)
        # print(bpm_numpts_name)

        # self.bpmChan = cda.VChan(bpm_data_name, max_nelems=8 * 1024 * 4, dtype=cda.DTYPE_INT32)
        # self.bpmChan_numpts = cda.IChan(bpm_numpts_name)
        

        # self.bpmChan_numpts.valueMeasured.connect(self._on_numpts_update)
        # self.bpmChan.valueMeasured.connect(self._on_signal_update)

        

    def receiving_data(self, bpm_channel):
        bpm_data_name = '{0}{1}{2}'.format(self.bpm_channel_template, bpm_channel, "@s")
        bpm_numpts_name = '{0}{1}{2}'.format(self.bpm_channel_template, bpm_channel, "@p10")
        print(bpm_data_name)
        print(bpm_numpts_name)

        self.bpmChan = cda.VChan(bpm_data_name, max_nelems=8 * 1024 * 4, dtype=cda.DTYPE_INT32)
        self.bpmChan_numpts = cda.IChan(bpm_numpts_name)
        # return (self.bpmChan, self.bpmChan_numpts)

        self.bpmChan_numpts.valueMeasured.connect(self._on_numpts_update)
        self.bpmChan.valueMeasured.connect(self._on_signal_update)

    def _on_signal_update(self, chan):
        """   """
        self.data = np.frombuffer(chan.val.data, dtype=np.dtype('f4'), count=chan.val.size)

    def _on_numpts_update(self, chan):
        """   """
        self.num_pts = chan.val
        self.data_len = self.num_pts

        tmp = np.reshape(self.data, (4, self.num_pts))

        self.dataT = tmp[0]
        self.dataX = tmp[1]
        self.dataZ = tmp[2]
        self.dataI = tmp[3]

        self.data_ready.emit(self)

        

    def force_data_ready(self, signature):
        """   """
        if signature == True:
            if self.data is not None:
                self.data_ready.emit(self)
            else:
                pass
