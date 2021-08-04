#
#
from PyQt5.QtCore import pyqtSignal, QObject, QTimer
import numpy as np
import pycx4.qcda as cda
from datasources import BPMData
from BPM_template import BPMTemplate


class BPMData(BPMTemplate):
    """   """
    # data_ready = pyqtSignal(object)

    def __init__(self, bpm_name='', parent=None):
        super(BPMData, self).__init__(parent)

        self.hesh = [0, 0, 0, 0]
        self.control = (1, 1, 1, 1)
        self.l = [0, 0, 0, 0]

        BPM1 = BPMData("bpm01")
        BPM2 = BPMData("bpm02")
        BPM3 = BPMData("bpm03")
        BPM4 = BPMData("bpm04")

        BPM1.data_ready.connect(self.timeshift)
        BPM2.data_ready.connect(self.timeshift)
        BPM3.data_ready.connect(self.timeshift)
        BPM4.data_ready.connect(self.timeshift)

    def timeshift(self, BPM):
        """   """
        self.def_time = 30
        self.timer = QTimer()
        self.timer.timeout.connect(self.on_timer_update)
        self.timer.start(self.def_time)

        if BPM.bpm_name == "bpm01":
            hesh[0] = 1

        elif BPM.bpm_name == "bpm02":
            hesh[1] = 1

        elif BPM.bpm_name == "bpm03":
            hesh[2] = 1

        elif BPM.bpm_name == "bpm04":
            hesh[3] = 1

        else:
            pass

        if self.control = (hesh[0], hesh[1], hesh[2], hesh[3]):
            self.controller()

    def controller(self):
        """   """
        self.l = [len(BPM1.dataT), len(BPM2.dataT), len(BPM3.dataT), len(BPM4.dataT)]
        if all(self.l[i] == self.l[i+1] for i in range(len(self.l)-1)):
            self.reshaping_data()
        else:
            self.l = [0, 0, 0, 0]
            pass
        

    def on_timer_update(self):
        """   """
        hesh = np.zeros(4)
        pass

    def reshaping_data(self):
        """   """
        self.dataT = reshaping_arrays(BPM1.dataT, BPM2.dataT, BPM3.dataT, BPM4.dataT)
        self.dataX = reshaping_arrays(BPM1.dataX, BPM2.dataX, BPM3.dataX, BPM4.dataX)
        self.dataZ = reshaping_arrays(BPM1.dataZ, BPM2.dataZ, BPM3.dataZ, BPM4.dataZ)
        self.dataI = reshaping_arrays(BPM1.dataI, BPM2.dataI, BPM3.dataI, BPM4.dataI)
        
        self.data_ready.emit(self)

    def reshaping_arrays(self, M1, M2, M3, M4):
        """   """
        newMass = np.zeros(len(M1)*4)
        for i in range(len(M1)):
            newMass[4*i] = M1[i]
            newMass[4*i + 1] = M2[i]
            newMass[4*i + 2] = M3[i]
            newMass[4*i + 3] = M4[i]

        return(newMass)

    def force_data_ready(self, signature):
        """   """
        super().force_data_ready(signature)
