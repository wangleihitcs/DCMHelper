# -*- coding:utf-8 -*-
import os


def gci(dcm_path, filepath_list):
    files = os.listdir(dcm_path)
    for file in files:
        file_dir = os.path.join(dcm_path, file)
        if os.path.isdir(file_dir):
            gci(file_dir, filepath_list)
        else:
            # print(os.path.join(dcm_path, file_dir))
            filepath_list.append(os.path.join(dcm_path, file_dir))

class DirTree(object):
    def __init__(self, dcm_path, output_path):
        self.dcm_path = dcm_path
        self.output_path = output_path

    def getDirTree(self):
        dir_tree = {}
        dir_tree['path'] = self.dcm_path
        for parent, dirnames, filenames in os.walk(self.dcm_path):
            for dirname in dirnames:
                # child_dir_tree = {}
                series_path = dirname
                filename_list = []
                path_1 = os.path.join(self.dcm_path, series_path)
                for parent, dirnames, filenames in os.walk(path_1):
                    for filename in filenames:
                        filename_list.append(filename)
                # child_dir_tree['filepaths'] = filename_list
                dir_tree[series_path] = filename_list
        return dir_tree

    def getDictList(self):
        print(self.dcm_path)
        print(self.output_path)

        filepath_list = []
        gci(self.dcm_path, filepath_list)

        dict_list = []
        for filepath in filepath_list:
            dict = {}
            filepath = filepath.replace('\\', '/')

            lastpath = os.path.abspath(os.path.dirname(self.dcm_path))
            lastpath = lastpath.replace('\\', '/')
            print(lastpath)

            outputpath = filepath.replace(lastpath, self.output_path)
            # print(outputpath)
            dict[filepath] = outputpath
            print(dict)
            # for key, value in dict.items():
            #     print(key + ', ' + value)
            dict_list.append(dict)
        return dict_list


# dt = DirTree('C:\Users\liu\Desktop\dcm\p1', 'C:\Users\liu\Desktop\pngs')
# dict_list = dt.getDictList()
# print(dir_tree)