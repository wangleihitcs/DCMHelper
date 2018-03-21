import matplotlib
matplotlib.rcParams['backend'] = "Qt4Agg"
import pydicom
import matplotlib.pyplot as plt
import os
from utils import dir2array


class DCMHelper(object):
    def __init__(self, dcm_path, img_path):
        self.dcm_path = dcm_path
        self.img_path = img_path

    def dcm_to_img(self):
        self.dcm_to_img_by_path(self.dcm_path, self.img_path)

    def batch_dcm_to_image(self):
        open_path = self.dcm_path
        str_array = open_path.split('/')
        pantient_dirname = str_array[-1]
        save_path = self.img_path

        dt = dir2array.DirTree(open_path, save_path)
        dir_tree = dt.getDirTree()
        # print(dir_tree)
        save_path1 = save_path + '/' + pantient_dirname + '(PNG)'
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
                    if os.path.exists(save_path1 + '/' + key + '/' + name + '.png') == False:
                        self.dcm_to_img_by_path(open_path1 + '/' + name, save_path1 + '/' + key + '/' + name + '.png')
                        print(save_path1 + '/' + key + '/' + name + '.png')
        print('batch save to img success!')

    def dcm_to_img_by_path(self, open_dcm_path, save_img_path):
        filename = open_dcm_path
        dataset = pydicom.dcmread(filename)

        if 'PixelData' in dataset:
            rows = float(dataset.Rows)
            cols = float(dataset.Columns)
            # print("Image size.......: {rows:f} x {cols:f}, {size:d} bytes".format(
            #     rows=rows, cols=cols, size=len(dataset.PixelData)))
            # if 'PixelSpacing' in dataset:
            #     print("Pixel spacing....:", dataset.PixelSpacing)

        # use .get() if not sure the item exists, and want a default value if missing
        # print("Slice location...:", dataset.get('SliceLocation', "(missing)"))

        # plot the image using matplotlib
        image_array = dataset.PixelData
        print(dataset.file_meta.TransferSyntaxUID)
        # print(image_array)
        plt.figure(figsize=(rows/100, cols/100))
        plt.imshow(dataset.pixel_array, cmap = plt.cm.bone)
        plt.axis('off')
        plt.savefig(save_img_path)
        # plt.show()

    def read_information(self):
        information = {}
        dataset = pydicom.read_file(self.dcm_path)
        information['width'] = dataset.Rows
        information['height'] = dataset.Columns
        information['type'] = dataset.Modality
        information['PatientID'] = dataset.PatientID
        information['PatientName'] = dataset.PatientName
        information['PatientBirthDate'] = dataset.PatientBirthDate
        information['PatientSex'] = dataset.PatientSex
        information['StudyID'] = dataset.StudyID
        information['StudyDate'] = dataset.StudyDate
        information['StudyTime'] = dataset.StudyTime
        information['SOPInstanceUID'] = dataset.SOPInstanceUID
        information['Manufacturer'] = dataset.Manufacturer

        # print(dataset.dir())
        return information

    def pixel_to_img(self):
        filename = self.dcm_path
        dataset = pydicom.dcmread(filename)
        if 'PixelData' in dataset:
            rows = int(dataset.Rows)
            cols = int(dataset.Columns)
            image_data = dataset.pixel_array
        print('(%d, %d)' % (rows, cols))
        print(image_data)

# dc = DCMHelper("C:/Users/liu/Desktop/DICOM/IM_0001", '../temp.png')
# infor = dc.read_information()
# print(infor)
# dc.dcm_to_img()