import os

class DicTree(object):
    def __init__(self, dcm_path, output_path):
        self.dcm_path = dcm_path
        self.output_path = output_path

    def getDicTree(self):
        list_name = []
            for parent, dirnames, filenames in os.walk(inputpath):
                for filename in filenames:
                    list_name.append(filename)
        list_name = sorted(list_name)