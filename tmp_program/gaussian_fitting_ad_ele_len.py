import sys
import re
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit


class BAND:
    def __init__(self, Gband, Yband, Zband):
        self.gband = Gband
        self.yband = Yband
        self.zband = Zband


class ELECTRODE_LEN:
    def __init__(self, E10mm, E30mm, E50mm):
        self.e10mm = E10mm
        self.e30mm = E30mm
        self.e50mm = E50mm


def gauss(x, a, mu, sigma):
    return a * np.exp(-(x - mu) ** 2 / (2 * sigma ** 2))


def fit(func, x, y, param_init):
    popt, pocv = curve_fit(func, x, y, param_init)
    perr = np.sqrt(np.diag(pocv))
    return popt, pocv, perr


def _branch_band_path(argv):
    gband = list()
    yband = list()
    zband = list()
    for path in argv:
        if "G-band" in path:
            gband.append(path)
        if "Y-band" in path:
            yband.append(path)
        if "Z-band" in path:
            zband.append(path)
    return gband, yband, zband


def _branch_electrode_len(band_path):
    e10mm = list()
    e30mm = list()
    e50mm = list()
    for path in band_path:
        if "L=10mm" in path:
            e10mm.append(path)
        if "L=30mm" in path:
            e30mm.append(path)
        if "L=50mm" in path:
            e50mm.append(path)
    return e10mm, e30mm, e50mm


def _init_angle_distribution(paths):
    angle_distribution = dict()
    for index, path in enumerate(paths):
        if not path.endswith(".txt"):
            print(
                "Error\n"
                f"{path}: Extension is not .txt\n"
                )
            continue
        match = re.search(r'(?<=_)([-\d]+)deg', path)
        angle = int(match.group(1))
        time, signal = np.loadtxt(
            path, skiprows=3, unpack=True, delimiter=','
            )
        max_signal = -min(signal)
        angle_distribution[angle] = max_signal
    return angle_distribution


def _sort_angle_distribution(angle_distribution):
    sorted_angle_distribution = dict(
        sorted(
            angle_distribution.items(),
            key=lambda x: x[0],
            reverse=True
            )
        )
    return sorted_angle_distribution


def main():
    argv = sys.argv[1:]
    band_path = BAND(*_branch_band_path(argv))
    for band in ("gband", "yband", "zband"):
        fig, axs = plt.subplots(layout="tight")
        axs.set_xlabel("Angle (degree)", fontsize=30)
        axs.set_ylabel("Signal voltage (mV)", fontsize=30)
        axs.set_xlim(-35, 35)
        axs.set_xticks(np.arange(-35, 36, 5))
        axs.get_xaxis().set_tick_params(pad=15)
        axs.get_yaxis().set_tick_params(pad=5)
        if band == "gband":
            axs.set_title("0.14 ~ 0.22 THz", fontsize=30, pad=20)
            axs.set_ylim(0, 35)
            axs.set_yticks(np.arange(0, 36, 5))
        if band == "yband":
            axs.set_title("0.22 ~ 0.33 THz", fontsize=30, pad=20)
            axs.set_ylim(0, 25)
            axs.set_yticks(np.arange(0, 26, 5))
        if band == "zband":
            axs.set_title("0.33 ~ 0.50 THz", fontsize=30, pad=20)
            axs.set_ylim(0, 5)
            axs.set_yticks(np.arange(0, 6, 1))
        for length in ("10mm", "30mm", "50mm"):
            if length == "10mm":
                color = 'r'
            if length == "30mm":
                color = 'g'
            if length == "50mm":
                color = 'b'
            electrode_len = ELECTRODE_LEN(
                *_branch_electrode_len(getattr(band_path, band))
                )
            ad_electrode_length = _init_angle_distribution(getattr(electrode_len, "e" + length))
            sorted_angle_distribution = _sort_angle_distribution(ad_electrode_length)
            x_list = list(sorted_angle_distribution.keys())
            y_list = list(sorted_angle_distribution.values())
            x = np.array(x_list)
            y = np.array(y_list)
            gauss_fit = fit(gauss, x, y * 10 ** 3, [np.max(y) * 10 ** 3, np.argmax(y), np.std(y * 10 ** 3)])
            fit_x = np.linspace(min(x) - 5, max(x) + 5, 1000)
            fit_y = gauss(fit_x, *gauss_fit[0])
            if not (band == "zband" and length == "10mm"):
                axs.plot(
                    fit_x,
                    fit_y,
                    color + '-',
                    linewidth=2,
                    )
            axs.plot(
                x,
                y * 10 ** 3,
                color + 'o',
                label=length
                )
        axs.legend(
            bbox_to_anchor=(1.18, 1),
            loc="upper right",
            borderaxespad=0
        )
        plt.savefig("/tmp/" + f"{band}_gaussian_fitting_ad_ele_len" + ".pdf", format="pdf")
        plt.show()
        plt.close()
    return


if __name__ == "__main__":
    main()
