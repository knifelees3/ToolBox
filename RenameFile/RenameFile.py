# To rename the file
import os
import numpy as np

# srcDir = './'

# dstDir = './'

# try:
#     os.rename(srcDir, dstDir)
# except Exception as e:
#     print e
#     print 'rename dir fail\r\n'
# else:
#     print 'rename dir success\r\n'
# Define the file name
name_char_1 = '../MphFile/NewMesh3_Up_theta_'
name_char_2 = '_phi_'
name_char_3 = '.mph'

phi_mat = np.linspace(-np.pi / 2, np.pi / 2, 7)
theta_mat = np.array([np.pi * 45.1 / 180, np.pi * 50 / 180])


for l in range(1):
    for m in range(7):
        if (m == 2 or m == 4):
            phi_char = round(phi_mat[m], 15)
            theta_char = round(theta_mat[l], 15)
            file_name_ori = name_char_1 + \
                str(theta_char) + name_char_2 + str(phi_char) + name_char_3
            file_name_dst = name_char_1 + \
                str(l + 1) + name_char_2 + str(m + 1) + name_char_3
        elif (m == 3):
            phi_char = int(phi_mat[m])
            theta_char = round(theta_mat[l], 15)
            file_name_ori = name_char_1 + \
                str(theta_char) + name_char_2 + str(phi_char) + name_char_3
            file_name_dst = name_char_1 + \
                str(l + 1) + name_char_2 + str(m + 1) + name_char_3
        else:
            phi_char = round(phi_mat[m], 13)
            theta_char = round(theta_mat[l], 15)
            file_name_ori = name_char_1 + \
                str(theta_char) + name_char_2 + str(phi_char) + name_char_3
            file_name_dst = name_char_1 + \
                str(l + 1) + name_char_2 + str(m + 1) + name_char_3
        print(file_name_ori)
        print(file_name_dst)

        try:
            os.rename(file_name_ori, file_name_dst)
        except Exception as e:
            print(e)
            print('rename file fail\r\n')
        else:
            print('rename file success\r\n')

        print('END')
