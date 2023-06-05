import os
from shutil import copy2


def get_files(rootdir, dstdir):
    counter = 0
    for filepath, dirnames, filenames in os.walk(rootdir):
        for filename in filenames:
            if 'A_En' in filename or 'B_随笔' in filename \
                    or 'C_教程' in filename or 'D_收集' in \
                    filename or 'E_物理' in filename or 'F_数学' \
                    in filename and filename.endswith('.md'):
                counter = counter + 1
                long_name = os.path.join(filepath, filename)
                copy2(long_name, dstdir)
                print('已经复制了文件： ' + long_name)

    print('一共复制了' + str(counter) + '个文件')


if __name__ == "__main__":

    # ______________________________________________________________
    # On personal pc
    rootdir = r'C:\Users\ZhaohuaTian\Documents\Dropbox\Note\Notes-Collection'
    # dstdir = r'C:
    #     Users\xiail\OneDrive\Blog\Blog_V1\source\_posts\'
    # test folder
    # dstdir = r'C:\Users\ZhaohuaTian\Desktop\BlogTmp'
    dstdir = r'D:\Blog\GithubBlog\source\\_posts'

    # _______________________________________________________________
    # For windows in science building
    #rootdir = r'E:\坚果云同步\Dropbox\Note\Vnote'
    #dstdir=r'C:\Users\Zhaohua Tian\OneDrive\Blog\Blog_V1\source\_posts'
    #dstdir = r'C:\Users\Zhaohua Tian\Desktop\TestBlog'

    # Run the function
    get_files(rootdir, dstdir)
