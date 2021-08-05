#
#
from PyQt5.QtCore import pyqtSignal, QObject, QTimer
import numpy as np
import pycx4.qcda as cda

from BPM_template import BPMTemplate
from datasources_bpm import BPMData
#from datasources import BPMData


class BPMDataAll(BPMTemplate):
    """   """
    # data_ready = pyqtSignal(object)

    def __init__(self, bpm_name='', parent=None):
        super(BPMDataAll, self).__init__("bpm_all", parent)

        self.hash = [0, 0, 0, 0]
        self.control = (1, 1, 1, 1)
        self.l = [0, 0, 0, 0]
        #self.bpm_name = "bpm_all"

        self.timer = QTimer()
        self.timer.timeout.connect(self.on_timer_update)
        self.def_time = 10 * 1000

        self.BPM1 = BPMData("bpm01")
        self.BPM2 = BPMData("bpm02")
        self.BPM3 = BPMData("bpm03")
        self.BPM4 = BPMData("bpm04")
        print("Sanechek1")

        self.BPM1.data_ready.connect(self.timeshift)
        self.BPM2.data_ready.connect(self.timeshift)
        self.BPM3.data_ready.connect(self.timeshift)
        self.BPM4.data_ready.connect(self.timeshift)

    def timeshift(self, BPM):
        """   """
        print(BPM.bpm_name)
        self.bpm_name = BPM.bpm_name
        if self.hash == [0, 0, 0, 0]:
            self.timer.start(self.def_time)

        print("time")

        if self.bpm_name == "bpm01":
            self.hash[0] = self.hash[0] + 1
            print("Sanechek01")


        elif self.bpm_name == "bpm02":
            self.hash[1] = self.hash[1] + 1
            print("Sanechek2")

        elif self.bpm_name == "bpm03":
            self.hash[2] = self.hash[2] + 1
            print("Sanechek3")

        elif self.bpm_name == "bpm04":
            self.hash[3] = self.hash[3] + 1
            print("Sanechek4")

        else:
            pass

        if (self.hash[0], self.hash[1], self.hash[2], self.hash[3]) == self.control:
            self.controller()

    def controller(self):
        """   """
        self.l = [len(self.BPM1.dataT), len(self.BPM2.dataT), len(self.BPM3.dataT), len(self.BPM4.dataT)]
        self.hash = [0, 0, 0, 0]
        print("Sanechek_cntrl")

        if all(self.l[i] == self.l[i+1] for i in range(len(self.l)-1)):
            self.start_type_check()

        else:
            pass


    def start_type_check(self):
        """   """
        #Here'll be checking for type of bpm's starters.
        self.reshaping_data()
        #pass

    def on_timer_update(self):
        """   """
        self.hash = [0, 0, 0, 0]
        self.l = [0, 0, 0, 0]
        pass

    def reshaping_data(self):
        """   """
        self.dataT = np.arange(len(self.BPM1.dataT)*4)
        self.dataX = self.reshaping_arrays(self.BPM1.dataX, self.BPM2.dataX, self.BPM3.dataX, self.BPM4.dataX)
        self.dataZ = self.reshaping_arrays(self.BPM1.dataZ, self.BPM2.dataZ, self.BPM3.dataZ, self.BPM4.dataZ)
        self.dataI = self.reshaping_arrays(self.BPM1.dataI, self.BPM2.dataI, self.BPM3.dataI, self.BPM4.dataI)
        self.data_len = len(self.dataT)

        self.data_ready.emit(self)

    def reshaping_arrays(self, M1, M2, M3, M4):
        """   """
        newMass = np.zeros(len(M1)*4)
        for i in range(len(M1)):
            newMass[4*i + 0] = M1[i]
            newMass[4*i + 1] = M2[i]
            newMass[4*i + 2] = M3[i]
            newMass[4*i + 3] = M4[i]

            #print("{0}, {1}, {2}, {3}".format(M1[i], M2[i], M3[i], M4[i]))

        return(newMass)
