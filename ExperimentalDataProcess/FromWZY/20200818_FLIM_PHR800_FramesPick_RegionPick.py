# -*- coding: utf-8 -*-
"""
Created on Tue Aug 18 21:54:09 2020

@author: Administrator
"""

import numpy as np
import matplotlib.pylab as plt
import os as os
import ToolBox_V3 as TB
#import datetime


def make_hist(x, bin_size):
    [hist, hist_ax] = np.histogram(x, int(np.ceil(np.max(x) / bin_size)), range=[np.min(x) + 60e-12, np.max(x)])  # ]
    return hist_ax[:-1], hist


def Bin_Pho_Str(photon_stream, bin_time):
    n = 1
    count = 0
    Inten = []
    time = []
    ii = 0
    while 1:
        if (photon_stream[ii] >= photon_stream[0] + (n - 1) * bin_time) & (photon_stream[ii] < photon_stream[0] + n * bin_time):
            count = count + 1
            ii = ii + 1
        else:
            Inten.append(count)
            time.append(photon_stream[0] + (n - 1) * bin_time)
            count = 0
            n = n + 1
        if ii == len(photon_stream) - 1:
            break
    Inten = np.array(Inten)
    time = np.array(time)
    return time, Inten


#####################################################################################################################################
Path_JPK = os.getcwd() + '\\Data_Picoharp_PHR\\'
Path_Fig = os.getcwd() + '\\Figures\\'
Path_Txt = os.getcwd() + '\\Data_txt\\'


############################# Settings ##################################
Filename = 'FLIM_01_QD650_013.ptu'
x_dim = 128  ## pixel number in x direction
y_dim = 128  ## pixel number in y direction
is_bottom_up =0 ## 0 if the first frameis bottom-up after TCSPC has started recording ; 1 if the first frame is top-down
do_plotframes = 1   ## 1 if plot for every frame
do_normframes = 0   ## 1 if normalize for every frame. Note: This setting does not influence the normalization for 'sumframe' Int and LT

### define the picked region for bg for normalization
bg_pick=5   ## [0:bg_pick, 0:y_dim]&[(x_dim-bg_pick):x_dim, 0:y_dim]

### define the picked out time region for bg LT for normalization
t_rise=3.0
t_fast=0.0

### define the picked region for extracting lifetime curve 
up_pick = y_dim  ## index of the upperbound in y-direction
down_pick = 0  ## index of the lowerbound in y-direction
right_pick = 10  ## index of the upperbound in x-direction
left_pick = 0  ## index of the lowerbound in x-direction

###
## when the photon counts of a pixel < threshold_blink, we consider it in dark-state.
## threshold_blink may be set as 0.3*(Flim_Int_Ch4_bg_meanframes)
threshold_blink = 0.3*8 
############################################################################
Rec             = TB.Read_PHR800_T3(Path_JPK+Filename)
#MacroTime_m_Chan_4=Rec.event_macrotime_Chan_4[((Rec.event_type==1)&(Rec.event_chan==4))]
#MicroTime_m_Chan_4=Rec.event_microtime_Chan_4[((Rec.event_type==1)&(Rec.event_chan==4))]


MacroTime_Ch1 = Rec.event_MacroTime[Rec.event_chan == 1]
MacroTime_Ch2 = Rec.event_MacroTime[Rec.event_chan == 2]
MacroTime_Ch3 = Rec.event_MacroTime[Rec.event_chan == 3]
MacroTime_Ch4 = Rec.event_MacroTime[Rec.event_chan == 4]

MicroTime_Ch1 = Rec.event_MicroTime[Rec.event_chan == 1]
MicroTime_Ch2 = Rec.event_MicroTime[Rec.event_chan == 2]
MicroTime_Ch3 = Rec.event_MicroTime[Rec.event_chan == 3]
MicroTime_Ch4 = Rec.event_MicroTime[Rec.event_chan == 4]
#
MacroTime_framemark = Rec.event_MacroTime[Rec.event_type == 3]
MacroTime_linemark = Rec.event_MacroTime[Rec.event_type == 4]
MacroTime_pixelmark =Rec.event_MacroTime[Rec.event_type == 5]


#MacroTime_framemark = Rec.frame_m
#MacroTime_linemark = Rec.line_m
#MacroTime_pixelmark =Rec.pixel_m


dt = MacroTime_pixelmark[3] - MacroTime_pixelmark[2]
###########################################################################################################################################################################

bin_time = Rec.microtime_res * 1e9
#bin_time =Rec.microtime_res
[time_LT_Ch4, Inten_LT_Ch4] = make_hist(MicroTime_Ch4, bin_time)
posi_Ch4 = np.where(Inten_LT_Ch4 == np.max(Inten_LT_Ch4))[0][0]
zero_line_Ch4 = time_LT_Ch4[posi_Ch4]

###################################################################################################
F2 = plt.figure()
F2ax1 = F2.add_subplot(111)
F2ax1.plot(Rec.event_MacroTime[Rec.event_type == 5] / 1e9, Rec.event_MacroTime[Rec.event_type == 5] / 1e9, 'bx', markersize=10, label='pixels')
F2ax1.plot(Rec.event_MacroTime[Rec.event_type== 4] / 1e9, Rec.event_MacroTime[Rec.event_type == 4] / 1e9, 'go', label='linestop')
F2ax1.plot(Rec.event_MacroTime[Rec.event_type == 3] / 1e9, Rec.event_MacroTime[Rec.event_type == 3] / 1e9, 'ro', lw='25', label='frame')
F2ax1.set_title('Marker positions')
F2ax1.set_xlabel('time (s)')
F2ax1.set_ylabel('time (s)')
F2ax1.legend(loc='best')
F2.show()
#F2.savefig(Path_Fig + Filename + 'mark.png')


########################################################################################################################################################
Flim_Int_tr_Ch4_frame = np.zeros([y_dim, x_dim])  #ndarray
Flim_Int_tr_Ch4_sumframes = np.zeros([y_dim, x_dim])
Flim_Int_tr_Ch4_sumframes_nbright = np.zeros([y_dim, x_dim])  ## number of bright frames. Int_mean=Int/num

Flim_LT_tr_Ch4_delay_num_frame = np.zeros([y_dim, x_dim])
Flim_LT_tr_Ch4_delay_sum_frame = np.zeros([y_dim, x_dim])
Flim_LT_tr_Ch4_delay_num_sumframes = np.zeros([y_dim, x_dim])
Flim_LT_tr_Ch4_delay_sum_sumframes = np.zeros([y_dim, x_dim])

Flim_Int_retr_Ch4_frame = np.zeros([y_dim, x_dim])
Flim_Int_retr_Ch4_sumframes = np.zeros([y_dim, x_dim])
Flim_Int_retr_Ch4_sumframes_nbright = np.zeros([y_dim, x_dim])  ## number of bright frames. Int_mean=Int/num

Flim_LT_retr_Ch4_delay_num_frame = np.zeros([y_dim, x_dim])
Flim_LT_retr_Ch4_delay_sum_frame = np.zeros([y_dim, x_dim])
Flim_LT_retr_Ch4_delay_num_sumframes = np.zeros([y_dim, x_dim])
Flim_LT_retr_Ch4_delay_sum_sumframes = np.zeros([y_dim, x_dim])

MicroTime_Ch4_bottomup_tr_pick = [] #list
MicroTime_Ch4_bottomup_retr_pick = []
MicroTime_Ch4_topdown_tr_pick = []
MicroTime_Ch4_topdown_retr_pick = []

########################################################################################################################
############################################################

num_mm = range(len(MacroTime_framemark) - 1)
#num_mm = [1,2,3,4,5,6]   #FLIM_04_QD605_001
#num_mm = [0,1,2,3,5,6]    #FLIM_04_QD605_002
#num_mm = [0,1,2,3]    #FLIM_04_QD605_006
#num_mm = [0,2,3,4,5]    #FLIM_04_QD605_009
#num_mm = [0,1,2,3,5]    #FLIM_04_QD605_010
#num_mm = [0,1,2,4,5]    #FLIM_04_QD605_016
#num_mm = [0,1,2,3,4]    #FLIM_04_QD605_018
#num_mm = [0,1,2,4,5]    #FLIM_04_QD605_021
#num_mm = [0,1,2,4,5,7]    #FLIM_04_QD605_024
#num_mm = [0,1,3,4,5]    #FLIM_04_QD605_028
num_mm = [2,3,4,5,6,7]    #FLIM_01_QD650_013






for ll in range(len(num_mm)):
    mm = num_mm[ll]

    if np.mod(mm, 2) == is_bottom_up:     # this frame is bottom-up

        # to make processing fast, re-store subset of data, named as "xxx_frame, xxx_line, xxx_pixel"
        MacroTime_frame=Rec.event_MacroTime[(Rec.event_MacroTime > MacroTime_framemark[mm]) & (Rec.event_MacroTime <= MacroTime_framemark[mm + 1])]
        Event_type_frame = Rec.event_type[(Rec.event_MacroTime > MacroTime_framemark[mm]) & (Rec.event_MacroTime <= MacroTime_framemark[mm + 1])]
        MacroTime_Ch4_frame = MacroTime_Ch4[(MacroTime_Ch4 > MacroTime_framemark[mm]) & (MacroTime_Ch4 <= MacroTime_framemark[mm + 1])]
        MicroTime_Ch4_frame = MicroTime_Ch4[(MacroTime_Ch4 > MacroTime_framemark[mm]) & (MacroTime_Ch4 <= MacroTime_framemark[mm + 1])]
        MacroTime_pixelmark_frame = MacroTime_pixelmark[(MacroTime_pixelmark > MacroTime_framemark[mm]) & (MacroTime_pixelmark <= MacroTime_framemark[mm + 1])]


        cnt_tr = -1  # the index 'cnt_tr' indicats the index of the current trace line
        cnt_retr = -1  # the index 'cnt_retr' indicats the index of the current retrace line
        for ii in range(2 * y_dim):

            pixels_times_line = np.ones(x_dim + 1) * 0
            for jjj in range(x_dim+1):
                jj = x_dim * ii + jjj
                if jjj == 0:
                    pixels_times_line[0] = MacroTime_pixelmark_frame[jj] - dt
                else:
                    pixels_times_line[jjj] = MacroTime_pixelmark_frame[jj - 1]

            # to make processing fast, re-store subset of data, named as "xxx_frame, xxx_line, xxx_pixel"
            MacroTime_line = MacroTime_frame[(MacroTime_frame >= (pixels_times_line[0] - dt)) & (MacroTime_frame <= pixels_times_line[x_dim])]
            Event_type_line = Event_type_frame[(MacroTime_frame >= (pixels_times_line[0] - dt)) & (MacroTime_frame <= pixels_times_line[x_dim])]
            MacroTime_Ch4_line = MacroTime_Ch4_frame[(MacroTime_Ch4_frame >= (pixels_times_line[0] - dt)) & (MacroTime_Ch4_frame <= pixels_times_line[x_dim])]
            MicroTime_Ch4_line = MicroTime_Ch4_frame[(MacroTime_Ch4_frame >= (pixels_times_line[0] - dt)) & (MacroTime_Ch4_frame <= pixels_times_line[x_dim])]
            #MacroTime_pixelmark_line = MacroTime_pixelmark_frame[(MacroTime_pixelmark_frame >= pixels_times_line[0] - dt) & (MacroTime_pixelmark_frame <= pixels_times_line[x_dim])]

            if np.mod(ii, 2) == 0:  # ii is even means this is trace
                cnt_tr = cnt_tr + 1
                for iii in range(1,x_dim+1):

                    # to make processing fast, re-store subset of data, named as "xxx_frame, xxx_line, xxx_pixel"
                    MacroTime_pixel = MacroTime_line[(MacroTime_line >= pixels_times_line[iii - 1]) & (MacroTime_line <= pixels_times_line[iii])]
                    Event_type_pixel = Event_type_line[(MacroTime_line >= pixels_times_line[iii - 1]) & (MacroTime_line <= pixels_times_line[iii])]
                    MacroTime_Ch4_pixel = MacroTime_Ch4_line[(MacroTime_Ch4_line >= pixels_times_line[iii - 1]) & (MacroTime_Ch4_line <= pixels_times_line[iii])]
                    MicroTime_Ch4_pixel = MicroTime_Ch4_line[(MacroTime_Ch4_line >= pixels_times_line[iii - 1]) & (MacroTime_Ch4_line <= pixels_times_line[iii])]

                    Flim_Int_tr_Ch4_frame[cnt_tr, iii - 1] = Event_type_pixel[Event_type_pixel == 1].shape[0]   # the intensity is the sum of photon events (event type==1)
                    if Flim_Int_tr_Ch4_frame[cnt_tr, iii - 1] >= threshold_blink:
                        Flim_Int_tr_Ch4_sumframes[cnt_tr, iii - 1] = Flim_Int_tr_Ch4_frame[cnt_tr, iii - 1] + Flim_Int_tr_Ch4_sumframes[cnt_tr, iii - 1]
                        Flim_Int_tr_Ch4_sumframes_nbright[cnt_tr, iii - 1] = Flim_Int_tr_Ch4_sumframes_nbright[cnt_tr, iii - 1] + 1

                    # photon events with MicroTime > (zero_line + t_fast)
                    delay_Ch4_pixel_right = MicroTime_Ch4_pixel[MicroTime_Ch4_pixel > (zero_line_Ch4 + t_fast)] - zero_line_Ch4
                    # phtons events with MicroTime < (zero_line - t_rise)
                    delay_Ch4_pixel_left = MicroTime_Ch4_pixel[MicroTime_Ch4_pixel < (zero_line_Ch4 - t_rise)] - zero_line_Ch4 + Rec.syncperiod

                    delay_Ch4_pixel = np.append(delay_Ch4_pixel_right, delay_Ch4_pixel_left)
                    
                    Flim_LT_tr_Ch4_delay_num_frame[cnt_tr, iii - 1] = len(delay_Ch4_pixel)
                    Flim_LT_tr_Ch4_delay_sum_frame[cnt_tr, iii - 1] = np.nansum(delay_Ch4_pixel)
                    
                    if Flim_Int_tr_Ch4_frame[cnt_tr, iii - 1] >= threshold_blink:   ## when the pixel is considered bright
                        Flim_LT_tr_Ch4_delay_num_sumframes[cnt_tr, iii - 1] = Flim_LT_tr_Ch4_delay_num_sumframes[cnt_tr, iii - 1] + Flim_LT_tr_Ch4_delay_num_frame[cnt_tr, iii - 1]
                        Flim_LT_tr_Ch4_delay_sum_sumframes[cnt_tr, iii - 1] = Flim_LT_tr_Ch4_delay_sum_sumframes[cnt_tr, iii - 1] + Flim_LT_tr_Ch4_delay_sum_frame[cnt_tr, iii - 1]

                    if ((ii < 2 * up_pick) & (ii > 2 * down_pick)) & ((iii < right_pick) & (iii > left_pick)):
                        MicroTime_Ch4_bottomup_tr_pick.extend(MicroTime_Ch4_pixel)

            else:  # ii is odd means this is retrace
                cnt_retr = cnt_retr + 1
                for iii in range(1,x_dim+1):

                    # to make processing fast, re-store subset of data, named as "xxx_frame, xxx_line, xxx_pixel"
                    MacroTime_pixel = MacroTime_line[(MacroTime_line >= pixels_times_line[iii - 1]) & (MacroTime_line <= pixels_times_line[iii])]
                    Event_type_pixel = Event_type_line[(MacroTime_line >= pixels_times_line[iii - 1]) & (MacroTime_line <= pixels_times_line[iii])]
                    MacroTime_Ch4_pixel = MacroTime_Ch4_line[(MacroTime_Ch4_line >= pixels_times_line[iii - 1]) & (MacroTime_Ch4_line <= pixels_times_line[iii])]
                    MicroTime_Ch4_pixel = MicroTime_Ch4_line[(MacroTime_Ch4_line >= pixels_times_line[iii - 1]) & (MacroTime_Ch4_line <= pixels_times_line[iii])]

                    Flim_Int_retr_Ch4_frame[cnt_retr, x_dim - iii] = Event_type_pixel[Event_type_pixel == 1].shape[0]   # the intensity is the sum of photon events (event type==1)
                    if Flim_Int_retr_Ch4_frame[cnt_retr, x_dim - iii] >= threshold_blink:
                        Flim_Int_retr_Ch4_sumframes[cnt_retr, x_dim - iii] = Flim_Int_retr_Ch4_frame[cnt_retr, x_dim - iii] + Flim_Int_retr_Ch4_sumframes[cnt_retr, x_dim - iii]
                        Flim_Int_retr_Ch4_sumframes_nbright[cnt_retr, x_dim - iii] = Flim_Int_retr_Ch4_sumframes_nbright[cnt_retr, x_dim - iii] + 1

                    # photon events with MicroTime > (zero_line + t_fast)
                    delay_Ch4_pixel_right = MicroTime_Ch4_pixel[MicroTime_Ch4_pixel > (zero_line_Ch4 + t_fast)] - zero_line_Ch4
                    # phtons events with MicroTime < (zero_line - t_rise)
                    delay_Ch4_pixel_left = MicroTime_Ch4_pixel[MicroTime_Ch4_pixel < (zero_line_Ch4 - t_rise)] - zero_line_Ch4 + Rec.syncperiod

                    delay_Ch4_pixel = np.append(delay_Ch4_pixel_right, delay_Ch4_pixel_left)
                    
                    Flim_LT_retr_Ch4_delay_num_frame[cnt_retr, x_dim - iii] = len(delay_Ch4_pixel)
                    Flim_LT_retr_Ch4_delay_sum_frame[cnt_retr, x_dim - iii] = np.nansum(delay_Ch4_pixel)
                    
                    if Flim_Int_retr_Ch4_frame[cnt_retr, x_dim - iii] >= threshold_blink:
                        Flim_LT_retr_Ch4_delay_num_sumframes[cnt_retr, x_dim - iii] = Flim_LT_retr_Ch4_delay_num_sumframes[cnt_retr, x_dim - iii] + Flim_LT_retr_Ch4_delay_num_frame[cnt_retr, x_dim - iii]
                        Flim_LT_retr_Ch4_delay_sum_sumframes[cnt_retr, x_dim - iii] = Flim_LT_retr_Ch4_delay_sum_sumframes[cnt_retr, x_dim - iii] + Flim_LT_retr_Ch4_delay_sum_frame[cnt_retr, x_dim - iii]

                    if ((ii < 2 * up_pick) & (ii > 2 * down_pick)) & ((iii < right_pick) & (iii > left_pick)):
                        MicroTime_Ch4_bottomup_retr_pick.extend(MicroTime_Ch4_pixel)
                        
    else:  # this frame is top-down

        # to make processing fast, re-store subset of data, named as "xxx_frame, xxx_line, xxx_pixel"
        MacroTime_frame = Rec.event_MacroTime[(Rec.event_MacroTime > MacroTime_framemark[mm]) & (Rec.event_MacroTime <= MacroTime_framemark[mm + 1])]
        Event_type_frame = Rec.event_type[(Rec.event_MacroTime > MacroTime_framemark[mm]) & (Rec.event_MacroTime <= MacroTime_framemark[mm + 1])]
        MacroTime_Ch4_frame = MacroTime_Ch4[(MacroTime_Ch4 > MacroTime_framemark[mm]) & (MacroTime_Ch4 <= MacroTime_framemark[mm + 1])]
        MicroTime_Ch4_frame = MicroTime_Ch4[(MacroTime_Ch4 > MacroTime_framemark[mm]) & (MacroTime_Ch4 <= MacroTime_framemark[mm + 1])]
        MacroTime_pixelmark_frame = MacroTime_pixelmark[(MacroTime_pixelmark > MacroTime_framemark[mm]) & (MacroTime_pixelmark <= MacroTime_framemark[mm + 1])]

        cnt_tr = -1  # the index 'cnt_tr' indicats the index of the current trace line
        cnt_retr = -1  # the index 'cnt_retr' indicats the index of the current retrace line
        for ii in range(2 * y_dim):

            pixels_times_line = np.ones(x_dim + 1) * 0
            for jjj in range(x_dim + 1):
                jj = x_dim * ii + jjj
                if jjj == 0:
                    pixels_times_line[0] = MacroTime_pixelmark_frame[jj] - dt
                else:
                    pixels_times_line[jjj] = MacroTime_pixelmark_frame[jj - 1]

            # to make processing fast, re-store subset of data, named as "xxx_frame, xxx_line, xxx_pixel"
            MacroTime_line = MacroTime_frame[(MacroTime_frame >= pixels_times_line[0] - dt) & (MacroTime_frame <= pixels_times_line[x_dim])]
            Event_type_line = Event_type_frame[(MacroTime_frame >= pixels_times_line[0] - dt) & (MacroTime_frame <= pixels_times_line[x_dim])]
            MacroTime_Ch4_line = MacroTime_Ch4_frame[(MacroTime_Ch4_frame >= (pixels_times_line[0] - dt)) & (MacroTime_Ch4_frame <= pixels_times_line[x_dim])]
            MicroTime_Ch4_line = MicroTime_Ch4_frame[(MacroTime_Ch4_frame >= (pixels_times_line[0] - dt)) & (MacroTime_Ch4_frame <= pixels_times_line[x_dim])]
            # MacroTime_pixelmark_line = MacroTime_pixelmark_frame[(MacroTime_pixelmark_frame >= pixels_times_line[0] - dt) & (MacroTime_pixelmark_frame <= pixels_times_line[x_dim])]

            if np.mod(ii, 2) == 0:  # ii is even means this is trace
                cnt_tr = cnt_tr + 1
                for iii in range(1, x_dim + 1):

                    # to make processing fast, re-store subset of data, named as "xxx_frame, xxx_line, xxx_pixel"
                    MacroTime_pixel = MacroTime_line[(MacroTime_line >= pixels_times_line[iii - 1]) & (MacroTime_line <= pixels_times_line[iii])]
                    Event_type_pixel = Event_type_line[(MacroTime_line >= pixels_times_line[iii - 1]) & (MacroTime_line <= pixels_times_line[iii])]
                    MacroTime_Ch4_pixel = MacroTime_Ch4_line[(MacroTime_Ch4_line >= pixels_times_line[iii - 1]) & (MacroTime_Ch4_line <= pixels_times_line[iii])]
                    MicroTime_Ch4_pixel = MicroTime_Ch4_line[(MacroTime_Ch4_line >= pixels_times_line[iii - 1]) & (MacroTime_Ch4_line <= pixels_times_line[iii])]

                    Flim_Int_tr_Ch4_frame[ y_dim - cnt_tr - 1, iii - 1] = Event_type_pixel[Event_type_pixel == 1].shape[0]  # the intensity is the sum of photon events (event type==1)
                    if Flim_Int_tr_Ch4_frame[ y_dim - cnt_tr - 1, iii - 1] >= threshold_blink:
                        Flim_Int_tr_Ch4_sumframes[ y_dim - cnt_tr - 1, iii - 1] = Flim_Int_tr_Ch4_frame[ y_dim - cnt_tr - 1, iii - 1] + Flim_Int_tr_Ch4_sumframes[ y_dim - cnt_tr - 1, iii - 1]
                        Flim_Int_tr_Ch4_sumframes_nbright[ y_dim - cnt_tr - 1, iii - 1] = Flim_Int_tr_Ch4_sumframes_nbright[ y_dim - cnt_tr - 1, iii - 1] + 1

                    # photon events with MicroTime > (zero_line + t_fast)
                    delay_Ch4_pixel_right = MicroTime_Ch4_pixel[MicroTime_Ch4_pixel > (zero_line_Ch4 + t_fast)] - zero_line_Ch4
                    # phtons events with MicroTime < (zero_line - t_rise)
                    delay_Ch4_pixel_left = MicroTime_Ch4_pixel[MicroTime_Ch4_pixel < (zero_line_Ch4 - t_rise)] - zero_line_Ch4 + Rec.syncperiod

                    delay_Ch4_pixel = np.append(delay_Ch4_pixel_right, delay_Ch4_pixel_left)
                    
                    Flim_LT_tr_Ch4_delay_num_frame[ y_dim - cnt_tr - 1, iii - 1] = len(delay_Ch4_pixel)
                    Flim_LT_tr_Ch4_delay_sum_frame[ y_dim - cnt_tr - 1, iii - 1] = np.nansum(delay_Ch4_pixel)
                    
                    if Flim_Int_tr_Ch4_frame[ y_dim - cnt_tr - 1, iii - 1] >= threshold_blink:
                        Flim_LT_tr_Ch4_delay_num_sumframes[ y_dim - cnt_tr - 1, iii - 1] = Flim_LT_tr_Ch4_delay_num_sumframes[ y_dim - cnt_tr - 1, iii - 1] + Flim_LT_tr_Ch4_delay_num_frame[ y_dim - cnt_tr - 1, iii - 1]
                        Flim_LT_tr_Ch4_delay_sum_sumframes[ y_dim - cnt_tr - 1, iii - 1] = Flim_LT_tr_Ch4_delay_sum_sumframes[ y_dim - cnt_tr - 1, iii - 1] + Flim_LT_tr_Ch4_delay_sum_frame[ y_dim - cnt_tr - 1, iii - 1]

                    if ((ii < 2 * up_pick) & (ii > 2 * down_pick)) & ((iii < right_pick) & (iii > left_pick)):
                        MicroTime_Ch4_topdown_tr_pick.extend(MicroTime_Ch4_pixel)

            else:  # ii is odd means this is retrace
                cnt_retr = cnt_retr + 1
                for iii in range(1, x_dim + 1):

                    # to make processing fast, re-store subset of data, named as "xxx_frame, xxx_line, xxx_pixel"
                    MacroTime_pixel = MacroTime_line[(MacroTime_line >= pixels_times_line[iii - 1]) & (MacroTime_line <= pixels_times_line[iii])]
                    Event_type_pixel = Event_type_line[(MacroTime_line >= pixels_times_line[iii - 1]) & (MacroTime_line <= pixels_times_line[iii])]
                    MacroTime_Ch4_pixel = MacroTime_Ch4_line[(MacroTime_Ch4_line >= pixels_times_line[iii - 1]) & (MacroTime_Ch4_line <= pixels_times_line[iii])]
                    MicroTime_Ch4_pixel = MicroTime_Ch4_line[(MacroTime_Ch4_line >= pixels_times_line[iii - 1]) & (MacroTime_Ch4_line <= pixels_times_line[iii])]

                    Flim_Int_retr_Ch4_frame[ y_dim - cnt_retr - 1, x_dim - iii] = Event_type_pixel[Event_type_pixel == 1].shape[0]  # the intensity is the sum of photon events (event type==1)
                    if Flim_Int_retr_Ch4_frame[ y_dim - cnt_retr - 1, x_dim - iii] >= threshold_blink:
                        Flim_Int_retr_Ch4_sumframes[y_dim - cnt_retr - 1, x_dim - iii] = Flim_Int_retr_Ch4_frame[y_dim - cnt_retr - 1, x_dim - iii] + Flim_Int_retr_Ch4_sumframes[y_dim - cnt_retr - 1, x_dim - iii]
                        Flim_Int_retr_Ch4_sumframes_nbright[y_dim - cnt_retr - 1, x_dim - iii] = Flim_Int_retr_Ch4_sumframes_nbright[y_dim - cnt_retr - 1, x_dim - iii] + 1

                    # photon events with MicroTime > (zero_line + t_fast)
                    delay_Ch4_pixel_right = MicroTime_Ch4_pixel[MicroTime_Ch4_pixel > (zero_line_Ch4 + t_fast)] - zero_line_Ch4
                    # phtons events with MicroTime < (zero_line - t_rise)
                    delay_Ch4_pixel_left = MicroTime_Ch4_pixel[MicroTime_Ch4_pixel < (zero_line_Ch4 - t_rise)] - zero_line_Ch4 + Rec.syncperiod

                    delay_Ch4_pixel=np.append(delay_Ch4_pixel_right,delay_Ch4_pixel_left)

                    Flim_LT_retr_Ch4_delay_num_frame[y_dim - cnt_retr - 1, x_dim - iii] = len(delay_Ch4_pixel)
                    Flim_LT_retr_Ch4_delay_sum_frame[y_dim - cnt_retr - 1, x_dim - iii] = np.nansum(delay_Ch4_pixel)

                    if Flim_Int_retr_Ch4_frame[ y_dim - cnt_retr - 1, x_dim - iii] >= threshold_blink:
                        Flim_LT_retr_Ch4_delay_num_sumframes[y_dim - cnt_retr - 1, x_dim - iii] = Flim_LT_retr_Ch4_delay_num_sumframes[y_dim - cnt_retr - 1, x_dim - iii] + Flim_LT_retr_Ch4_delay_num_frame[y_dim - cnt_retr - 1, x_dim - iii]
                        Flim_LT_retr_Ch4_delay_sum_sumframes[y_dim - cnt_retr - 1, x_dim - iii] = Flim_LT_retr_Ch4_delay_sum_sumframes[y_dim - cnt_retr - 1, x_dim - iii] + Flim_LT_retr_Ch4_delay_sum_frame[y_dim - cnt_retr - 1, x_dim - iii]

                    if ((ii < 2 * up_pick) & (ii > 2 * down_pick)) & ((iii < right_pick) & (iii > left_pick)):
                        MicroTime_Ch4_topdown_retr_pick.extend(MicroTime_Ch4_pixel)

    ######################################################################################################
    Flim_LT_tr_Ch4_frame = Flim_LT_tr_Ch4_delay_sum_frame / Flim_LT_tr_Ch4_delay_num_frame
    Flim_LT_retr_Ch4_frame = Flim_LT_retr_Ch4_delay_sum_frame / Flim_LT_retr_Ch4_delay_num_frame
    
    if do_plotframes:  
        
        F5 = plt.figure()
        F5ax1 = F5.add_subplot(111)
        map = F5ax1.pcolorfast(Flim_LT_tr_Ch4_frame)
        F5col_bar = F5.colorbar(map)
        F5ax1.set_title('trace' + str(mm))
        F5ax1.set_xlabel(r'x (pixel)')
        F5ax1.set_xlabel(r'y (pixel)')
        # F5.show()
        F5.savefig(Path_Fig +'1_'+ Filename + '_LT_frame_' + str(mm) + '_trace.png')

        F5 = plt.figure()
        F5ax1 = F5.add_subplot(111)
        map = F5ax1.pcolorfast(Flim_LT_retr_Ch4_frame)
        F5col_bar = F5.colorbar(map)
        F5ax1.set_title('retrace' + str(mm))
        F5ax1.set_xlabel(r'x (pixel)')
        F5ax1.set_xlabel(r'y (pixel)')
        # F5.show()
        F5.savefig(Path_Fig +'1_'+ Filename + '_LT_frame_' + str(mm) + '_retrace.png')

        ########################################################################################################
        F5 = plt.figure()
        F5ax1 = F5.add_subplot(111)
        map = F5ax1.pcolorfast(Flim_Int_tr_Ch4_frame)
        F5col_bar = F5.colorbar(map)
        F5ax1.set_title('trace' + str(mm))
        F5ax1.set_xlabel(r'x (pixel)')
        F5ax1.set_xlabel(r'y (pixel)')
        # F5.show()
        F5.savefig(Path_Fig +'1_'+ Filename + '_Int_frame_' + str(mm) + '_trace_.png')

        F5 = plt.figure()
        F5ax1 = F5.add_subplot(111)
        map = F5ax1.pcolorfast(Flim_Int_retr_Ch4_frame)
        F5col_bar = F5.colorbar(map)
        F5ax1.set_title('retrace' + str(mm))
        F5ax1.set_xlabel(r'x (pixel)')
        F5ax1.set_xlabel(r'y (pixel)')
        # F5.show()
        F5.savefig(Path_Fig +'1_'+ Filename + '_Int_frame_' + str(mm) + '_retrace.png')

        if do_normframes:
            ## normalization of Int and LT of the frame
    
            # trace
            temp1=Flim_Int_tr_Ch4_frame[0:bg_pick, 0:y_dim]
            temp2=Flim_Int_tr_Ch4_frame[(x_dim-bg_pick):x_dim, 0:y_dim]
            temp_Int=np.hstack((temp1,temp2))
            Flim_Int_tr_Ch4_bg_frame = np.mean(temp_Int)  # the bg for PL intensity normalization
    
            temp1=Flim_LT_tr_Ch4_delay_sum_frame[0:bg_pick, 0:y_dim]
            temp2=Flim_LT_tr_Ch4_delay_sum_frame[(x_dim-bg_pick):x_dim, 0:y_dim]
            temp_delay_sum = np.hstack((temp1, temp2))
    
            temp1 = Flim_LT_tr_Ch4_delay_num_frame[0:bg_pick, 0:y_dim]
            temp2 = Flim_LT_tr_Ch4_delay_num_frame[(x_dim-bg_pick):x_dim, 0:y_dim]
            temp_delay_num = np.hstack((temp1, temp2))
            Flim_LT_tr_Ch4_bg_frame = np.nansum(temp_delay_sum)/ np.nansum(temp_delay_num)  # the bg for lifetime normalization
    
            Flim_Int_tr_Ch4_norm_frame = Flim_Int_tr_Ch4_frame / Flim_Int_tr_Ch4_bg_frame  # normalized intensity  (i.e., PL intensity enhancement factors)
            Flim_LT_tr_Ch4_norm_frame = Flim_LT_tr_Ch4_frame / Flim_LT_tr_Ch4_bg_frame  # normalized lifetime  (i.e., lifetime shortening factors)
            Flim_Decayrate_tr_Ch4_norm_frame = 1.0 / Flim_LT_tr_Ch4_norm_frame  # normalized decay rate (i.e., decay rate enhancement factors)
    
            # retrace
            temp1 = Flim_Int_retr_Ch4_frame[0:bg_pick, 0:y_dim]
            temp2 = Flim_Int_retr_Ch4_frame[(x_dim-bg_pick):x_dim, 0:y_dim]
            temp_Int = np.hstack((temp1, temp2))
            Flim_Int_retr_Ch4_bg_frame = np.mean(temp_Int)  # the bg for PL intensity normalization
    
            temp1 = Flim_LT_retr_Ch4_delay_sum_frame[0:bg_pick, 0:y_dim]
            temp2 = Flim_LT_retr_Ch4_delay_sum_frame[(x_dim-bg_pick):x_dim, 0:y_dim]
            temp_delay_sum = np.hstack((temp1, temp2))
    
            temp1 = Flim_LT_retr_Ch4_delay_num_frame[0:bg_pick, 0:y_dim]
            temp2 = Flim_LT_retr_Ch4_delay_num_frame[(x_dim-bg_pick):x_dim, 0:y_dim]
            temp_delay_num = np.hstack((temp1, temp2))
            Flim_LT_retr_Ch4_bg_frame = np.nansum(temp_delay_sum) / np.nansum(temp_delay_num)  # the bg for lifetime normalization
    
            Flim_Int_retr_Ch4_norm_frame = Flim_Int_retr_Ch4_frame / Flim_Int_retr_Ch4_bg_frame  # normalized intensity  (i.e., PL intensity enhancement factors)
            Flim_LT_retr_Ch4_norm_frame = Flim_LT_retr_Ch4_frame / Flim_LT_retr_Ch4_bg_frame  # normalized lifetime  (i.e., lifetime shortening factors)
            Flim_Decayrate_retr_Ch4_norm_frame = 1.0 / Flim_LT_retr_Ch4_norm_frame  # normalized decay rate (i.e., decay rate enhancement factors)
    
            ## plot normalized Int and LT of the frame
    
            F5 = plt.figure()
            F5ax1 = F5.add_subplot(111)
            map = F5ax1.pcolorfast(Flim_Decayrate_tr_Ch4_norm_frame, vmax=np.nanmax(Flim_Decayrate_tr_Ch4_norm_frame))
            F5col_bar = F5.colorbar(map)
            F5ax1.set_title('trace' + str(mm))
            F5ax1.set_xlabel(r'x (pixel)')
            F5ax1.set_xlabel(r'y (pixel)')
            # F5.show()
            #F5.savefig(Path_Fig + Filename + '_Decayrate_norm_frame_' + str(mm) + '_trace.png')
    
            F5 = plt.figure()
            F5ax1 = F5.add_subplot(111)
            map = F5ax1.pcolorfast(Flim_Decayrate_retr_Ch4_norm_frame, vmax=np.nanmax(Flim_Decayrate_retr_Ch4_norm_frame))
            F5col_bar = F5.colorbar(map)
            F5ax1.set_title('retrace' + str(mm))
            F5ax1.set_xlabel(r'x (pixel)')
            F5ax1.set_xlabel(r'y (pixel)')
            # F5.show()
            #F5.savefig(Path_Fig + Filename + '_Decayrate_norm_frame_' + str(mm) + '_retrace.png')
    
            ########################################################################################################
            F5 = plt.figure()
            F5ax1 = F5.add_subplot(111)
            map = F5ax1.pcolorfast(Flim_Int_tr_Ch4_norm_frame, vmax=np.nanmax(Flim_Int_tr_Ch4_norm_frame))
            F5col_bar = F5.colorbar(map)
            F5ax1.set_title('trace' + str(mm))
            F5ax1.set_xlabel(r'x (pixel)')
            F5ax1.set_xlabel(r'y (pixel)')
            # F5.show()
            #F5.savefig(Path_Fig + Filename + '_Int_norm_frame_' + str(mm) + '_trace_.png')
    
            F5 = plt.figure()
            F5ax1 = F5.add_subplot(111)
            map = F5ax1.pcolorfast(Flim_Int_retr_Ch4_norm_frame, vmax=np.nanmax(Flim_Int_retr_Ch4_norm_frame))
            F5col_bar = F5.colorbar(map)
            F5ax1.set_title('retrace' + str(mm))
            F5ax1.set_xlabel(r'x (pixel)')
            F5ax1.set_xlabel(r'y (pixel)')
            # F5.show()
            #F5.savefig(Path_Fig + Filename + '_Int_norm_frame_' + str(mm) + '_retrace.png')
        
#########################################################################################
Flim_Int_tr_Ch4_meanframes = Flim_Int_tr_Ch4_sumframes/Flim_Int_tr_Ch4_sumframes_nbright
Flim_Int_retr_Ch4_meanframes = Flim_Int_retr_Ch4_sumframes/Flim_Int_retr_Ch4_sumframes_nbright
            
Flim_LT_tr_Ch4_sumframes = Flim_LT_tr_Ch4_delay_sum_sumframes/Flim_LT_tr_Ch4_delay_num_sumframes
Flim_LT_retr_Ch4_sumframes = Flim_LT_retr_Ch4_delay_sum_sumframes/Flim_LT_retr_Ch4_delay_num_sumframes

########## normalization of Int and LT of sumframes
# trace
temp1=Flim_Int_tr_Ch4_meanframes[0:bg_pick, 0:y_dim]
temp2=Flim_Int_tr_Ch4_meanframes[(x_dim-bg_pick):x_dim, 0:y_dim]
temp_Int_meanframes=np.hstack((temp1,temp2))
Flim_Int_tr_Ch4_bg_meanframes = np.nanmean(temp_Int_meanframes)  # the bg for PL intensity normalization

temp1=Flim_LT_tr_Ch4_delay_sum_sumframes[0:bg_pick, 0:y_dim]
temp2=Flim_LT_tr_Ch4_delay_sum_sumframes[(x_dim-bg_pick):x_dim, 0:y_dim]
temp_delay_sum = np.hstack((temp1, temp2))

temp1 = Flim_LT_tr_Ch4_delay_num_sumframes[0:bg_pick, 0:y_dim]
temp2 = Flim_LT_tr_Ch4_delay_num_sumframes[(x_dim-bg_pick):x_dim, 0:y_dim]
temp_delay_num = np.hstack((temp1, temp2))
Flim_LT_tr_Ch4_bg_sumframes = np.nansum(temp_delay_sum)/ np.nansum(temp_delay_num)  # the bg for lifetime normalization

Flim_Int_tr_Ch4_norm_meanframes = Flim_Int_tr_Ch4_meanframes / Flim_Int_tr_Ch4_bg_meanframes  # normalized intensity  (i.e., PL intensity enhancement factors)
Flim_LT_tr_Ch4_norm_sumframes = Flim_LT_tr_Ch4_sumframes / Flim_LT_tr_Ch4_bg_sumframes  # normalized lifetime  (i.e., lifetime shortening factors)
Flim_Decayrate_tr_Ch4_norm_sumframes = 1.0 / Flim_LT_tr_Ch4_norm_sumframes  # normalized decay rate (i.e., decay rate enhancement factors)

# retrace
temp1 = Flim_Int_retr_Ch4_meanframes[0:bg_pick, 0:y_dim]
temp2 = Flim_Int_retr_Ch4_meanframes[(x_dim-bg_pick):x_dim, 0:y_dim]
temp_Int_meanframes = np.hstack((temp1, temp2))
Flim_Int_retr_Ch4_bg_meanframes = np.nanmean(temp_Int_meanframes)  # the bg for PL intensity normalization

temp1 = Flim_LT_retr_Ch4_delay_sum_sumframes[0:bg_pick, 0:y_dim]
temp2 = Flim_LT_retr_Ch4_delay_sum_sumframes[(x_dim-bg_pick):x_dim, 0:y_dim]
temp_delay_sum = np.hstack((temp1, temp2))

temp1 = Flim_LT_retr_Ch4_delay_num_sumframes[0:bg_pick, 0:y_dim]
temp2 = Flim_LT_retr_Ch4_delay_num_sumframes[(x_dim-bg_pick):x_dim, 0:y_dim]
temp_delay_num = np.hstack((temp1, temp2))
Flim_LT_retr_Ch4_bg_sumframes = np.nansum(temp_delay_sum) / np.nansum(temp_delay_num)  # the bg for lifetime normalization

Flim_Int_retr_Ch4_norm_meanframes = Flim_Int_retr_Ch4_meanframes / Flim_Int_retr_Ch4_bg_meanframes  # normalized intensity  (i.e., PL intensity enhancement factors)
Flim_LT_retr_Ch4_norm_sumframes = Flim_LT_retr_Ch4_sumframes / Flim_LT_retr_Ch4_bg_sumframes  # normalized lifetime  (i.e., lifetime shortening factors)
Flim_Decayrate_retr_Ch4_norm_sumframes = 1.0 / Flim_LT_retr_Ch4_norm_sumframes  # normalized decay rate (i.e., decay rate enhancement factors)

#trace+retrace
Flim_Int_Ch4_meanframes = (Flim_Int_tr_Ch4_sumframes + Flim_Int_retr_Ch4_sumframes)/(Flim_Int_tr_Ch4_sumframes_nbright+Flim_Int_retr_Ch4_sumframes_nbright)
Flim_Int_Ch4_bg_meanframes = (Flim_Int_tr_Ch4_bg_meanframes + Flim_Int_retr_Ch4_bg_meanframes)/2
Flim_Int_Ch4_norm_meanframes = Flim_Int_Ch4_meanframes / Flim_Int_Ch4_bg_meanframes

Flim_LT_Ch4_sumframes = (Flim_LT_tr_Ch4_delay_sum_sumframes+Flim_LT_retr_Ch4_delay_sum_sumframes)/(Flim_LT_tr_Ch4_delay_num_sumframes+Flim_LT_retr_Ch4_delay_num_sumframes)
Flim_LT_Ch4_bg_sumframes = (Flim_LT_tr_Ch4_bg_sumframes + Flim_LT_retr_Ch4_bg_sumframes)/2
Flim_LT_Ch4_norm_sumframes = Flim_LT_Ch4_sumframes / Flim_LT_Ch4_bg_sumframes 
Flim_Decayrate_Ch4_norm_sumframes = 1.0 / Flim_LT_Ch4_norm_sumframes

F5 = plt.figure()
F5ax1 = F5.add_subplot(111)
map = F5ax1.pcolorfast(Flim_Int_tr_Ch4_norm_meanframes,vmax=np.nanmax(Flim_Int_tr_Ch4_norm_meanframes))
F5col_bar = F5.colorbar(map)
F5ax1.set_title('Int_norm_trace')
F5ax1.set_xlabel(r'x (pixel)')
F5ax1.set_xlabel(r'y (pixel)')
# F5.show()
F5.savefig(Path_Fig + Filename + '_Int_norm' + '_trace.png')

F5 = plt.figure()
F5ax1 = F5.add_subplot(111)
map = F5ax1.pcolorfast(Flim_Decayrate_tr_Ch4_norm_sumframes, vmax=np.nanmax(Flim_Decayrate_tr_Ch4_norm_sumframes))
F5col_bar = F5.colorbar(map)
F5ax1.set_title('Decayrate_norm_trace')
F5ax1.set_xlabel(r'x (pixel)')
F5ax1.set_xlabel(r'y (pixel)')
# F5.show()
F5.savefig(Path_Fig + Filename + '_Decayrate_norm' + '_trace.png')

F5 = plt.figure()
F5ax1 = F5.add_subplot(111)
map = F5ax1.pcolorfast(Flim_Int_retr_Ch4_norm_meanframes,vmax=np.nanmax(Flim_Int_retr_Ch4_norm_meanframes))
F5col_bar = F5.colorbar(map)
F5ax1.set_title('Int_norm_retrace')
F5ax1.set_xlabel(r'x (pixel)')
F5ax1.set_xlabel(r'y (pixel)')
# F5.show()
F5.savefig(Path_Fig + Filename + '_Int_norm' + '_retrace.png')

F5 = plt.figure()
F5ax1 = F5.add_subplot(111)
map = F5ax1.pcolorfast(Flim_Decayrate_retr_Ch4_norm_sumframes, vmax=np.nanmax(Flim_Decayrate_retr_Ch4_norm_sumframes))
F5col_bar = F5.colorbar(map)
F5ax1.set_title('Decayrate_norm_retrace')
F5ax1.set_xlabel(r'x (pixel)')
F5ax1.set_xlabel(r'y (pixel)')
# F5.show()
F5.savefig(Path_Fig + Filename + '_Decayrate_norm' + '_retrace.png')

F5 = plt.figure()
F5ax1 = F5.add_subplot(111)
map = F5ax1.pcolorfast(Flim_Int_Ch4_norm_meanframes,vmax=1.5)#np.nanmax(Flim_Int_Ch4_norm_meanframes))
F5col_bar = F5.colorbar(map)
F5ax1.set_title('Int_norm_trace&retrace')
F5ax1.set_xlabel(r'x (pixel)')
F5ax1.set_xlabel(r'y (pixel)')
# F5.show()
F5.savefig(Path_Fig + Filename + '_Int_norm' + '_trace&retrace.png')

F5 = plt.figure()
F5ax1 = F5.add_subplot(111)
map = F5ax1.pcolorfast(Flim_Decayrate_Ch4_norm_sumframes, vmax=7)#np.nanmax(Flim_Decayrate_Ch4_norm_sumframes))
F5col_bar = F5.colorbar(map)
F5ax1.set_title('Decayrate_norm_trace&retrace')
F5ax1.set_xlabel(r'x (pixel)')
F5ax1.set_xlabel(r'y (pixel)')
# F5.show()
F5.savefig(Path_Fig + Filename + '_Decayrate_norm' + '_trace&retrace.png')

#########################################################################################
# obtain the lifetime curve extracted from the picked region
MicroTime_Ch4_tr_pick=MicroTime_Ch4_bottomup_tr_pick
MicroTime_Ch4_tr_pick.extend(MicroTime_Ch4_topdown_tr_pick)
MicroTime_Ch4_retr_pick=MicroTime_Ch4_bottomup_retr_pick
MicroTime_Ch4_retr_pick.extend(MicroTime_Ch4_topdown_retr_pick)
MicroTime_Ch4_pick=MicroTime_Ch4_tr_pick
MicroTime_Ch4_pick.extend(MicroTime_Ch4_retr_pick)

MicroTime_Ch4_pick=np.array(MicroTime_Ch4_pick)


#bin_time = MeasDesc_Resolution * 1e9
bin_time =Rec.microtime_res*1e9
[time_LT_Ch4, Inten_LT_Ch4] = make_hist(MicroTime_Ch4_pick, bin_time)
Inten_LT_Ch4 = np.array(Inten_LT_Ch4)
Inten_LT_Ch4_max = np.max(Inten_LT_Ch4)

x = np.where(Inten_LT_Ch4 == Inten_LT_Ch4_max)
x_value = time_LT_Ch4[x]
time_LT_Ch4_1 = []
Inten_LT_Ch4_1 = []
time_LT_Ch4_2 = []
Inten_LT_Ch4_2 = []

for ii in range(len(time_LT_Ch4)):
    if time_LT_Ch4[ii] < (x_value - 20):
        Inten_LT_Ch4_1.append(Inten_LT_Ch4[ii])
    else:
        Inten_LT_Ch4_2.append(Inten_LT_Ch4[ii])
Inten_LT_Ch4 = np.hstack((Inten_LT_Ch4_2[0:], Inten_LT_Ch4_1[0:]))

Inten_LT_Ch4_norm = Inten_LT_Ch4 * 1.0 / Inten_LT_Ch4_max

F3 = plt.figure()
F3ax1 = F3.add_subplot(111)
F3ax1.semilogy(time_LT_Ch4[0:], Inten_LT_Ch4_norm)
F3ax1.set_xlabel(r'time (ns)')
# F3ax1.set_ylabel(r'y (nm)')
F3ax1.set_xlim([0,250])
F3.show()







