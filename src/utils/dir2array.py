import os

class DirTree(object):
    def __init__(self, dcm_path, output_path):
        self.dcm_path = dcm_path
        self.output_path = output_path

    def getDirTree(self):
        dir_tree = {}
        dir_tree['path'] = self.dcm_path
        for parent, dirnames, filenames in os.walk(self.dcm_path):
            i = 0
            for dirname in dirnames:
                child_dir_tree = {}
                series_path = self.dcm_path + '/' + dirname
                child_dir_tree['path'] = series_path
                filename_list = []
                for parent, dirnames, filenames in os.walk(series_path):
                    for filename in filenames:
                        filename_list.append(series_path + '/' + filename)
                i += 1
                child_dir_tree['filepaths'] = filename_list
                dir_tree['data' + str(i)] = child_dir_tree
            i += 1
        return dir_tree

# dt = DirTree('/Users/wanglei/Downloads/wh_ah_data/1001004816CTA', '/Users/wanglei/Downloads')
# dir_tree = dt.getDirTree()
# print(dir_tree)