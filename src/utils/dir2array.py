# -*- coding:utf-8 -*-
import os

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

# dt = DirTree('/Users/wanglei/Downloads/wh_ah_data/1001004816CTA', '/Users/wanglei/Downloads')
# dir_tree = dt.getDirTree()
# print(dir_tree)