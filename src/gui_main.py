# -*- coding:utf-8 -*-
import sys
from PyQt5 import QtGui, QtCore, QtWidgets
import shutil
from dcm import dcm2img
# from dcm import signals

# reload(sys)
# sys.setdefaultencoding('utf-8')

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.initUI()

    def initUI(self):
        self.resize(1300, 800)
        self.move(400, 100)
        self.setWindowTitle('DCM Tool')

        # File菜单下Open
        open = QtWidgets.QAction(QtGui.QIcon('icons/open.png'), 'Open', self)
        open.setShortcut('Ctrl+O')
        open.setStatusTip('Open file')
        # self.connect(open, QtCore.SIGNAL('triggered()'), self.toOpen)
        open.triggered.connect(self.toOpen)
        # File菜单下Save
        save = QtWidgets.QAction(QtGui.QIcon('icons/save.png'), 'Save', self)
        save.setShortcut('Ctrl+S')
        save.setStatusTip('Save file')
        # self.connect(save, QtCore.SIGNAL('triggered()'), self.toSave)
        save.triggered.connect(self.toSave)
        # File菜单下Exit
        exit = QtWidgets.QAction(QtGui.QIcon('icons/exit.png'), 'Exit', self)
        exit.setShortcut('Ctrl+Q')
        exit.setStatusTip('Exit application')
        # self.connect(exit, QtCore.SIGNAL('triggered()'), QtCore.SLOT('close()'))
        exit.triggered.connect(QtWidgets.qApp.quit)
        self.statusBar().showMessage('Ready') # 状态栏
        # 菜单
        menubar = self.menuBar()
        file = menubar.addMenu('&File')
        file.addAction(open)
        file.addAction(save)
        file.addAction(exit)

        batch = QtWidgets.QAction(QtGui.QIcon('icons/open.png'), 'Batch', self)
        batch.setShortcut('Ctrl+B')
        batch.setStatusTip('Batch to img')
        # self.connect(batch, QtCore.SIGNAL('triggered()'), self.toBatch)
        batch.triggered.connect(self.toBatch)
        menubar.addAction(batch)
        # self.connect(batch, QtCore.SIGNAL('triggered()'), self.saveBatch)

        # self.one_ui_widget()
        self.batch_ui_widget()


    def toOpen(self):
        self.one_ui_widget()
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
    def toSave(self):
        # self.one_ui_widget()
        save_dir_path = QtGui.QFileDialog.getSaveFileName(self, 'save file dialog', '', 'PNG file(*.png)')
        save_dir_path = str(save_dir_path)

        if save_dir_path != '':
            shutil.copyfile('../data/temp.png', save_dir_path)
            print('save .png success!')
    def toBatch(self):
        self.batch_ui_widget()
    def toButtonOpen1(self):
        open_dir_path = QtWidgets.QFileDialog.getExistingDirectory(self, 'open directory dialog', 'C:/', QtWidgets.QFileDialog.ShowDirsOnly)
        # print(open_dir_path)
        open_dir_path = str(open_dir_path)  # 之前的open_dialog是QString, 需要转成普通String
        self.patient_dir_edit.setText(open_dir_path)
    def toButtonOpen2(self):
        open_dir_path = QtWidgets.QFileDialog.getExistingDirectory(self, 'open directory dialog', 'C:/', QtWidgets.QFileDialog.ShowDirsOnly)
        # print(open_dir_path)
        open_dir_path = str(open_dir_path)  # 之前的open_dialog是QString, 需要转成普通String
        self.img_save_edit.setText(open_dir_path)
    def toStart(self):
        # # print(self.patient_dir_edit.text())
        reply = QtWidgets.QMessageBox.information(self, '提示', '即将转换，请确认并等待!',
                                                  QtWidgets.QMessageBox.Yes|QtWidgets.QMessageBox.No)
        print(reply)
        open_path = str(self.patient_dir_edit.text())
        save_path = str(self.img_save_edit.text())
        if self.patient_dir_edit.text() != '' and self.img_save_edit.text() != '':
            open_path = open_path
            save_path = save_path
            dcm_helper = dcm2img.DCMHelper(open_path, save_path)
            log_str = dcm_helper.batch_dcm_to_image()
            self.log_text_edit.setText(log_str)
        else:
            print('Dir is null')

        # logSignal = signals.LogsSignal()
        # logSignal.str_signal.connect(self.log_slot)
        # logSignal.run()

    def log_slot(self, log_str):
        # self.log_text_edit.setText('zzzzzz')
        self.log_text_edit.setText(log_str)

    def one_ui_widget(self):
        # 中间布局
        widget = QtWidgets.QWidget()

        left_vbox = QtWidgets.QVBoxLayout()
        pixmap = QtWidgets.QPixmap(700, 600)
        pixmap.fill()
        label = QtWidgets.QLabel()
        label.setPixmap(pixmap)
        left_vbox.addWidget(label)

        patient_id_label = QtWidgets.QLabel('PatientID:')
        patient_id_edit = QtWidgets.QLineEdit()
        patient_id_edit.setEnabled(False)
        patient_id_edit.setText('')
        patient_name_label = QtWidgets.QLabel('PatientName:')
        patient_name_edit = QtWidgets.QLineEdit()
        patient_name_edit.setEnabled(False)
        patient_name_edit.setText('')
        patient_bdate_label = QtWidgets.QLabel('PatientBirthDate:')
        patient_bdate_edit = QtWidgets.QLineEdit()
        patient_bdate_edit.setEnabled(False)
        patient_bdate_edit.setText('')
        patient_sex_label = QtWidgets.QLabel('PatientSex:')
        patient_sex_edit = QtWidgets.QLineEdit()
        patient_sex_edit.setEnabled(False)
        patient_sex_edit.setText('')
        study_id_label = QtWidgets.QLabel('StudyID:')
        study_id_edit = QtWidgets.QLineEdit()
        study_id_edit.setEnabled(False)
        study_id_edit.setText('')
        study_date_label = QtWidgets.QLabel('StudyDate:')
        study_date_edit = QtWidgets.QLineEdit()
        study_date_edit.setEnabled(False)
        study_date_edit.setText('')
        sop_uid_label = QtWidgets.QLabel('SOPInstanceUID:')
        sop_uid_edit = QtWidgets.QLineEdit()
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

        main_layout = QtWidgets.QHBoxLayout()
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

    def batch_ui_widget(self):
        # batch 处理布局
        widget = QtWidgets.QWidget()

        grid_layout = QtWidgets.QGridLayout()
        grid_layout.setContentsMargins(200, 30, 200, 30)
        patient_dir_label = QtWidgets.QLabel('DCM Dir')
        # patient_dir_label.setContentsMargins(100, 20, 20, 10) # left, top, right, bottom
        patient_dir_edit = QtWidgets.QLineEdit('')
        patient_dir_edit.setText('')
        # patient_dir_edit.setContentsMargins(0, 20, 400, 10)
        open1 = QtWidgets.QPushButton('open', self)
        # open1.setContentsMargins(0, 20, 200, 10)
        open1.clicked.connect(self.toButtonOpen1)

        img_save_label = QtWidgets.QLabel('PNG Dir')
        img_save_edit = QtWidgets.QLineEdit()
        img_save_edit.setText('')
        open2 = QtWidgets.QPushButton('open', self)
        open2.clicked.connect(self.toButtonOpen2)

        start = QtWidgets.QPushButton('start', self)
        start.clicked.connect(self.toStart)
        start.setMaximumHeight(30)
        start.setMaximumWidth(100)
        log_text_label = QtWidgets.QLabel('Logs')
        log_text_edit = QtWidgets.QTextEdit()

        grid_layout.setSpacing(20)
        grid_layout.addWidget(patient_dir_label, 1, 0)
        grid_layout.addWidget(patient_dir_edit, 1, 1)
        grid_layout.addWidget(open1, 1, 2)
        grid_layout.addWidget(img_save_label, 2, 0)
        grid_layout.addWidget(img_save_edit, 2, 1)
        grid_layout.addWidget(open2, 2, 2)
        grid_layout.addWidget(start, 3, 2)
        grid_layout.addWidget(log_text_label, 4 , 0)
        grid_layout.addWidget(log_text_edit, 4, 1, 5, 1)

        widget.setLayout(grid_layout)
        self.setCentralWidget(widget)
        self.patient_dir_edit = patient_dir_edit
        self.img_save_edit = img_save_edit
        self.log_text_edit = log_text_edit

def start():
    app = QtWidgets.QApplication(sys.argv)

    main = MainWindow()
    # logThread = threads.StrThread()
    # logThread.str_signal.connect(main.log_slot)
    # logThread.start()
    main.show()

    sys.exit(app.exec_())

start()
