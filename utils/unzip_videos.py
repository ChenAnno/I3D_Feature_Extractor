# 用于zip视频文件的解压缩
# 视频文件夹移动至samplevideos中：如  I3D_Feature_Extraction_resnet-main/samplevideos/abuse_videos
import zipfile
import sys
import os

path = os.path.abspath('..') + '/samplevideos'


def get_dir_names(parent_path) -> list:
    dirs = []
    for _ in os.listdir(parent_path):
        new_path = path + '/' + str(_)
        if os.path.isdir(new_path):
            dirs.append(_)
    return dirs


def get_file_paths(parent_path) -> list:
    files = []
    for _ in os.listdir(parent_path):
        new_path = parent_path + '/' + str(_)
        if not os.path.isdir(new_path):
            files.append(new_path)

    return files


def unzip(file_path):
    zFile = zipfile.ZipFile(file_path, "r")
    # ZipFile.namelist(): 获取ZIP文档内所有文件的名称列表
    for fileM in zFile.namelist():
        zFile.extract(fileM, path)
    zFile.close()

    os.remove(file_path)  # Attention! will remove the origin zip file


if __name__ == '__main__':
    dirs = get_dir_names(parent_path=path)
    for dir in dirs:
        dir_path = path + '/' + str(dir)
        file_paths = get_file_paths(dir_path)
        for file_path in file_paths:
            unzip(file_path)
