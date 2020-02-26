import numpy as np
import matplotlib.pyplot as plt


def calc_exp_vals(n_wfns, h_filename, dirname, filename):
    """
    calc expectation values <O^hat> and <O^Hat**2> for position operator given wfns
    :param n_wfns: number of wfns collected from dvr
    :type n_wfns: int
    :param h_filename: filename WITH EXTENSION containing h positions from dvr scans
    :type h_filename: str
    :param dirname: name of directory where dvr wfns are stored
    :type dirname: str
    :param filename: name of dvr wfn files EXCLUDE EXTENSION
    :type filename: str
    :return: myexp_val_list, myexp_val_list2
    :rtype: np arrays
    """
    myexp_val_list = np.zeros(n_wfns)
    myexp_val_list2 = np.zeros(n_wfns)
    for i in np.arange(1, n_wfns + 1):
        foo = np.load(dirname + "/" + filename + "_" + str(i) + ".npy")
        psi = foo[:, 0]
        x = np.load(h_filename)
        exp_val = psi@(x * psi)
        print(exp_val)
        exp_val2 = psi@((x**2) * psi)
        myexp_val_list[i - 1] = np.copy(exp_val)
        myexp_val_list2[i - 1] = np.copy(exp_val2)
        print(myexp_val_list)
        print(myexp_val_list2)
    return myexp_val_list, myexp_val_list2


def stand_dev(myexp_val_list, myexp_val_list2, oo_filename):
    """
    calculate standard deviation (sigma/width) of expectation values
    plot sigma_OH (y) vs oo step (x)
    """
    oo_vals = np.load(oo_filename)
    ct = 0
    for expval, expval2 in zip(myexp_val_list, myexp_val_list2):
        sigma = np.sqrt(expval2 - (expval)**2)
        plt.plot(oo_vals[ct], sigma, "bo")
        ct += 1
    plt.show()
    return None


def psi_max(n_wfns, h_filename, oo_filename, dirname, filename):
    """
    find oh position where psi is maximum for each oo distance
    plot (y) oh position vs (x) oo step
    """
    xhyd = np.load(h_filename)
    oo_vals = np.load(oo_filename)
    for i in np.arange(1, n_wfns + 1):
        foo = np.load(dirname + "/" + filename + "_" + str(i) + ".npy")
        psi = foo[:, 0]
        psi = np.absolute(psi)
        psi_max_loc = np.argmax(psi)
        coord_psi_max = xhyd[psi_max_loc]
        plt.plot(oo_vals[i - 1], coord_psi_max, "bo")
    plt.show()
    return None