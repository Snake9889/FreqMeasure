
from PyQt5.QtCore import pyqtSignal, QObject, QTimer
import numpy as np
from FreqMeasure.Modules.DataSources.BPM_template import BPMTemplate


class BPMData(BPMTemplate):
    """   """

    def __init__(self, bpm_name='', parent=None):
        super().__init__(bpm_name, parent)

        self.bpm_phase = 0.0;

        if bpm_name == "bpm01":
            self.bpm_phase = 0.01
        elif bpm_name == "bpm02":
            self.bpm_phase = 0.02
        elif bpm_name == "bpm03":
            self.bpm_phase = 0.03
        elif bpm_name == "bpm04":
            self.bpm_phase = 0.04
        else:
            self.bpm_phase = 0.0
        
        self.mu, self.sigma = 0, 1
        self.a0 = 1
        self.a1 = 0.8
        self.a2 = 0.5
        self.w0 = 0.181
        self.w1 = 0.176
        self.w2 = 0.02
        self.k = 0.000005
        self.n_amp = 0.1
        self.bn_amp = 0.025
        
        self.def_time = 5000
        self.timer = QTimer()
        self.timer.timeout.connect(self.on_timer_update)
        self.timer.start(self.def_time)

    def on_timer_update(self):
        """   """
        self.generate_bpm_data()
        self.data_ready.emit(self)

    def generate_bpm_data(self):
        """   """
        self.dataT = np.arange(0, self.data_len, dtype=float)
        self.dataX = np.exp(-1*self.k*self.dataT**2)*\
                (self.harmonic_oscillations(self.bpm_phase, self.dataT, self.a0, self.w0, self.n_amp) + \
                self.harmonic_oscillations(self.bpm_phase, self.dataT, self.a1, self.w1, self.n_amp) + \
                self.harmonic_oscillations(self.bpm_phase, self.dataT, self.a2, self.w2, self.n_amp)) + \
                [x for x in self.bn_amp*(np.random.normal(self.mu, self.sigma, self.data_len))]

        self.dataZ = np.exp(-0.5*self.k*self.dataT**2)*\
                (self.harmonic_oscillations(self.bpm_phase, self.dataT, self.a0, self.w0, self.n_amp) + \
                1.5*self.harmonic_oscillations(self.bpm_phase, self.dataT, self.a1, self.w1, self.n_amp) + \
                3* self.harmonic_oscillations(self.bpm_phase, self.dataT, self.a2, self.w2, self.n_amp)) + \
                [x for x in self.bn_amp*(np.random.normal(self.mu, self.sigma, self.data_len))]
        self.dataI = np.ones(self.data_len)
        self.dataX = self.dataX + 0.03 * np.random.normal(size=self.data_len)  # 30% noise
        self.dataZ = self.dataZ + 0.01 * np.random.normal(size=self.data_len)  # 10% noise

    def harmonic_oscillations(self, phase, dataT, amp1, freq, amp2):
        """   """
        osc = (amp1 + amp2*(np.random.normal(self.mu, self.sigma, self.data_len)))*np.sin(2 * np.pi * freq * dataT + 2 * np.pi * phase)

        return(osc)

    def force_data_ready(self, signature):
        """   """
        super().force_data_ready(signature)
