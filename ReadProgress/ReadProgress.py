import os
import time
import sys
import re
import numpy as np


def prog_read(filename, keystr, totalnum):
    with open(filename, 'r', encoding='utf-8') as f:
        lines = []  # 创建了一个空列表，里面没有元素
        counter = 0
        for line in f.readlines():
            if keystr in line:
                counter = counter + 1
        f.close()
        prog = float(counter / float(totalnum))
    return prog


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False


def trans_list_to_array(line):
    num = len(line)
    tmp = np.zeros(num)
    for l in range(num):
        tmp[l] = float(line[l])
    return tmp


def read_stepvalues(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        lines_iter = []
        for line in f.readlines():
            pattern1 = re.compile(r'[+-]?\d+\.?\d*[e]?[+-]?\d*\d*?')
            pattern2 = re.compile(r'\d+[e][+-]\d+')
            result1 = pattern1.findall(line)
            result2 = pattern2.findall(line)
            if len(result1) == 6 and len(result2) == 4:
                pattern3 = re.compile(r'[+-]?\d+\.?\d*[e]?[+-]?\d*\d*?')
                lines_iter.append(trans_list_to_array(pattern3.findall(line)))
    return lines_iter


filename = './LogFile/progress7cav.txt'
keystr = 'Solver stopped prematurely'
totalnum = 2000
prog = prog_read(filename, keystr, totalnum)
print("Has calculated ", str(prog * 100), '%')

line = read_stepvalues(filename)
data1d = np.ravel(np.array(line))
numdata = len(data1d)

datareshape = np.reshape(data1d, (int(numdata / 6), 6))
maxoverlp = np.max(-datareshape[:, 2])
print("The maximum overlap up to now is", maxoverlp)
# while prog < 1:
#     prog = prog_read(filename, keystr, totalnum)
#     print('current progress', prog, end="\r")
#     # sys.stdout.write("\033[F")
#     time.sleep(1)
