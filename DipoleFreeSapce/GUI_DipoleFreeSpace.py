# To Calculate the dipole's emission power in a homogeneous
import numpy as np
from tkinter import *
import tkinter.font as tkFont
import matplotlib.pyplot as plt


def cal_power_homo(wavelength, epsilon, J):

    epsilon0 = 8.854187817620389850537e-12
    mu0 = 1.2566370614359172953851e-6
    c_const = 1 / np.sqrt(epsilon0 * mu0)

    omega = 2 * np.pi / wavelength * c_const
    n = np.sqrt(epsilon)

    # In COMSOL, the dipole moment is defined as current
    d = J * 1j / omega

    P = (np.abs(d)**2) * omega**4 / 3 / c_const**3 / \
        4 / np.pi / epsilon0 / epsilon * n**3
    print(P)

    return P


class Power_Homo_Cal():

    def __init__(self, init_window_name):
        self.ft = tkFont.Font(family='Fixdsys', size=20, weight=tkFont.BOLD)
        self.init_window_name = init_window_name

    def set_init_window(self):

        self.init_window_name.title(
            "Dipole's Emission Power In Homogeneous Media V1.0 By Zhaohua Tian")  # 窗口名
        # self.init_window_name.geometry('320x160+10+10')       #290
        # 160为窗口大小，+10 +10 定义窗口弹出时的默认展示位置
        self.init_window_name.geometry('1920x1080+10+10')

        # The Single Cal Part
        self.SingleBigText = Label(
            self.init_window_name, text="Single Cal", font=self.ft,  compound='center')
        self.SingleBigText.grid(column=0, row=0)

        # Wavelength
        self.WL0_single_lbl = Label(
            self.init_window_name, text="Wavelngth (nm)")
        self.WL0_single_lbl.grid(column=0, row=1)

        self.WL0_single_En = Entry(self.init_window_name, width=10)
        self.WL0_single_En.grid(column=1, row=1)

        # Epsilon
        self.epsilon_lbl = Label(
            self.init_window_name, text="Relative Permitivity")
        self.epsilon_lbl.grid(column=2, row=1)

        self.epsilon_En = Entry(self.init_window_name, width=10)
        self.epsilon_En.grid(column=3, row=1)

        # Dipole Moment
        self.dipoleMoment_lbl = Label(
            self.init_window_name, text="Dipole Moment (C*m)")
        self.dipoleMoment_lbl.grid(column=4, row=1)

        self.dipoleMoment_En = Entry(self.init_window_name, width=10)
        self.dipoleMoment_En.grid(column=5, row=1)

        # Power results
        self.power_single_lbl = Label(
            self.init_window_name, text="Power (W)")
        self.power_single_lbl.grid(column=4, row=3)

        self.power_single_text = Text(
            self.init_window_name, width=10, height=1)
        self.power_single_text.grid(column=5, row=3, rowspan=1, columnspan=1)

        # Button Calculate Single
        self.Cal_Single_btn = Button(self.init_window_name,
                                     text="Calculate", command=self.cal_single_btn)

        self.Cal_Single_btn.grid(column=1, row=3)

        ##############################################################
        # The second Cal Part
        self.SingleBigText = Label(
            self.init_window_name, text="Multi Cal", font=self.ft,  compound='center')
        self.SingleBigText.grid(column=0, row=4)

        # Wavelength min
        self.WL0_Min_lbl = Label(
            self.init_window_name, text="Wavelngth Min(nm)")
        self.WL0_Min_lbl.grid(column=0, row=5)

        self.WL0_Min_En = Entry(self.init_window_name, width=10)
        self.WL0_Min_En.grid(column=1, row=5)

        # Wavelength max
        self.WL0_Max_lbl = Label(
            self.init_window_name, text="Wavelngth Max(nm)")
        self.WL0_Max_lbl.grid(column=2, row=5)

        self.WL0_Max_En = Entry(self.init_window_name, width=10)
        self.WL0_Max_En.grid(column=3, row=5)

        # Number of wavelength
        self.WL0_num_lbl = Label(
            self.init_window_name, text="Number of points")
        self.WL0_num_lbl.grid(column=4, row=5)

        self.WL0_num_En = Entry(self.init_window_name, width=10)
        self.WL0_num_En.grid(column=5, row=5)

       # Power results big
        self.power_mat_lbl = Label(
            self.init_window_name, text="Power list(W)")
        self.power_mat_lbl.grid(column=1, row=8)

        self.power_mat_text = Text(
            self.init_window_name)
        self.power_mat_text.grid(column=1, row=9, rowspan=10, columnspan=10)

        # Button Calculate Single
        self.Cal_Plot_btn = Button(self.init_window_name,
                                   text="Plot the power", command=self.plot_lines)

        self.Cal_Plot_btn.grid(column=3, row=7)

        # Text information
        self.info_lbl = Label(
            self.init_window_name, text="This software was developed by Zhaohua Tian as a study project for python GUI")
        self.info_lbl.grid(column=3, row=30)

    # ________________________________________________________________________
    # Function definition

    def cal_single_btn(self):
        wavelength = float(self.WL0_single_En.get())
        epsilon = float(self.epsilon_En.get())
        dipolemoment = float(self.dipoleMoment_En.get())

        power = cal_power_homo(wavelength * 1e-9,
                               epsilon, dipolemoment)
        # self.write_log_to_Text(str(wavelength))
        self.power_single_text.delete(1.0, END)
        self.power_single_text.insert(1.0, power)
        # self.write_log_to_Text("INFO:str_trans_to_md5 success")
        return 0

    def plot_lines(self):
        wave_min = float(self.WL0_Min_En.get())
        wave_max = float(self.WL0_Max_En.get())
        wave_num = int(self.WL0_num_En.get())
        wave_mat = np.linspace(wave_min, wave_max, wave_num)
        # print(wave_mat)
        epsilon = float(self.epsilon_En.get())
        dipolemoment = float(self.dipoleMoment_En.get())
        power = cal_power_homo(wave_mat * 1e-9, epsilon, dipolemoment)

        # self.write_log_to_Text(str(wavelength))
        self.power_mat_text.delete(1.0, END)
        self.power_mat_text.insert(1.0, power)

        fig1 = plt.figure()
        plt.plot(wave_mat, power)
        plt.xlabel('Wavelength/nm')
        plt.ylabel('Power/W')
        plt.title('Emission Power Of Dipole')
        plt.show()
        return 0

        ###################################################################


def gui_start():
    init_window = Tk()  # 实例化出一个父窗口
    ZMJ_PORTAL = Power_Homo_Cal(init_window)
    # 设置根窗口默认属性
    ZMJ_PORTAL.set_init_window()
    init_window.mainloop()  # 父窗口进入事件循环，可以理解为保持窗口运行，否则界面不展示


gui_start()
