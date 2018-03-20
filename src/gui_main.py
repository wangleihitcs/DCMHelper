# -*- coding:utf-8 -*-
import sys
from PyQt4 import QtGui, QtCore
import shutil
import os
from dcm import dcm2img
from utils import dir2array

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
        self.connect(open, QtCore.SIGNAL('triggered()'), self.saveBatch)
        # File菜单下Save
        save = QtGui.QAction(QtGui.QIcon('icons/save.png'), 'Save', self)
        save.setShortcut('Ctrl+S')
        save.setStatusTip('Save file')
        self.connect(save, QtCore.SIGNAL('triggered()'), self.saveDir)
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

        # batch = menubar.addMenu('&Batch')
        # self.connect(batch, QtCore.SIGNAL('triggered()'), self.saveBatch)

        # 中间布局
        widget = QtGui.QWidget()

        left_vbox = QtGui.QVBoxLayout()
        pixmap = QtGui.QPixmap(700, 600)
        pixmap.fill()
        label = QtGui.QLabel()
        label.setPixmap(pixmap)
        left_vbox.addWidget(label)

        patient_id_label = QtGui.QLabel('PatientID:')
        patient_id_edit = QtGui.QLineEdit()
        patient_id_edit.setEnabled(False)
        patient_id_edit.setText('')
        patient_name_label = QtGui.QLabel('PatientName:')
        patient_name_edit = QtGui.QLineEdit()
        patient_name_edit.setEnabled(False)
        patient_name_edit.setText('')
        patient_bdate_label = QtGui.QLabel('PatientBirthDate:')
        patient_bdate_edit = QtGui.QLineEdit()
        patient_bdate_edit.setEnabled(False)
        patient_bdate_edit.setText('')
        patient_sex_label = QtGui.QLabel('PatientSex:')
        patient_sex_edit = QtGui.QLineEdit()
        patient_sex_edit.setEnabled(False)
        patient_sex_edit.setText('')
        study_id_label = QtGui.QLabel('StudyID:')
        study_id_edit = QtGui.QLineEdit()
        study_id_edit.setEnabled(False)
        study_id_edit.setText('')
        study_date_label = QtGui.QLabel('StudyDate:')
        study_date_edit = QtGui.QLineEdit()
        study_date_edit.setEnabled(False)
        study_date_edit.setText('')
        sop_uid_label = QtGui.QLabel('SOPInstanceUID:')
        sop_uid_edit = QtGui.QLineEdit()
        sop_uid_edit.setEnabled(False)
        sop_uid_edit.setText('')

        right_vbox = QtGui.QVBoxLayout()
        right_grid = QtGui.QGridLayout()
        right_grid.setSpacing(20)
        right_grid.addWidget(patient_id_label, 1, 0)
        right_grid.addWidget(patient_id_edit, 1, 1)
        right_grid.addWidget(patient_name_label, 2, 0)
        right_grid.addWidget(patient_name_edit, 2, 1)
        right_grid.addWidget(patient_bdate_label, 3, 0)
        right_grid.addWidget(patient_bdate_edit, 3, 1)
        right_grid.addWidget(patient_sex_label, 4, 0)
        right_grid.addWidget(patient_sex_edit, 4, 1)
        right_grid.addWidget(study_id_label, 5, 0)
        right_grid.addWidget(study_id_edit, 5, 1)
        right_grid.addWidget(study_date_label, 6, 0)
        right_grid.addWidget(study_date_edit, 6, 1)
        right_grid.addWidget(sop_uid_label, 7, 0)
        right_grid.addWidget(sop_uid_edit, 7, 1)
        right_vbox.addLayout(right_grid)

        main_layout = QtGui.QHBoxLayout()
        # hbox.setStretch(0, 1)
        # hbox.setStretch(1, 2)
        # main_layout.setMargin(15)
        main_layout.setSpacing(20)
        main_layout.addLayout(left_vbox)
        main_layout.addLayout(right_vbox)
        # main_layout.setSizeConstraint(QtGui.QLayout.SetFixedSize)

        widget.setLayout(main_layout)
        self.setCentralWidget(widget)

        self.patient_id_edit = patient_id_edit
        self.patient_name_edit = patient_name_edit
        self.patient_bdate_edit = patient_bdate_edit
        self.patient_sex_edit = patient_sex_edit
        self.study_id_edit = study_id_edit
        self.study_date_edit = study_date_edit
        self.sop_uid_edit = sop_uid_edit
        self.label = label


    def openDir(self):
        open_dir_path = QtGui.QFileDialog.getOpenFileName(self, 'open file dialog', '', '')
        print(open_dir_path)
        open_dir_path = str(open_dir_path) # 之前的open_dialog是QString, 需要转成普通String

        if open_dir_path != '':
            dcm_helper = dcm2img.DCMHelper(open_dir_path, '../data/temp.png')
            # 图片
            dcm_helper.dcm_to_img()
            pixmap = QtGui.QPixmap("../data/temp.png")
            pixmap = pixmap.scaled(700, 900)
            self.label.setPixmap(pixmap)
            # 病人信心
            infor = dcm_helper.read_information()
            print(infor)
            self.patient_id_edit.setText(infor['PatientID'])
            self.patient_name_edit.setText(infor['PatientName'])
            self.patient_bdate_edit.setText(infor['PatientBirthDate'])
            self.patient_sex_edit.setText(infor['PatientSex'])
            self.study_id_edit.setText(infor['StudyID'])
            self.study_date_edit.setText(infor['StudyDate'])
            self.sop_uid_edit.setText(infor['SOPInstanceUID'])


    def saveDir(self):
        save_dir_path = QtGui.QFileDialog.getSaveFileName(self, 'save file dialog', '', 'PNG file(*.png)')
        save_dir_path = str(save_dir_path)

        if save_dir_path != '':
            shutil.copyfile('../data/temp.png', save_dir_path)
            print('save .png success!')

    def saveBatch(self):
        # open_dir_path = QtGui.QFileDialog.getOpenFileName(self, 'open file dialog', '', '')
        # print(open_dir_path)
        # open_dir_path = str(open_dir_path)  # 之前的open_dialog是QString, 需要转成普通String
        #
        # if open_dir_path != '':
        #     dcm_helper = dcm2img.DCMHelper(open_dir_path, '../data/temp.png')
        open_path = 'C:/Users/liu/Desktop/1000968749CTA'
        save_path = 'C:/Users/liu/Desktop/test'
        dt = dir2array.DirTree(open_path, save_path)
        dir_tree = dt.getDirTree()
        print(dir_tree)
        save_path1 = save_path + '/' + '1000968749CTA'
        if os.path.exists(save_path1) == False:
            os.mkdir(save_path1)
        for key in dir_tree.keys():
            if key != 'path':
                if os.path.exists(save_path1 + '/' + key) == False:
                    os.mkdir(save_path1 + '/' + key)
        for key in dir_tree.keys():
            if key != 'path':
                open_path1 = open_path + '/' + key
                name_list = dir_tree[key]
                for name in name_list:
                    dcm_helper = dcm2img.DCMHelper(open_path1 + '/' + name, save_path1 + '/' + key + '/' + name + '.png')
                    if os.path.exists(save_path1 + '/' + key + '/' + name + '.png') == False:
                        dcm_helper.dcm_to_img()
                        print(save_path1 + '/' + key + '/'+ name + '.png')


def start():
	app = QtGui.QApplication(sys.argv)

	main = MainWindow()
	main.show()

	sys.exit(app.exec_())

start()
