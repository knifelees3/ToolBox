import os
import numpy as np
from shutil import copy2
# To list the files in a specific folders


def list_files(dstdir):
    pnglist = []
    for filepath, dirnames, filenames in os.walk(dstdir):
        for filename in filenames:
            if "2" in filename and filename.endswith('.png'):
                pnglist.append(filename)
    return pnglist

# To obtain the str needed in latex file


def obtain_initial(filename):
    lines = []
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f.readlines():
            if line != '\\end{document}':
                lines.append(line)
    f.close()
    return lines

# To rename files by removing Chinese characters


def rename_png(filelist):
    for file in filelist:
        filenamestr = str(file)
        filenew = filenamestr[5:]
        print(filenew)
        try:
            os.rename(filenamestr, filenew)
        except Exception as e:
            print(e)
            print('rename file fail\r\n')
        else:
            print('rename file success\r\n')

        print('END')

# To generate latex files


def gentex(filename, filelist):
    num = len(filelist)
    modelfile = obtain_initial('./model_beamer.tex')
    with open(filename, 'w', encoding='utf-8') as f:
        for line in modelfile:
            f.write('%s\n' % line)
        for l in range(num):
            f.write('\n')
            f.write('\\begin{frame}\n')
            f.write('\\begin{figure}\n')
            f.write('\\centering\n')
            f.write('\\includegraphics[width=4in]{%s}\n' % filelist[l])
            f.write('\\end{figure}\n')
            f.write('\\end{frame}\n')
        f.write('\\end{document}\n')

    f.close()


if __name__ == "__main__":

    # ______________________________________________________________
    dstdir = r'C:\Users\ZhaohuaTian\Desktop\pic'
    pnglist = np.ravel(list_files(dstdir))
    # rename_png(pnglist)
    gentex("./test2.tex", pnglist)
