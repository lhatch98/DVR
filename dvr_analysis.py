import numpy as np
import matplotlib.pyplot as plt


class DVRAnalysis:
    def __init__(self, nwfns,
                 wfn_fname,
                 xOH_fname,
                 oo_fname
                 ):
        """
        calc expectation values <O^hat> and <O^Hat**2> for position operator given wfns
        :param nwfns: number of wave functions
        :type nwfns: int
        :param wfn_fname: filename of wfn data to use EXCLUDE EXTENSION
        :type wfn_fname: str
        :param xOH_fname: filename of OH steps INCLUDE EXT
        :type xOH_fname: str
        :param oo_fname: filename of OO steps
        :type oo_fname : str
        """
        self.nwfns = nwfns
        self.wfn_fname = wfn_fname
        self.xOH_fname = xOH_fname
        self.oo_fname = oo_fname
        self.myexp_val_list = np.zeros(self.nwfns)
        self.myexp_val_list2 = np.zeros(self.nwfns)
        self.oo_vals = np.load(self.oo_fname)
        self.x = np.load(self.xOH_fname) / 1.88973  # bohr -> angst

    def calc_expvals(self):
        for i in range(1, self.nwfns + 1):
            wfns = np.load(self.wfn_fname + str(i) + ".npy")  # "dimer_dvrwfns_"
            psi = wfns[:, 0]
            exp_val = psi @ (self.x * psi)
            exp_val2 = psi @ ((self.x ** 2) * psi)
            self.myexp_val_list[i - 1] = np.copy(exp_val)
            self.myexp_val_list2[i - 1] = np.copy(exp_val2)
        return self.myexp_val_list, self.myexp_val_list2

    def calc_stand_dev(self):
        ct = 0
        for expval, expval2 in zip(self.myexp_val_list, self.myexp_val_list2):
            sigma = np.sqrt(expval2 - (expval ** 2))
            plt.plot(self.oo_vals[ct], sigma, "ro")
            ct += 1
        plt.xlabel("$R_{OO} (\AA)$")
        plt.ylabel("$\sigma_{\Psi{OH}}$")
        # plt.savefig(fname="dimer_stddev_vs_oo_fig", dpi=250)
        plt.show()

    def calc_psi_max(self):
        for i in range(1, self.nwfns + 1):
            wfns = np.load(self.wfn_fname + str(i) + ".npy")  # "dimer_dvrwfns_"
            psi = wfns[:, 0]
            psi = np.absolute(psi)  # correct for phase
            psi_max_loc = np.argmax(psi)
            coord_psi_max = self.x[psi_max_loc]
            plt.plot(self.oo_vals[i - 1], coord_psi_max, "bo")
        plt.xlabel("$R_{OO} (\AA)$")
        plt.ylabel("$r_{OH} (\AA)$ of $\Psi^{max}$")
        # plt.savefig(fname="dimer_psimax_vs_oo_fig", dpi=250)
        plt.show()
        return None




exp_ob = DVRAnalysis(16, "dimer_dvrwfns_", "xOH.npy", "oo_steps_dimer.npy")
exp_ob.calc_expvals()
exp_ob.calc_stand_dev()
exp_ob.calc_psi_max()

#  -------------------------------------------------------------------


# def calc_exp_vals(n_wfns, h_filename, dirname, filename):
#     """
#     calc expectation values <O^hat> and <O^Hat**2> for position operator given wfns
#     :param n_wfns: number of wfns collected from dvr
#     :type n_wfns: int
#     :param h_filename: filename WITH EXTENSION containing h positions from dvr scans
#     :type h_filename: str
#     :param dirname: name of directory where dvr wfns are stored
#     :type dirname: str
#     :param filename: name of dvr wfn files EXCLUDE EXTENSION
#     :type filename: str
#     :return: myexp_val_list, myexp_val_list2
#     :rtype: np arrays
#     """
#     myexp_val_list = np.zeros(n_wfns)
#     myexp_val_list2 = np.zeros(n_wfns)
#     for i in np.arange(1, n_wfns + 1):
#         foo = np.load(dirname + "/" + filename + "_" + str(i) + ".npy")
#         psi = foo[:, 0]
#         x = np.load(h_filename)
#         exp_val = psi@(x * psi)
#         print(exp_val)
#         exp_val2 = psi@((x**2) * psi)
#         myexp_val_list[i - 1] = np.copy(exp_val)
#         myexp_val_list2[i - 1] = np.copy(exp_val2)
#         print(myexp_val_list)
#         print(myexp_val_list2)
#     return myexp_val_list, myexp_val_list2
#
#
#
# def stand_dev(myexp_val_list, myexp_val_list2, oo_filename):
#     """
#     calculate standard deviation (sigma/width) of expectation values
#     plot sigma_OH (y) vs oo step (x)
#     """
#     oo_vals = np.load(oo_filename)
#     ct = 0
#     for expval, expval2 in zip(myexp_val_list, myexp_val_list2):
#         sigma = np.sqrt(expval2 - (expval)**2)
#         plt.plot(oo_vals[ct], sigma, "bo")
#         ct += 1
#     plt.show()
#     return None
#
#
# def psi_max(n_wfns, h_filename, oo_filename, dirname, filename):
#     """
#     find oh position where psi is maximum for each oo distance
#     plot (y) oh position vs (x) oo step
#     """
#     xhyd = np.load(h_filename)
#     oo_vals = np.load(oo_filename)
#     for i in np.arange(1, n_wfns + 1):
#         foo = np.load(dirname + "/" + filename + "_" + str(i) + ".npy")
#         psi = foo[:, 0]
#         psi = np.absolute(psi)
#         psi_max_loc = np.argmax(psi)
#         coord_psi_max = xhyd[psi_max_loc]
#         plt.plot(oo_vals[i - 1], coord_psi_max, "bo")
#     plt.show()
#     return None


def wfn_plot(numb_wfns):
    for i in range(1, numb_wfns + 1):
        a = np.load(file="dimer_dvrwfns_" + str(i) + ".npy")
        psi = a[:, 0]
        x = np.load(file="xOH.npy")
        plt.plot(x, psi)
    plt.show()
    return None

test = wfn_plot(16)


# exp_val_list, exp_val_list2 = calc_exp_vals(10, "h_steps_trimer.npy", "dvr_wfn_data_trimer", "dvrwfns")
# xd = stand_dev(exp_val_list, exp_val_list2, "oo_steps_trimer.npy")


# run = psi_max(10, "h_steps_trimer.npy", "oo_steps_trimer.npy", "dvr_wfn_data_trimer", "dvrwfns")





