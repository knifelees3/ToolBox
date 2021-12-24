import os
from shutil import copy2


def changetext(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        lines = []  # 创建了一个空列表，里面没有元素
        counter = 0
        for line in f.readlines():
            print(counter)
            if 'title' in line:
                title = '#'+' '+line[7:]
                lines.append(title)
            if counter != 0 and counter != 1:
                lines.append(line)
            if line == '---\n':
                counter = counter+1
        f.close()
    with open(filename, 'w', encoding='utf-8') as f:
        for line in lines:
            f.write('%s\n' % line)
        print('已经修改了文件： ' + filename)


def change_files(dstdir):
    counter = 0
    for filepath, dirnames, filenames in os.walk(dstdir):
        for filename in filenames:
            if 'A_En' in filename or 'B_随笔' in filename or 'C_教程' in filename or 'D_收集' in filename and filename.endswith('.md'):
                counter = counter + 1
                long_name = os.path.join(filepath, filename)
                # print(long_name)
                changetext(long_name)
    print('一共修改了' + str(counter) + '个文件')


def copy_files(rootdir, dstdir):
    counter = 0
    for filepath, dirnames, filenames in os.walk(rootdir):
        for filename in filenames:
            if 'A_En' in filename or 'B_随笔' in filename or 'C_教程' in filename or 'D_收集' in filename and filename.endswith('.md'):
                counter = counter + 1
                long_name = os.path.join(filepath, filename)
                copy2(long_name, dstdir)
                print('已经复制了文件： ' + long_name)

    print('一共复制了' + str(counter) + '个文件')


if __name__ == "__main__":

    # ______________________________________________________________
    # On personal pc
    rootdir = r'C:\Users\xiail\Documents\Dropbox\Note\VNote'
    # dstdir = r'C:
    #     Users\xiail\OneDrive\Blog\Blog_V1\source\_posts\'
    # test folder
    dstdir = r'C:\Users\xiail\Desktop\TestBlog\CSDN'

    copy_files(rootdir, dstdir)
    change_files(dstdir)
