import matplotlib
matplotlib.rcParams['backend'] = "Qt4Agg"
import pydicom
import matplotlib.pyplot as plt

class DCMHelper(object):
    def __init__(self, dcm_path, img_path):
        self.dcm_path = dcm_path
        self.img_path = img_path

    def dcm_to_img(self):
        filename = self.dcm_path
        dataset = pydicom.dcmread(filename)

        if 'PixelData' in dataset:
            rows = int(dataset.Rows)
            cols = int(dataset.Columns)
            print("Image size.......: {rows:d} x {cols:d}, {size:d} bytes".format(
                rows=rows, cols=cols, size=len(dataset.PixelData)))
            if 'PixelSpacing' in dataset:
                print("Pixel spacing....:", dataset.PixelSpacing)

        # use .get() if not sure the item exists, and want a default value if missing
        print("Slice location...:", dataset.get('SliceLocation', "(missing)"))

        # plot the image using matplotlib
        # print(dataset.pixel_array)
        plt.imshow(dataset.pixel_array, cmap = plt.cm.bone)
        plt.axis('off')
        plt.savefig(self.img_path)
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

        print(dataset.dir())
        return information

# dc = DCMHelper("C:/Users/liu/Desktop/TG18-RH-2k-01.dcm", '')
# dc.read_information()
