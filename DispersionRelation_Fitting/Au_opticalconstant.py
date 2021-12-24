# %%
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


def DrudeM(omega, omegaAu_D, gammaAu_D):
    varepsilon_D = omegaAu_D**2/(omega**2-1j*(omega*gammaAu_D))
    return varepsilon_D


def LorentzM(omega, omegaAu_L, gammaAu_L, omega_0):
    varepsilon_L = omegaAu_L**2/(omega**2-omega_0**2-1j*omega*gammaAu_L)
    return varepsilon_L


def dispersion_nk(wavelength, omegaAu_D, gammaAu_D, omegaAu_L, gammaAu_L, omega0_L):
    omega = 2*np.pi*c_const/wavelength*1e9
    varepsilon_gold = varepsilon_inf * \
        (1-omegaAu_L**2/(omega**2-omega0_L**2-1j*omega*gammaAu_L) -
         omegaAu_D**2/(omega**2-1j*(omega*gammaAu_D)))
    n = np.sqrt((np.abs(varepsilon_gold)+varepsilon_gold.real)/2)
    k = np.sqrt((np.abs(varepsilon_gold)-varepsilon_gold.real)/2)
    # epsilon = n**2-k**2+1j*(2*n*k)
    return np.hstack((n, k))


if __name__ == '__main__':

    varepsilon_inf = 5.90157
    omegaAu_D1 = np.sqrt(1.297056e16**2/varepsilon_inf)
    gammaAu_D1 = 4.108244e13
    omegaAu_L1 = np.sqrt(4.298305e15**2*1.26913/varepsilon_inf)
    omegaAu_01 = 4.298305e15
    gammaAu_L1 = 2*4.104244e13
    para_guess = np.array(
        [omegaAu_D1, gammaAu_D1, omegaAu_L1, gammaAu_L1, omegaAu_01])

    c_const = 3.0e8

    num = 1000
    wavelen_mat = np.linspace(800, 2000, num)
    refractive = np.zeros((num, 3))

    filename = "./Au_opticalconstants.csv"
    data = np.loadtxt(filename, delimiter=',')
    n_exp = data[:, 1]
    k_exp = data[:, 2]
    wl_exp = data[:, 0]*1000
    epsilon_exp = n_exp**2-k_exp**2+1j*(2*n_exp*k_exp)
# %%
    fit_para, cov_mat = curve_fit(
        dispersion_nk, wl_exp, np.hstack((n_exp, k_exp)), para_guess, bounds=(0, np.inf))
# %%
    nk_fit = dispersion_nk(
        wavelen_mat, fit_para[0], fit_para[1], fit_para[2], fit_para[3], fit_para[4])
# %%
# Plot epsilon
    #omegaAu_D, gammaAu_D, omegaAu_L, gammaAu_L, omega0_L
    str_wpAuD = "$\omega_{p}^{Dru}$="+str(fit_para[0])
    str_gammaAuD = "$\gamma_{p}^{Dru}$="+str(fit_para[1])
    str_wpAuL = "$\omega_{p}^{Lor}$="+str(fit_para[2])
    str_gammaAuL = "$\gamma_{p}^{Lor}$="+str(fit_para[3])
    str_omega0L = "$\omega_{0}^{Lor}$="+str(fit_para[4])
    fig1 = plt.figure()
    plt.plot(wl_exp, n_exp, 'g*', label='exp n')
    plt.plot(wl_exp, k_exp, 'b*', label='exp k')
    plt.plot(wavelen_mat, nk_fit[0:1000], 'g-', label="Fitted n")
    plt.plot(wavelen_mat, nk_fit[1000:2000], 'b-', label="Fitted k")
    plt.legend(loc='best')
    plt.text(1400, 10,  str_wpAuD)
    plt.text(1400, 8,  str_gammaAuD)
    plt.text(1400, 6,  str_wpAuL)
    plt.text(1400, 4,  str_gammaAuL)
    plt.text(1400, 2,  str_omega0L)
    plt.xlabel('wavelength (um)')
    #plt.xlim([500, 1600])
    plt.grid()
    plt.savefig("./DispersionforAu.png")
    plt.show()
