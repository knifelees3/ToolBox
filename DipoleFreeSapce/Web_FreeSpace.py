import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# @st.cache(hash_funcs={np.ufunc: cal_power_homo})
def cal_power_homo(wavelength, epsilon, J):

    wavelength = wavelength*1e-9
    epsilon0 = 8.854187817620389850537e-12
    mu0 = 1.2566370614359172953851e-6
    c_const = 1 / np.sqrt(epsilon0 * mu0)

    omega = 2 * np.pi / wavelength * c_const
    n = np.sqrt(epsilon)

    # In COMSOL, the dipole moment is defined as current
    d = J / omega

    P = (np.abs(d)**2) * omega**4 / 3 / c_const**3 / \
        4 / np.pi / epsilon0 / epsilon * n**3

    return np.abs(P)


st.markdown('## Single Calculate')
wavelength = st.number_input('Please Input the Wavelength (nm) Here')
epsilon = st.number_input('Please Input the Epsilon Here')
J = st.number_input('Please Input the Dipole Moment (nm) Here')

if st.button('Calculate Power'):
    power0 = cal_power_homo(wavelength, epsilon, J)
    st.write('The power is', power0, 'W')

st.markdown('## Plot A Figure')

wavelength_min = st.number_input('Please Input the Begin Wavelength (nm) Here')
wavelength_max = st.number_input('Please Input the End Wavelength (nm) Here')
num_wavelength = int(st.number_input('Please Input Number of Points'))

wl_mat = np.linspace(wavelength_min, wavelength_max, num_wavelength)

epsilon_2 = st.number_input('Please Re Input the Epsilon Here')
J_2 = st.number_input('Please Re Input the Dipole Moment (nm) Here')
power_mat = cal_power_homo(wl_mat, epsilon_2, J_2)

# if st.button('Show the power list'):
#     power_mat = cal_power_homo(wl_mat, epsilon_2, J_2)
#     st.write('The power has been calculated')

if st.checkbox('Show power data'):
    st.subheader('power list data')
    st.write(power_mat)


if st.button('Plot the power'):
    fig1 = plt.figure()
    plt.plot(wl_mat, power_mat)
    plt.xlabel('Wavelength/nm')
    plt.ylabel('Power/W')
    plt.title('Emission Power Of Dipole')
    plt.grid()
    st.write(fig1)
# if st.button('Say hello'):
#     st.write('Why hello there')

# title = st.text_input('Movie title', 'Life of Brian')
# st.write('The current movie title is', title)

# number = st.number_input('Insert a number')
# st.write('The current number is ', number)
