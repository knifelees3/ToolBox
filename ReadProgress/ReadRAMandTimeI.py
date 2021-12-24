import numpy as np
import os
import sys
import matplotlib.pyplot as plt


def changetext(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        lines_memo = []  # 创建了一个空列表，里面没有元素
        lines_time = []  # 创建了一个空列表，里面没有元素
        for line in f.readlines():
            if 'Physical memory' in line:
                memo = line[17:-4]
                lines_memo.append(memo)
            if 'Solution time' in line:
                memo = line[15:19]
                lines_time.append(memo)

    return lines_memo, lines_time


if __name__ == "__main__":
    os.chdir(sys.path[0])
    dst_dir_1 = './LogFile/comsol_progress_11.txt'
    dst_dir_2 = './LogFile/comsol_progress_21.txt'
    dst_dir_3 = './LogFile/comsol_progress_31.txt'

    lines_memo_1, lines_time_1 = changetext(dst_dir_1)
    lines_memo_2, lines_time_2 = changetext(dst_dir_2)
    lines_memo_3, lines_time_3 = changetext(dst_dir_3)
    print(len(lines_time_1))
    print(len(lines_time_2))
    print(len(lines_time_3))

    num_1 = int((len(lines_time_1) - 1) / 2)
    num_2 = int((len(lines_time_2) - 1) / 2)
    num_3 = int((len(lines_time_3) - 1) / 2)

    x_1 = np.linspace(1, num_1, num_1)
    x_2 = np.linspace(1, num_2, num_2)
    x_3 = np.linspace(1, num_3, num_3)

    memo_mat_1 = np.zeros(num_1)
    time_mat_1 = np.zeros(num_1)

    memo_mat_2 = np.zeros(num_2)
    time_mat_2 = np.zeros(num_2)

    memo_mat_3 = np.zeros(num_3)
    time_mat_3 = np.zeros(num_3)

    for l in range(num_1):
        memo_mat_1[l] = float(lines_memo_1[3 * (l) + 2])
        time_mat_1[l] = float(lines_time_1[2 * (l) + 1])
    for l in range(num_2):
        memo_mat_2[l] = float(lines_memo_2[3 * (l) + 2])
        time_mat_2[l] = float(lines_time_2[2 * (l) + 1])
    for l in range(num_3):
        memo_mat_3[l] = float(lines_memo_3[3 * (l) + 2])
        time_mat_3[l] = float(lines_time_3[2 * (l) + 1])

    fig1 = plt.figure(figsize=(6.4 * 2, 4.8))
    plt.subplot(121)
    plt.plot(x_1, memo_mat_1, label='4CPU 1')
    plt.plot(x_2, memo_mat_2, label='4CPU 2')
    plt.plot(x_3, memo_mat_3, label='Dell 1')
    plt.xlabel('Loop Counts')
    plt.ylabel('Physical Memory (GB)')
    plt.legend(loc='best')

    plt.subplot(122)
    plt.plot(x_1, time_mat_1, label='4CPU 1')
    plt.plot(x_2, time_mat_2, label='4CPU 2')
    plt.plot(x_3, time_mat_3, label='Dell 1')
    plt.xlabel('Loop Counts')
    plt.ylabel('Simulation Time (s)')

    plt.legend(loc='best')

    plt.show()
