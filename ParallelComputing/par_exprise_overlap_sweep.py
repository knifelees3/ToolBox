"""
To summaarize the sweep using parallel computing
Author Zhaohua Tian
Date: 2020 08 03
"""

import multiprocessing as mp
import numpy as np
# from scipy import integrate
import matplotlib.pyplot as plt
import time
from tqdm import tqdm
# from scipy.linalg import solve

start = time.time()


def exp_overlap(t, lambdamat, coe, kappa0):
    f_temp = 0
    N = len(lambdamat)
    for l in range(N):
        coe_l = 1.0*coe*np.sqrt(kappa0)
        for n in range(N):
            if n != l:
                coe_l = coe_l/(lambdamat[l]-lambdamat[n])
        coe_l = coe_l/(-1j*(lambdamat[l]+1j*kappa0/2))
        f_temp = f_temp+coe_l * \
            (np.exp(-1j * lambdamat[l]*t)-np.exp(-kappa0*t/2))
    sym = max(np.abs(f_temp)**2)
    return sym
# The fucntion to implement the theoretical expressions
# Theoretical eigenvalues and coefficients should be given
# kappa0: linewidth of the exponential rsing pulse
# lambdamat: the list of eigenvalues
# coe: -i*ge\sqrt{kappa}*J_{12}*J_{23}...


def exp_overlap_list(t, lambdamat, coe):
    num_kappa0 = 100
    kappa0_mat = np.linspace(0.2, 5, num_kappa0)
    overlap_mat = np.zeros((num_kappa0))
    for l in range(num_kappa0):
        kappa0 = kappa0_mat[l]
        overlap_mat[l] = exp_overlap(t, lambdamat, coe, kappa0)
    return max(overlap_mat)
# A function to handle a list of kappa0 and select the best kappa0


# define basic parameters
g = 1.0
ge = np.sqrt(2) * g
J12 = 1.88 * g
J23 = 2.94 * g
kappa = 7.92 * g
tmax = 20.0 / g
numt = 1000
num_J12 = 99
num_J23 = 100
num_kappa = 101
num_loop = num_J12 * num_J23
tmat = np.linspace(0, tmax, numt)
J12_mat = np.linspace(0.1, 9, num_J12)
J23_mat = np.linspace(0.1, 10, num_J23)
kappa3_mat = np.linspace(0.1, 28, num_kappa)
J12_grid, J23_grid = np.meshgrid(J12_mat, J23_mat)
loop_mat = np.hstack((J12_grid.reshape(num_loop, 1),
                      J23_grid.reshape(num_loop, 1)))

# test----------------------------
# M = np.array([[0, ge, 0, 0], [ge, 0, J12, 0], [0, J12, 0, J23],
#               [0, 0, J23, -1j * kappa / 2]])
# kappa_mat = np.array([0, 0, 0, kappa])
# [lambda_mat, vec] = np.linalg.eig(M)
# coe = -1j * np.sqrt(kappa) * ge * J12 * J23
# testmat = exp_overlap_list(tmat, lambda_mat, coe)
# kappa0_mat = np.linspace(0.2, 5, 100)
# fig1 = plt.figure()
# plt.plot(kappa0_mat, testmat)
# plt.show()
# print(loop_mat.shape)


def sweep_sym(l, loop_mat, kappa3_mat, num_loop):
    temp = np.zeros(num_loop)
    for m in range(num_loop):
        J12 = loop_mat[m, 0] * g
        J23 = loop_mat[m, 1] * g
        kappa = kappa3_mat[l] * g
        M = np.array([[0, ge, 0, 0], [ge, 0, J12, 0], [0, J12, 0, J23],
                      [0, 0, J23, -1j * kappa / 2]])
        [lambda_mat, vec] = np.linalg.eig(M)
        kappa_mat = np.array([0, 0, 0, kappa])
        coe = -1j * np.sqrt(kappa) * ge * J12 * J23
        temp[m] = exp_overlap_list(tmat, lambda_mat, coe)
    return temp
# A function to sweep the parameters and make it easy to parallize


max_sym = 0
if __name__ == '__main__':
    pbar = tqdm(total=num_kappa)
    pool = mp.Pool(processes=15)  # number of cores
    results = [pool.apply_async(sweep_sym, args=(
        l, loop_mat, kappa3_mat, num_loop), callback=lambda _:
        pbar.update(1)) for l in range(num_kappa)]
    max_sym_temp = [p.get() for p in results]
    max_symd = np.array(max_sym_temp)
    max_sym = np.ravel(max_symd)
    # pool.terminate()
    pool.close()
    pool.join()

# print(max_sym)

end = time.time()
print(str(end - start))
# np.save("./MaxSymExpRise3Cav20200731.npy", max_sym)
# np.savetxt("./MaxSymExpRise3Cav20200731.txt", max_sym)
