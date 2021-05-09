import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtGui import QPixmap, QImage

class HelpWidget(QWidget):
    """   """
    def __init__(self, file_name):
        super().__init__()
        self.label = QLabel(self)
        pixmap = QPixmap(file_name)
        self.label.setPixmap(pixmap)
        self.resize(pixmap.width(), pixmap.height())
        #self.show()

    # @staticmethod
    # def convert_numpy_img_to_qpixmap(np_img):
        # height, width, channel = np_img.shape
        # bytesPerLine = 3 * width
        # return QPixmap(QImage(np_img.data, width, height, bytesPerLine, QImage.Format_RGB888).rgbSwapped())
