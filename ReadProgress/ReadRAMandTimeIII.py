# %%
import numpy as np
import os
import sys
import matplotlib.pyplot as plt
import re

# %%
def fetchinfo(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        lines_memo = []  # 创建了一个空列表，里面没有元素
        lines_time = []  # 创建了一个空列表，里面没有元素
        pattern = re.compile(r'\d+\.?\d*')   # 查找数字
        count=0
        for line in f.readlines():
            if 'Updating plots' in line:
                count=count+1
            if count==1:
                if 'Physical memory' in line:
                    result = pattern.search(line)
                    lines_memo.append(result.group())
                    count=0
                if 'Solution time' in line:
                    result = pattern.search(line)
                    lines_time.append(result.group())

    return lines_memo, lines_time


if __name__ == "__main__":
    os.chdir(sys.path[0])
    dst_dir_1 = '../LogFile/DipoleGNRBendWaveguideModeProjectionSweepWL0.log'
    dst_dir_2 = '../LogFile/DipoleGNRBendWaveguideModeProjectionSweepWL0-2.log'

    lines_memo_1, lines_time_1 = fetchinfo(dst_dir_1)
    lines_memo_2, lines_time_2 = fetchinfo(dst_dir_2)

    print(len(lines_time_1))
    print(len(lines_time_2))

# %%
    num_1 = int(len(lines_time_1))
    num_2 = int(len(lines_time_2))


    x_1 = np.linspace(1, num_1, num_1)
    x_2 = np.linspace(1, num_2, num_2)


    memo_mat_1 = np.zeros(num_1)
    time_mat_1 = np.zeros(num_1)

    memo_mat_2 = np.zeros(num_2)
    time_mat_2 = np.zeros(num_2)

# %%
    for l in range(num_1):
        print(l)
        memo_mat_1[l] = float(lines_memo_1[l])
        time_mat_1[l] = float(lines_time_1[l])
# %%    
    for l in range(num_2):
        memo_mat_2[l] = float(lines_memo_2[l])
        time_mat_2[l] = float(lines_time_2[l])


    fig1 = plt.figure(figsize=(6.4 * 2, 4.8))
    plt.subplot(121)
    plt.plot(x_1, memo_mat_1, label='4CPU 1')
    plt.plot(x_2, memo_mat_2, label='4CPU 2')
    plt.xlabel('Loop Counts')
    plt.ylabel('Physical Memory (GB)')
    plt.legend(loc='best')

    plt.subplot(122)
    plt.plot(x_1, time_mat_1, label='4CPU 1')
    plt.plot(x_2, time_mat_2, label='4CPU 2')
    plt.xlabel('Loop Counts')
    plt.ylabel('Simulation Time (s)')

    plt.legend(loc='best')

    plt.show()

# %%
