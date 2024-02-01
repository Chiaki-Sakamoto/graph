import sys
import re
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
from scipy.integrate import quad


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
    fig, axs = plt.subplots(layout="tight")
    x = [10, 30, 50]
    for band in ("gband", "yband", "zband"):
        integral_value = list()
        axs.set_xlabel("Electrode length (cm)", fontsize=30)
        axs.set_ylabel("Signal voltage (mV)", fontsize=30)
        axs.set_xlim(5, 55)
        axs.set_xticks(np.arange(5, 56, 5))
        axs.get_xaxis().set_tick_params(pad=15)
        axs.set_ylim(0, 700)
        axs.set_yticks(np.arange(0, 701, 100))
        axs.get_yaxis().set_tick_params(pad=5)
        if band == "gband":
            color = 'r'
            label = "0.14 ~ 0.22 THz"
        if band == "yband":
            color = 'g'
            label = "0.22 ~ 0.33 THz"
        if band == "zband":
            color = 'b'
            label = "0.33 ~ 0.50 THz"
        for length in ("10mm", "30mm", "50mm"):
            electrode_len = ELECTRODE_LEN(
                *_branch_electrode_len(getattr(band_path, band))
                )
            ad_electrode_length = _init_angle_distribution(getattr(electrode_len, "e" + length))
            sorted_angle_distribution = _sort_angle_distribution(ad_electrode_length)
            x_list = list(sorted_angle_distribution.keys())
            y_list = list(sorted_angle_distribution.values())
            ad_x = np.array(x_list)
            ad_y = np.array(y_list)
            if not (band == "zband" and length == "10mm"):
                gauss_fit = fit(gauss, ad_x, ad_y * 10 ** 3, [np.max(ad_y) * 10 ** 3, np.argmax(ad_y), np.std(ad_y * 10 ** 3)])
                lower_limit = min(ad_x)
                uper_limit = max(ad_x)
                area, _ = quad(gauss, lower_limit, uper_limit, args=(gauss_fit[0][0], gauss_fit[0][1], gauss_fit[0][2]))
                integral_value.append(area)
        if band == "zband":
            x = [30, 50]
        axs.plot(
            x,
            integral_value,
            color + 'o',
            label=label,
            )
        axs.legend(
            bbox_to_anchor=(1.38, 1),
            loc="upper right",
            borderaxespad=0
        )
    plt.savefig("/tmp/" + "integral_ad_ele_len" + ".pdf", format="pdf")
    plt.show()
    plt.close()
    return


if __name__ == "__main__":
    main()
