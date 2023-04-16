import os
import shutil

"""
将List保存到文件
"""
def save_list_to_file(filename,datalist,type):
    f = open(filename, type)
    for line in datalist:
        line = line.decode().replace('\n', '').replace('\r', '')
        f.write(line + '\n')
    f.close()

"""
创建目录
"""
def create_dir(path_name):
    os.makedirs(path_name)

"""
删除目录
"""
def delete_dir(path_name):
    try:
        # os.rmdir(path_name)
        shutil.rmtree(path_name)
    except OSError as e:
        print("Error: %s : %s" % (path_name, e.strerror))

"""
删除目录下所有文件及子目录
"""
def delete_dir_all(dir):
    for files in os.listdir(dir):
        path = os.path.join(dir, files)
        try:
            shutil.rmtree(path)
        except OSError:
            os.remove(path)

"""
删除目录下所有文件
"""
def delete_dir_file(dir):
    for file in os.scandir(dir):
        os.remove(file.path)