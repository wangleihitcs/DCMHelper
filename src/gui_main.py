# -*- coding:utf-8 -*-
import sys
from PyQt4 import QtGui, QtCore
import dcm2img

reload(sys)
sys.setdefaultencoding('utf-8')

class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.initUI()

    def initUI(self):
        self.resize(1300, 800)
        self.move(400, 100)
        self.setWindowTitle('DCM Tool')

        # File菜单下Open
        open = QtGui.QAction(QtGui.QIcon('icons/open.png'), 'Open', self)
        open.setShortcut('Ctrl+O')
        open.setStatusTip('Open file')
        self.connect(open, QtCore.SIGNAL('triggered()'), self.getOpenDir)
        # File菜单下Save
        save = QtGui.QAction(QtGui.QIcon('icons/save.png'), 'Save', self)
        save.setShortcut('Ctrl+S')
        save.setStatusTip('Save file')
        # File菜单下Exit
        exit = QtGui.QAction(QtGui.QIcon('icons/exit.png'), 'Exit', self)
        exit.setShortcut('Ctrl+Q')
        exit.setStatusTip('Exit application')
        self.connect(exit, QtCore.SIGNAL('triggered()'), QtCore.SLOT('close()'))
        self.statusBar().showMessage('Ready') # 状态栏
        # 菜单
        menubar = self.menuBar()
        file = menubar.addMenu('&File')
        file.addAction(open)
        file.addAction(save)
        file.addAction(exit)

        # 中间布局
        widget = QtGui.QWidget()

        vbox1 = QtGui.QVBoxLayout()
        pixmap = QtGui.QPixmap("../data/test.png")
        label = QtGui.QLabel()
        label.setPixmap(pixmap)
        vbox1.addWidget(label)

        vbox2 = QtGui.QVBoxLayout()
        patient_id_label = QtGui.QLabel('PatientID:')
        patient_id_edit = QtGui.QLineEdit()
        patient_id_edit.setEnabled(False)
        patient_id_edit.setText('xxxxxx')
        patient_name_label = QtGui.QLabel('PatientName:')
        patient_name_edit = QtGui.QLineEdit()
        patient_name_edit.setEnabled(False)
        patient_name_edit.setText('xxxxxx')
        patient_bdate_label = QtGui.QLabel('PatientBirthDate:')
        patient_bdate_edit = QtGui.QLineEdit()
        patient_bdate_edit.setEnabled(False)
        patient_bdate_edit.setText('xxxxxx')
        patient_sex_label = QtGui.QLabel('PatientSex:')
        patient_sex_edit = QtGui.QLineEdit()
        patient_sex_edit.setEnabled(False)
        patient_sex_edit.setText('xxxxxx')
        study_id_label = QtGui.QLabel('StudyID:')
        study_id_edit = QtGui.QLineEdit()
        study_id_edit.setEnabled(False)
        study_id_edit.setText('xxxxxx')
        study_date_label = QtGui.QLabel('StudyDate:')
        study_date_edit = QtGui.QLineEdit()
        study_date_edit.setEnabled(False)
        study_date_edit.setText('xxxxxx')
        sop_uid_label = QtGui.QLabel('SOPInstanceUID:')
        sop_uid_edit = QtGui.QLineEdit()
        sop_uid_edit.setEnabled(False)
        sop_uid_edit.setText('xxxxxx')

        grid = QtGui.QGridLayout()
        grid.setSpacing(20)
        grid.addWidget(patient_id_label, 1, 0)
        grid.addWidget(patient_id_edit, 1, 1)
        grid.addWidget(patient_name_label, 2, 0)
        grid.addWidget(patient_name_edit, 2, 1)
        grid.addWidget(patient_bdate_label, 3, 0)
        grid.addWidget(patient_bdate_edit, 3, 1)
        grid.addWidget(patient_sex_label, 4, 0)
        grid.addWidget(patient_sex_edit, 4, 1)
        grid.addWidget(study_id_label, 5, 0)
        grid.addWidget(study_id_edit, 5, 1)
        grid.addWidget(study_date_label, 6, 0)
        grid.addWidget(study_date_edit, 6, 1)
        grid.addWidget(sop_uid_label, 7, 0)
        grid.addWidget(sop_uid_edit, 7, 1)
        vbox2.addLayout(grid)

        hbox = QtGui.QHBoxLayout()
        # hbox.setStretch(0, 1)
        # hbox.setStretch(1, 2)
        hbox.setSpacing(50)
        hbox.addLayout(vbox1)
        hbox.addLayout(vbox2)

        widget.setLayout(hbox)
        self.setCentralWidget(widget)

        self.patient_id_edit = patient_id_edit
        self.patient_name_edit = patient_name_edit
        self.patient_bdate_edit = patient_bdate_edit
        self.patient_sex_edit = patient_sex_edit
        self.study_id_edit = study_id_edit
        self.study_date_edit = study_date_edit
        self.sop_uid_edit = sop_uid_edit


    def getOpenDir(self):
        open_dialog = QtGui.QFileDialog.getOpenFileName(self, 'open file dialog', 'C:\Users', 'DCM files(*.dcm)')
        print(open_dialog)

        dcm_helper = dcm2img.DCMHelper('C:/Users/liu/Desktop/TG18-RH-2k-01.dcm', 'tt.png')
        infor = dcm_helper.read_information()
        print(infor)
        self.patient_id_edit.setText(infor['PatientID'])
        self.patient_name_edit.setText(infor['PatientName'])
        self.patient_bdate_edit.setText(infor['PatientBirthDate'])
        self.patient_sex_edit.setText(infor['PatientSex'])
        self.study_id_edit.setText(infor['StudyID'])
        self.study_date_edit.setText(infor['StudyDate'])
        self.sop_uid_edit.setText(infor['SOPInstanceUID'])

    def clickEvent(self, event):
        if event.key() == QtCore.Qt.ActionsContextMenu:
            self.getOpenDir()

def start():
	app = QtGui.QApplication(sys.argv)

	main = MainWindow()
	main.show()

	sys.exit(app.exec_())

start()
