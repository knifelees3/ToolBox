import numpy as np
import matplotlib.pyplot as plt
import re


# import re

# pattern = re.compile(r'\d+')   # 查找数字
# pattern = re.compile(r'[+-]?\d+\.?\d*[e]?[+-]?\d*\d*?')   #
# # pattern = re.compile(r'[e]')   #
# result1 = pattern.findall('0   31     709   -6.657158e-01    0.000e+00    8.186e-03    4.483e+00')
# result2 = pattern.findall('run88oob123google456', 0, 10)

# print(result1)
# print(result2)


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

if __name__ == "__main__":
    dst_dir_1 = './LogFile/progress7cav.txt'
    line = read_stepvalues(dst_dir_1)
    data1d = np.ravel(np.array(line))
    numdata = len(data1d)
    perlen = int(1e5)
    numfig = int((numdata - numdata % perlen) / perlen / 6) + 1
    dataopti = np.zeros((perlen, numfig))
    datastep = np.zeros((perlen, numfig))
    maxdata = np.zeros((numfig, 1))
    for l in range(numfig):
        if l == numfig - 1:
            lenlast = len(data1d[l * 6 * perlen:numdata])
            tmp = np.reshape(data1d[l * 6 * perlen:numdata], (int(lenlast / 6), 6))
            dataopti[0:int(lenlast / 6), l] = -tmp[:, 2]
            datastep[0:int(lenlast / 6), l] = np.ravel(tmp[:, 0])
            maxdata[l, 0] = np.max(-tmp[:, 2])
        else:
            tmp = np.reshape(data1d[l * 6 * perlen: (l + 1) * 6 * perlen], (perlen, 6))
            dataopti[:, l] = -np.ravel(tmp[:, 2])
            datastep[:, l] = np.ravel(tmp[:, 0])
            maxdata[l, 0] = np.max(-tmp[:, 2])
        fig1 = plt.figure(figsize=(6.4, 4.8))
        plt.plot(datastep[:, l], dataopti[:, l])
        plt.xlabel('Interation Step')
        plt.ylabel('Optimal Value')
        plt.title(str(l))
        strfilename = './Figure/pico_step_7cav' + str(l) + '.png'
        plt.savefig(strfilename)
        plt.close(fig1)
        # plt.legend(loc='best')

    fig2 = plt.figure(figsize=(6.4, 4.8))
    plt.plot(maxdata)
    plt.xlabel('Interation Step')
    plt.ylabel('Optimal Value')
    plt.title(str(np.max(maxdata)))
    # plt.legend(loc='best')
    strfilename = './Figure/global_step_7cav' + '.png'
    plt.savefig(strfilename)
    plt.close(fig2)
