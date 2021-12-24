import scipy.io as scio
import matplotlib.patches as patches
import os as os
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
import cv2
"""
Created on Sat Dec 19 01:43:31 2020

@author: ZhaohuaTian
* Doing superpositions of different BFP
* Find the center of BFP and cut the matrix into a smaller one
* Remove the noise use the method developed in "superposition_picture_and_noise_remove.py" 
"""

"""
From Zhiyuan Wang:
* 拷给你的数据里只有01,03,05,06,07,08,10,12,15,16测量了对应光纤上的BFP，其它编号的数据可以删掉
* 对了，玻片上编号15的量子点背景没有测量，你用16号量子点的背景代替一下吧
"""
# Definition of function to find the circles


def find_center(BFP_ori, num_approxi):
    num_size_ori = np.shape(BFP_ori)[0]
    num_size_ori_half = int(num_size_ori/2)

    # First approximated range of the picture
    num_approxi = 200
    img = BFP_ori[num_size_ori_half-num_approxi:num_size_ori_half +
                  num_approxi, num_size_ori_half-num_approxi:num_size_ori_half+num_approxi]

    img = img.astype(np.uint8)
    gray = np.array(Image.fromarray(img))

    # test = gray.astype(np.uint8)
    # Blur using 3 * 3 kernel.
    gray_blurred = cv2.blur(gray, (2, 2))
    #gray_blurred =gray
    # Apply Hough transform on the blurred BFP.
    detected_circles = cv2.HoughCircles(gray_blurred,
                                        cv2.HOUGH_GRADIENT, dp=20, minDist=400, param1=50,
                                        param2=30, minRadius=60, maxRadius=90)
    # if detected_circles is not None:

    #     # Convert the circle parameters a, b and r to integers.
    #     detected_circles = np.uint16(np.around(detected_circles))

    #     for pt in detected_circles[0, :]:
    #         a, b, r = pt[0], pt[1], pt[2]

    #         # Draw the circumference of the circle.
    #         cv2.circle(img, (a, b), r, (0, 255, 0), 2)

    #         # Draw a small circle (of radius 1) to show the center.
    #         cv2.circle(img, (a, b), 1, (0, 0, 255), 3)
    #         cv2.imshow("Detected Circle", img)
    #         cv2.waitKey(0)
    return detected_circles


# Current Path
Path = os.getcwd()+"\\"

# Read the file list of different QD BFP and Bkg
file_list = os.listdir(Path)


# Only the figures can be in the file list
file_list_c = file_list.copy()
file_list_QD_coverslip = []
file_list_QD_fiber = []
file_list_Bkg_coverslip = []
file_list_Bkg_fiber = []

for file in file_list_c:
    if '.tif' not in file or '.py' in file:
        file_list.remove(file)
        print(file)
    elif 'Bkg' in file:
        if 'coverslip' in file:
            file_list_Bkg_coverslip.append(file[0:16])
        elif 'QD' in file:
            file_list_Bkg_fiber.append(file[0:15])
    else:
        if 'coverslip' in file:
            file_list_QD_coverslip.append(file[0:15])
        else:
            file_list_QD_fiber.append(file[0:11])
# Remove duplicates
file_list_QD_coverslip = list(dict.fromkeys(file_list_QD_coverslip))
file_list_Bkg_coverslip = list(dict.fromkeys(file_list_Bkg_coverslip))
file_list_QD_fiber = list(dict.fromkeys(file_list_QD_fiber))
file_list_Bkg_fiber = list(dict.fromkeys(file_list_Bkg_fiber))

# further pocess
# remove extra data from coverlsip list
remove_indices_QD = np.int_([1, 3, 5, 6, 7, 8, 10, 12, 15, 16])-1
remove_indices_Bkg = np.int_([1, 3, 5, 6, 7, 8, 10, 12, 15])-1
file_list_QD_coverslip = [i for j, i in enumerate(
    file_list_QD_coverslip) if j in remove_indices_QD]
file_list_Bkg_coverslip = [i for j, i in enumerate(
    file_list_Bkg_coverslip) if j in remove_indices_Bkg]
# add needed bkg data of 15
file_list_Bkg_coverslip.insert(8, 'Bkg_16_coverslip')
# add extra data into the data of 12
file_list_Bkg_fiber.insert(7, 'Bkg_QD_12_2_fib')
file_list_Bkg_coverslip.insert(7, 'Bkg_12_coverslip')
file_list_QD_coverslip.insert(7, 'QD_12_coverslip')
# %%
num_QD_coverslip = len(file_list_QD_coverslip)
num_Bkg_coverslip = len(file_list_Bkg_coverslip)
num_QD_fiber = len(file_list_QD_fiber)
num_Bkg_fiber = len(file_list_Bkg_fiber)

num_QD = num_QD_coverslip

# (1) Do a superpistion of data for different QDs
# (2) Find the center of different QDs
num_ori = 2048

BFP_fiber_ori = np.zeros((num_ori, num_ori, num_QD))
Bkg_fiber_ori = np.zeros((num_ori, num_ori, num_QD))
BFP_coverslip_ori = np.zeros((num_ori, num_ori, num_QD))
Bkg_coverslip_ori = np.zeros((num_ori, num_ori, num_QD))


num_BFP = 78*2
num_BFP_half = int(num_BFP/2)
num_approxi = int(400/2)
BFP_fiber = np.zeros((num_BFP, num_BFP, num_QD))
Bkg_fiber = np.zeros((num_BFP, num_BFP, num_QD))
BFP_coverslip = np.zeros((num_BFP, num_BFP, num_QD))
Bkg_coverslip = np.zeros((num_BFP, num_BFP, num_QD))

cen_BFP_fiber = np.zeros((num_QD, 3))
cen_BFP_coverslip = np.zeros((num_QD, 3))
# The extra dispalcement of BFP center
dis_x_pos = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])+3
dis_y_pos = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])+6

nb_QD_fiber_list = np.zeros(num_QD)
nb_Bkg_fiber_list = np.zeros(num_QD)
nb_QD_coverslip_list = np.zeros(num_QD)
nb_Bkg_coverslip_list = np.zeros(num_QD)
for l_QD in range(num_QD):
    nb_QD_fiber = 0
    nb_Bkg_fiber = 0
    nb_QD_coverslip = 0
    nb_Bkg_coverslip = 0
    for file in file_list:
        if file_list_QD_fiber[l_QD] in file[0:11]:
            nb_QD_fiber = nb_QD_fiber+1
            Filename = file
            tmp = np.array(plt.imread(Path+Filename))
            BFP_fiber_ori[:, :, l_QD] = BFP_fiber_ori[:, :, l_QD]+tmp
            circles = find_center(tmp, num_approxi)
            cen_BFP_fiber[l_QD, :] = cen_BFP_fiber[l_QD, :]+circles[0, 0, :]
        elif file_list_Bkg_fiber[l_QD] in file[0:15]:
            nb_Bkg_fiber = nb_Bkg_fiber+1
            Filename = file
            tmp = np.array(plt.imread(Path+Filename))
            Bkg_fiber_ori[:, :, l_QD] = Bkg_fiber_ori[:, :, l_QD]+tmp
        elif file_list_QD_coverslip[l_QD] in file[0:15]:
            nb_QD_coverslip = nb_QD_coverslip+1
            Filename = file
            tmp = np.array(plt.imread(Path+Filename))
            BFP_coverslip_ori[:, :, l_QD] = BFP_coverslip_ori[:, :, l_QD]+tmp
            circles = find_center(tmp, num_approxi)
            cen_BFP_coverslip[l_QD,
                              :] = cen_BFP_coverslip[l_QD, :]+circles[0, 0, :]
        elif file_list_Bkg_coverslip[l_QD] in file[0:16]:
            nb_Bkg_coverslip = nb_Bkg_coverslip+1
            Filename = file
            tmp = np.array(plt.imread(Path+Filename))
            Bkg_coverslip_ori[:, :, l_QD] = Bkg_coverslip_ori[:, :, l_QD]+tmp

    nb_QD_fiber_list[l_QD] = nb_QD_fiber
    nb_Bkg_fiber_list[l_QD] = nb_Bkg_fiber
    nb_QD_coverslip_list[l_QD] = nb_QD_coverslip
    nb_Bkg_coverslip_list[l_QD] = nb_Bkg_coverslip
    cen_BFP_fiber[l_QD, :] = cen_BFP_fiber[l_QD, :]/nb_QD_fiber
    cen_BFP_coverslip[l_QD, :] = cen_BFP_coverslip[l_QD, :]/nb_QD_coverslip

    print('Find center of ',
          file_list_QD_fiber[l_QD], ' at ', cen_BFP_fiber[l_QD, :])
    print('Find center of ',
          file_list_QD_coverslip[l_QD], ' at ', cen_BFP_coverslip[l_QD, :])
    position_x_fiber = int(
        cen_BFP_fiber[l_QD, 0]+1024-num_approxi-dis_x_pos[l_QD])
    position_y_fiber = int(
        cen_BFP_fiber[l_QD, 1]+1024-num_approxi-dis_y_pos[l_QD])
    position_x_coverslip = int(
        cen_BFP_coverslip[l_QD, 0]+1024-num_approxi-dis_x_pos[l_QD])
    position_y_coverslip = int(
        cen_BFP_coverslip[l_QD, 1]+1024-num_approxi-dis_y_pos[l_QD])

    BFP_fiber[:, :, l_QD] = BFP_fiber_ori[position_y_fiber-num_BFP_half:position_y_fiber +
                                          num_BFP_half, position_x_fiber-num_BFP_half:position_x_fiber+num_BFP_half, l_QD]
    Bkg_fiber[:, :, l_QD] = Bkg_fiber_ori[position_y_fiber-num_BFP_half:position_y_fiber +
                                          num_BFP_half, position_x_fiber-num_BFP_half:position_x_fiber+num_BFP_half, l_QD]
    BFP_coverslip[:, :, l_QD] = BFP_coverslip_ori[position_y_coverslip-num_BFP_half:position_y_coverslip +
                                                  num_BFP_half, position_x_coverslip-num_BFP_half:position_x_coverslip+num_BFP_half, l_QD]
    Bkg_coverslip[:, :, l_QD] = Bkg_coverslip_ori[position_y_coverslip-num_BFP_half:position_y_coverslip +
                                                  num_BFP_half, position_x_coverslip-num_BFP_half:position_x_coverslip+num_BFP_half, l_QD]
# # %%
# # vmax =np.max(np.sum(BFP/num_BFP**2)*1.5)
# # fig1=plt.figure()
# # plt.imshow(BFP[:,:,0],cmap='jet',vmin=0,vmax=vmax)
# # plt.show()
# Show the numer of QD BFP and background
# %%
fig1 = plt.figure()
plt.plot(nb_QD_fiber_list, label='number of pictures for QD BFP Fiber')
plt.plot(nb_Bkg_fiber_list, label='number of pictures for Background Fiber')
plt.plot(nb_QD_coverslip_list, label='number of pictures for QD BFP coverslip')
plt.plot(nb_Bkg_coverslip_list,
         label='number of pictures for Background coverslip')
plt.grid()
plt.legend(loc='best')
plt.savefig('./BFP_Image_List/numberoffilesofBFPandBkg.png')
# plt.show()
# %% The ratio to use
fold = np.ones(num_QD)
Bkg_fiber_use = np.zeros((num_BFP, num_BFP, num_QD))
Bkg_coverslip_use = np.zeros((num_BFP, num_BFP, num_QD))
for l_QD in range(num_QD):
    Bkg_fiber_use[:, :, l_QD] = Bkg_fiber[:, :, l_QD]*fold[l_QD]
    Bkg_coverslip_use[:, :, l_QD] = Bkg_coverslip[:, :, l_QD]*fold[l_QD]

BFP_fiber_rmBkg = BFP_fiber-Bkg_fiber_use
BFP_coverslip_rmBkg = BFP_coverslip-Bkg_coverslip_use
# The radius
lcen = 78.5
lradius_1 = 78
lradius_2 = 78/1.4

print('Begin save the figures')
# Plot the figures
# -----------------------------------------------------------------------------------------------------
# # %%
# for l_QD in range(num_QD):
#     # for l_QD in [1]:
#     vmax_BFP_fiber = np.max(np.sum(BFP_fiber[:, :, l_QD]/num_BFP**2)*3)
#     vmax_Bkg_fiber = np.max(np.sum(Bkg_fiber[:, :, l_QD]/num_BFP**2)*2)
#     vmax_rmBkg_fiber = np.max(np.sum(BFP_fiber_rmBkg[:, :, l_QD]/num_BFP**2)*3)
#     vmax_BFP_coverslip = np.max(np.sum(BFP_coverslip[:, :, l_QD]/num_BFP**2)*3)
#     vmax_Bkg_coverslip = np.max(np.sum(Bkg_coverslip[:, :, l_QD]/num_BFP**2)*2)
#     vmax_rmBkg_coverslip = np.max(
#         np.sum(BFP_coverslip_rmBkg[:, :, l_QD]/num_BFP**2)*3)

#     fig, axs = plt.subplots(2, 3, figsize=(6.4*3, 4.8*2))

#     im1 = axs[0, 0].pcolormesh(
#         BFP_fiber[:, :, l_QD], vmin=0, vmax=vmax_BFP_fiber, cmap='jet', linestyle='--')
#     axs[0, 0].set_xlabel(r'x(pixel)')
#     axs[0, 0].set_ylabel(r'Y(pixel)')
#     axs[0, 0].set_title('original BFP of fiber')
#     circle_1 = patches.Circle((lcen, lcen), lradius_1, linewidth=1,
#                               edgecolor='r', facecolor='none', linestyle='--')
#     circle_2 = patches.Circle((lcen, lcen), lradius_2, linewidth=1,
#                               edgecolor='r', facecolor='none', linestyle='--')
#     axs[0, 0].add_patch(circle_1)
#     axs[0, 0].add_patch(circle_2)
#     fig.colorbar(im1, ax=axs[0, 0])

#     im2 = axs[0, 1].pcolormesh(
#         Bkg_fiber[:, :, l_QD], vmin=0, vmax=vmax_Bkg_fiber, cmap='jet')
#     axs[0, 1].set_xlabel(r'x(pixel)')
#     axs[0, 1].set_ylabel(r'Y(pixel)')
#     axs[0, 1].set_title('Background data of fiber')
#     circle_1 = patches.Circle((lcen, lcen), lradius_1, linewidth=1,
#                               edgecolor='r', facecolor='none', linestyle='--')
#     circle_2 = patches.Circle((lcen, lcen), lradius_2, linewidth=1,
#                               edgecolor='r', facecolor='none', linestyle='--')
#     axs[0, 1].add_patch(circle_1)
#     axs[0, 1].add_patch(circle_2)
#     fig.colorbar(im2, ax=axs[0, 1])

#     im3 = axs[0, 2].pcolormesh(
#         BFP_fiber_rmBkg[:, :, l_QD], vmin=0, vmax=vmax_rmBkg_fiber, cmap='jet')
#     axs[0, 2].set_xlabel(r'x(pixel)')
#     axs[0, 2].set_ylabel(r'Y(pixel)')
#     axs[0, 2].set_title('Processed data of fiber')
#     circle_1 = patches.Circle((lcen, lcen), lradius_1, linewidth=1,
#                               edgecolor='r', facecolor='none', linestyle='--')
#     circle_2 = patches.Circle((lcen, lcen), lradius_2, linewidth=1,
#                               edgecolor='r', facecolor='none', linestyle='--')
#     axs[0, 2].add_patch(circle_1)
#     axs[0, 2].add_patch(circle_2)
#     fig.colorbar(im3, ax=axs[0, 2])

#     im4 = axs[1, 0].pcolormesh(
#         BFP_coverslip[:, :, l_QD], vmin=0, vmax=vmax_BFP_coverslip, cmap='jet', linestyle='--')
#     axs[1, 0].set_xlabel(r'x(pixel)')
#     axs[1, 0].set_ylabel(r'Y(pixel)')
#     axs[1, 0].set_title('original BFP of coverslip')
#     circle_1 = patches.Circle((lcen, lcen), lradius_1, linewidth=1,
#                               edgecolor='r', facecolor='none', linestyle='--')
#     circle_2 = patches.Circle((lcen, lcen), lradius_2, linewidth=1,
#                               edgecolor='r', facecolor='none', linestyle='--')
#     axs[1, 0].add_patch(circle_1)
#     axs[1, 0].add_patch(circle_2)
#     fig.colorbar(im4, ax=axs[1, 0])

#     im5 = axs[1, 1].pcolormesh(
#         Bkg_coverslip[:, :, l_QD], vmin=0, vmax=vmax_Bkg_coverslip, cmap='jet')
#     axs[1, 1].set_xlabel(r'x(pixel)')
#     axs[1, 1].set_ylabel(r'Y(pixel)')
#     axs[1, 1].set_title('Background data of coverslip')
#     circle_1 = patches.Circle((lcen, lcen), lradius_1, linewidth=1,
#                               edgecolor='r', facecolor='none', linestyle='--')
#     circle_2 = patches.Circle((lcen, lcen), lradius_2, linewidth=1,
#                               edgecolor='r', facecolor='none', linestyle='--')
#     axs[1, 1].add_patch(circle_1)
#     axs[1, 1].add_patch(circle_2)
#     fig.colorbar(im5, ax=axs[1, 1])

#     im6 = axs[1, 2].pcolormesh(
#         BFP_coverslip_rmBkg[:, :, l_QD], vmin=0, vmax=vmax_rmBkg_coverslip, cmap='jet')
#     axs[1, 2].set_xlabel(r'x(pixel)')
#     axs[1, 2].set_ylabel(r'Y(pixel)')
#     axs[1, 2].set_title('Processed data of coverslip')
#     circle_1 = patches.Circle((lcen, lcen), lradius_1, linewidth=1,
#                               edgecolor='r', facecolor='none', linestyle='--')
#     circle_2 = patches.Circle((lcen, lcen), lradius_2, linewidth=1,
#                               edgecolor='r', facecolor='none', linestyle='--')
#     axs[1, 2].add_patch(circle_1)
#     axs[1, 2].add_patch(circle_2)
#     fig.colorbar(im6, ax=axs[1, 2])
#     figure_name = './BFP_Image_List/'+file_list_QD_fiber[l_QD]+'.png'
#     fig.savefig(figure_name)
#     # fig.show()
#     plt.close(fig)


for l_QD in range(num_QD):
# for l_QD in [1]:
    vmax_BFP_fiber = np.max(np.sum(BFP_fiber[:, :, l_QD]/num_BFP**2)*3)
    vmax_Bkg_fiber = np.max(np.sum(Bkg_fiber[:, :, l_QD]/num_BFP**2)*2)
    vmax_rmBkg_fiber = np.max(np.sum(BFP_fiber_rmBkg[:, :, l_QD]/num_BFP**2)*3)
    vmax_BFP_coverslip = np.max(np.sum(BFP_coverslip[:, :, l_QD]/num_BFP**2)*3)
    vmax_Bkg_coverslip = np.max(np.sum(Bkg_coverslip[:, :, l_QD]/num_BFP**2)*2)
    vmax_rmBkg_coverslip = np.max(
        np.sum(BFP_coverslip_rmBkg[:, :, l_QD]/num_BFP**2)*3)

    fig, axs = plt.subplots(2, 3, figsize=(6.4*3, 4.8*2))

    im1 = axs[0, 0].pcolormesh(
        BFP_fiber[:, :, l_QD], vmin=0, vmax=vmax_BFP_fiber, cmap='jet', linestyle='--')
    axs[0, 0].set_xlabel(r'x(pixel)')
    axs[0, 0].set_ylabel(r'Y(pixel)')
    axs[0, 0].set_title('original BFP of fiber')
    circle_1 = patches.Circle((lcen, lcen), lradius_1, linewidth=1,
                              edgecolor='r', facecolor='none', linestyle='--')
    circle_2 = patches.Circle((lcen, lcen), lradius_2, linewidth=1,
                              edgecolor='r', facecolor='none', linestyle='--')
    axs[0, 0].add_patch(circle_1)
    axs[0, 0].add_patch(circle_2)
    fig.colorbar(im1, ax=axs[0, 0])

    im2 = axs[0, 1].pcolormesh(
        Bkg_fiber_use[:, :, l_QD], vmin=0, vmax=vmax_BFP_fiber, cmap='jet')
    axs[0, 1].set_xlabel(r'x(pixel)')
    axs[0, 1].set_ylabel(r'Y(pixel)')
    axs[0, 1].set_title('Background data of fiber')
    circle_1 = patches.Circle((lcen, lcen), lradius_1, linewidth=1,
                              edgecolor='r', facecolor='none', linestyle='--')
    circle_2 = patches.Circle((lcen, lcen), lradius_2, linewidth=1,
                              edgecolor='r', facecolor='none', linestyle='--')
    axs[0, 1].add_patch(circle_1)
    axs[0, 1].add_patch(circle_2)
    fig.colorbar(im2, ax=axs[0, 1])

    im3 = axs[0, 2].pcolormesh(
        BFP_fiber_rmBkg[:, :, l_QD], vmin=0, vmax=vmax_BFP_fiber, cmap='jet')
    axs[0, 2].set_xlabel(r'x(pixel)')
    axs[0, 2].set_ylabel(r'Y(pixel)')
    axs[0, 2].set_title('Processed data of fiber')
    circle_1 = patches.Circle((lcen, lcen), lradius_1, linewidth=1,
                              edgecolor='r', facecolor='none', linestyle='--')
    circle_2 = patches.Circle((lcen, lcen), lradius_2, linewidth=1,
                              edgecolor='r', facecolor='none', linestyle='--')
    axs[0, 2].add_patch(circle_1)
    axs[0, 2].add_patch(circle_2)
    fig.colorbar(im3, ax=axs[0, 2])

    im4 = axs[1, 0].pcolormesh(
        BFP_coverslip[:, :, l_QD], vmin=0, vmax=vmax_BFP_coverslip, cmap='jet', linestyle='--')
    axs[1, 0].set_xlabel(r'x(pixel)')
    axs[1, 0].set_ylabel(r'Y(pixel)')
    axs[1, 0].set_title('original BFP of coverslip')
    circle_1 = patches.Circle((lcen, lcen), lradius_1, linewidth=1,
                              edgecolor='r', facecolor='none', linestyle='--')
    circle_2 = patches.Circle((lcen, lcen), lradius_2, linewidth=1,
                              edgecolor='r', facecolor='none', linestyle='--')
    axs[1, 0].add_patch(circle_1)
    axs[1, 0].add_patch(circle_2)
    fig.colorbar(im4, ax=axs[1, 0])

    im5 = axs[1, 1].pcolormesh(
        Bkg_coverslip_use[:, :, l_QD], vmin=0, vmax=vmax_BFP_coverslip, cmap='jet')
    axs[1, 1].set_xlabel(r'x(pixel)')
    axs[1, 1].set_ylabel(r'Y(pixel)')
    axs[1, 1].set_title('Background data of coverslip')
    circle_1 = patches.Circle((lcen, lcen), lradius_1, linewidth=1,
                              edgecolor='r', facecolor='none', linestyle='--')
    circle_2 = patches.Circle((lcen, lcen), lradius_2, linewidth=1,
                              edgecolor='r', facecolor='none', linestyle='--')
    axs[1, 1].add_patch(circle_1)
    axs[1, 1].add_patch(circle_2)
    fig.colorbar(im5, ax=axs[1, 1])

    im6 = axs[1, 2].pcolormesh(
        BFP_coverslip_rmBkg[:, :, l_QD], vmin=0, vmax=vmax_BFP_coverslip, cmap='jet')
    axs[1, 2].set_xlabel(r'x(pixel)')
    axs[1, 2].set_ylabel(r'Y(pixel)')
    axs[1, 2].set_title('Processed data of coverslip')
    circle_1 = patches.Circle((lcen, lcen), lradius_1, linewidth=1,
                              edgecolor='r', facecolor='none', linestyle='--')
    circle_2 = patches.Circle((lcen, lcen), lradius_2, linewidth=1,
                              edgecolor='r', facecolor='none', linestyle='--')
    axs[1, 2].add_patch(circle_1)
    axs[1, 2].add_patch(circle_2)
    fig.colorbar(im6, ax=axs[1, 2])
    figure_name = './BFP_Image_List/'+file_list_QD_fiber[l_QD]+'.png'
    fig.savefig(figure_name)
    #fig.show()
    plt.close(fig)

# %%
# Save the npy data
# for l_QD in range(num_QD):
#     npy_data_name = '../BFP_Image_List/'+file_QD[l_QD]+'.npy'
#     np.save(npy_data_name, BFP_rmBkg[:, :, l_QD])
# npy_data_name = './BFP_Image_List/QD605_20201229_BFP_List.npy'
# np.save(npy_data_name, BFP_rmBkg)
#mat_data_name = './BFP_Image_List/QD605_20210101_BFP_List.mat'
#scio.savemat(mat_data_name, {'BFP_coverslip': BFP_coverslip_rmBkg,'BFP_fiber': BFP_fiber_rmBkg})
