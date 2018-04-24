from PyQt5 import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import QtCore
import time, sys

class Backend(QThread):
    update_date = pyqtSignal(QtCore.QString)

    def run(self):
        data = QDateTime.currentDateTime()
        self.update_date.emit(QString(str(data)))
        time.sleep(1)

class MainWindow(QDialog):
    def __init__(self):
        QDialog.__init__()
        self.initUI()

    def initUI(self):
        # exitAction = QtWidgets.QAction(QtGui.QIcon(''), '&Exit', self)
        # exitAction.triggered.connect(QtWidgets.qApp.quit)
        self.input = QLineEdit(self)

    def handleDisplay(self, data):
        self.input.setText(data)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    b = Backend()
    w = MainWindow()
    b.update_date.connect(w.handleDisplay)
    b.start()
    w.show()
    app.exec_()