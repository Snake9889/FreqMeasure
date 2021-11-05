import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtCore import QSize, QCoreApplication
from PyQt5.QtGui import QPixmap, QIcon
import os.path


class PhaseWidget(QWidget):
    """   """
    def __init__(self, file_name):
        super().__init__()
        self.initUI()
        
        icon_path = os.path.dirname(os.path.abspath(__file__))
        help_icon = QIcon()
        help_icon.addFile(os.path.join(icon_path, 'etc/icons/Psi.png'), QSize(32, 32))
        self.setWindowIcon(help_icon)
        
    def initUI(self):
            self.setGeometry(300, 300, 300, 200)
            self.setWindowTitle('Phase')
            self.show()

        
    

        # pixmap = QPixmap(file_name)
        # self.label.setPixmap(pixmap)
        # self.resize(pixmap.width(), pixmap.height())
        #self.show()
