"""
Created on Sat Dec 19 01:43:31 2020

@author: ZhaohuaTian
* Doing superpositions of different BFP
* Find the center of BFP and cut the matrix into a smaller one
* Remove the noise use the method developed in "superposition_picture_and_noise_remove.py" 
"""

import cv2
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import os as os
import matplotlib.patches as patches
import scipy.io as scio
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
file_list_QD = []
file_list_Bkg = []

for file in file_list_c:
    if '.tif' not in file or '.py' in file:
        file_list.remove(file)
        print(file)
    elif 'Bkg' in file:
        if file[6]=='_':
            file_list_Bkg.append(file[0:6])
        else:
            file_list_Bkg.append(file[0:7])
    else:
        if file[8]=='_':
            file_list_QD.append(file[0:8])
        else:
            file_list_QD.append(file[0:9])
# Remove duplicates
file_list_QD = list(dict.fromkeys(file_list_QD))
file_list_Bkg = list(dict.fromkeys(file_list_Bkg))
# file_list_Bkg.remove('Bkg_61')
num_QD = len(file_list_QD)
num_Bkg = len(file_list_Bkg)

if num_QD == num_Bkg:
    print('File list of Bkg and signal is correct !')
else:
    print('File list of Bkg and signal is wrong !')


# (1) Do a superpistion of data for different QDs
# (2) Find the center of different QDs
num_ori = 2048
BFP_ori = np.zeros((num_ori, num_ori, num_QD))
Bkg_ori = np.zeros((num_ori, num_ori, num_QD))
num_BFP = 78*2
num_BFP_half = int(num_BFP/2)
num_approxi = int(400/2)
BFP = np.zeros((num_BFP, num_BFP, num_QD))
Bkg = np.zeros((num_BFP, num_BFP, num_QD))
cen_BFP = np.zeros((num_QD, 3))

# The extra dispalcement of BFP center
dis_x_pos = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                      0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                      0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                      0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                      0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                      0, 0, 0, 0, 0, 0, 0, 0, 0, 0,0])+3
dis_y_pos = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                      0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                      0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                      0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                      0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                      0, 0, 0, 0, 0, 0, 0, 0, 0, 0,0])+6

nb_QD_list=np.zeros(num_QD)
nb_Bkg_list=np.zeros(num_QD)
for l_QD in range(num_QD):
    nb_QD = 0
    nb_Bkg = 0
    for file in file_list:
        if file_list_QD[l_QD] in file:
            nb_QD = nb_QD+1
            Filename = file
            tmp = np.array(plt.imread(Path+Filename))
            BFP_ori[:, :, l_QD] = BFP_ori[:, :, l_QD]+tmp
            circles = find_center(tmp, num_approxi)
            cen_BFP[l_QD, :] = cen_BFP[l_QD, :]+circles[0, 0, :]
        if file_list_Bkg[l_QD] in file:
            nb_Bkg = nb_Bkg+1
            Filename = file
            tmp = np.array(plt.imread(Path+Filename))
            Bkg_ori[:, :, l_QD] = Bkg_ori[:, :, l_QD]+tmp
    nb_QD_list[l_QD]=nb_QD
    nb_Bkg_list[l_QD]=nb_Bkg
    cen_BFP[l_QD, :] = cen_BFP[l_QD, :]/nb_QD
    print('Find center of ', file_list_QD[l_QD], ' at ', cen_BFP[l_QD, :])
    position_x = int(cen_BFP[l_QD, 0]+1024-num_approxi-dis_x_pos[l_QD])
    position_y = int(cen_BFP[l_QD, 1]+1024-num_approxi-dis_y_pos[l_QD])

    BFP[:, :, l_QD] = BFP_ori[position_y-num_BFP_half:position_y +
                              num_BFP_half, position_x-num_BFP_half:position_x+num_BFP_half, l_QD]
    Bkg[:, :, l_QD] = Bkg_ori[position_y-num_BFP_half:position_y +
                              num_BFP_half, position_x-num_BFP_half:position_x+num_BFP_half, l_QD]

# # %%
# # vmax =np.max(np.sum(BFP/num_BFP**2)*1.5)
# # fig1=plt.figure()
# # plt.imshow(BFP[:,:,0],cmap='jet',vmin=0,vmax=vmax)
# # plt.show()
## Show the numer of QD BFP and background
# %%
fig1=plt.figure()
plt.plot(nb_QD_list,label='number of pictures for QD BFP')
plt.plot(nb_Bkg_list,label='number of pictures for Background')
plt.grid()
plt.legend(loc='best')
plt.savefig('./BFP_Image_List/numberoffilesofBFPandBkg.png')
# plt.show()
# %% The ratio to use
fold = np.ones(num_QD)
Bkg_use = np.zeros((num_BFP, num_BFP, num_QD))
for l_QD in range(num_QD):
    Bkg_use[:, :, l_QD] = Bkg[:, :, l_QD]*fold[l_QD]

BFP_rmBkg = BFP-Bkg_use

# The radius
lcen=78.5
lradius_1=78
lradius_2=78/1.4

print('Begin save the figures')
# Plot the figures
# -----------------------------------------------------------------------------------------------------
# %%
for l_QD in range(num_QD):
#for l_QD in [1]:
    vmax = np.max(np.sum(BFP[:, :, l_QD]/num_BFP**2)*3)
    vmax_Bkg = np.max(np.sum(Bkg[:, :, l_QD]/num_BFP**2)*2)
    vmax_rmBkg = np.max(np.sum(BFP_rmBkg[:, :, l_QD]/num_BFP**2)*3)
    fig, axs = plt.subplots(1, 3, figsize=(6.4*3, 4.8))

    im1 = axs[0].pcolormesh(
        BFP[:, :, l_QD], vmin=0, vmax=vmax, cmap='jet', linestyle='--')
    axs[0].set_xlabel(r'x(pixel)')
    axs[0].set_ylabel(r'Y(pixel)')
    axs[0].set_title('original BFP')
    circle_1 = patches.Circle((lcen, lcen), lradius_1, linewidth=1,
                            edgecolor='r', facecolor='none', linestyle='--')
    circle_2 = patches.Circle((lcen, lcen), lradius_2, linewidth=1,
                            edgecolor='r', facecolor='none', linestyle='--')
    axs[0].add_patch(circle_1)
    axs[0].add_patch(circle_2)
    fig.colorbar(im1, ax=axs[0])

    im2 = axs[1].pcolormesh(
        Bkg[:, :, l_QD], vmin=0, vmax=vmax_Bkg, cmap='jet')
    axs[1].set_xlabel(r'x(pixel)')
    axs[1].set_ylabel(r'Y(pixel)')
    axs[1].set_title('Background data')
    circle_1 = patches.Circle((lcen, lcen), lradius_1, linewidth=1,
                            edgecolor='r', facecolor='none', linestyle='--')
    circle_2 = patches.Circle((lcen, lcen), lradius_2, linewidth=1,
                            edgecolor='r', facecolor='none', linestyle='--')
    axs[1].add_patch(circle_1)
    axs[1].add_patch(circle_2)
    fig.colorbar(im2, ax=axs[1])

    im3 = axs[2].pcolormesh(
        BFP_rmBkg[:, :, l_QD], vmin=0, vmax=vmax_rmBkg, cmap='jet')
    axs[2].set_xlabel(r'x(pixel)')
    axs[2].set_ylabel(r'Y(pixel)')
    axs[2].set_title('Processed data')
    circle_1 = patches.Circle((lcen, lcen), lradius_1, linewidth=1,
                            edgecolor='r', facecolor='none', linestyle='--')
    circle_2 = patches.Circle((lcen, lcen), lradius_2, linewidth=1,
                            edgecolor='r', facecolor='none', linestyle='--')
    axs[2].add_patch(circle_1)
    axs[2].add_patch(circle_2)
    fig.colorbar(im3, ax=axs[2])
    figure_name = './BFP_Image_List/'+file_list_QD[l_QD]+'.png'
    fig.savefig(figure_name)
    #fig.show()
    plt.close(fig)

# %%
# Save the npy data
# for l_QD in range(num_QD):
#     npy_data_name = '../BFP_Image_List/'+file_QD[l_QD]+'.npy'
#     np.save(npy_data_name, BFP_rmBkg[:, :, l_QD])
npy_data_name = './BFP_Image_List/QD605_20201229_BFP_List.npy'
np.save(npy_data_name, BFP_rmBkg)
mat_data_name = './BFP_Image_List/QD605_20201229_BFP_List.mat'
scio.savemat(mat_data_name, {'BFP':BFP_rmBkg})