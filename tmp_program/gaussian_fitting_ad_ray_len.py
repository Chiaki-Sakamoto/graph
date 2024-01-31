import re
import sys
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit


class BAND_PATH:
    def __init__(self, G_band_path, Y_band_path, Z_band_path):
        self.gband = G_band_path
        self.yband = Y_band_path
        self.zband = Z_band_path


class AD_LIST:
    def __init__(self, F200_ad, F400_ad, F800_ad):
        self.ad_f200 = F200_ad
        self.ad_f400 = F400_ad
        self.ad_f800 = F800_ad


def gauss(x, a, mu, sigma):
    return a * np.exp(-(x - mu) ** 2 / (2 * sigma ** 2))


def fit(func, x, y, param_init):
    popt, pocv = curve_fit(func, x, y, param_init)
    perr = np.sqrt(np.diag(pocv))
    return popt, pocv, perr


def _init_angle_distribution(band_path):
    angle_distribution = dict()
    for index, path in enumerate(band_path):
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


def _branch_set_band_fig(band, axs):
    if band == "gband":
        axs.set_ylim(0, 35)
        axs.set_title("0.14 ~ 0.22 THz")
    if band == "yband":
        axs.set_ylim(0, 25)
        axs.set_title("0.22 ~ 0.33 THz")
    if band == "zband":
        axs.set_ylim(0, 3)
        axs.set_title("0.33 ~ 0.50 THz")


def _plot_focal_band_ad(band_ad_list, band, axs):
    for focal in ("200mm", "400mm", "800mm"):
        if focal == "200mm":
            focal_band_ad = band_ad_list.ad_f200
            color = 'r'
        if focal == "400mm":
            focal_band_ad = band_ad_list.ad_f400
            color = 'g'
        if focal == "800mm":
            focal_band_ad = band_ad_list.ad_f800
            color = 'b'
        label = "f = " + focal
        x_list = list(focal_band_ad.keys())
        y_list = list(focal_band_ad.values())
        x = np.array(x_list)
        y = np.array(y_list)
        peak_index = np.argmax(y)
        peak_value = np.max(y) * 10 ** 3
        std = np.std(y * 10 ** 3)
        print(f"std{std}, peak_index{peak_index}, peak_value{peak_value}")
        gauss_fit = fit(gauss, x, y * 10 ** 3, [peak_value, peak_index, std])
        fit_x = np.linspace(min(x) - 5, max(x) + 5, 1000)
        fit_y = gauss(fit_x, *gauss_fit[0])
        if not (band == "zband" and focal == "200mm"):
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
            label=label,
        )
    axs.legend(
        bbox_to_anchor=(1.25, 1),
        loc="upper right",
        borderaxespad=0
    )


def _set_label_limit(axs):
    axs.set_xlabel("Angle (degree)", fontsize=30)
    axs.set_xlim(-35, 35)
    axs.set_xticks(np.arange(-35, 36, 5))
    axs.get_xaxis().set_tick_params(pad=15)
    axs.set_ylabel("Signal voltage (mV)", fontsize=30)
    axs.get_yaxis().set_tick_params(pad=5)


def branch_focal_path(argv):
    result = dict(
        f200mm=list(),
        f400mm=list(),
        f800mm=list(),
    )
    for path in argv:
        if "Lens" in path and "200mm" in path:
            result["f200mm"].append(path)
        if "Lens" in path and "400mm" in path:
            result["f400mm"].append(path)
        if "Lens" in path and "800mm" in path:
            result["f800mm"].append(path)
    return result


def branch_band_path(focal_path):
    gband = list()
    yband = list()
    zband = list()
    for path in focal_path:
        if "G-band" in path:
            gband.append(path)
        if "Y-band" in path:
            yband.append(path)
        if "Z-band" in path:
            zband.append(path)
    return gband, yband, zband


def main():
    argv = sys.argv[1:]
    focal_path = branch_focal_path(argv)
    f200_path = BAND_PATH(*branch_band_path(focal_path["f200mm"]))
    f400_path = BAND_PATH(*branch_band_path(focal_path["f400mm"]))
    f800_path = BAND_PATH(*branch_band_path(focal_path["f800mm"]))
    for band in ("gband", "yband", "zband"):
        fig, axs = plt.subplots(layout="tight")
        _set_label_limit(axs)
        _branch_set_band_fig(band, axs)
        band_ad_list = AD_LIST(
            _sort_angle_distribution(
                _init_angle_distribution(getattr(f200_path, band))
                ),
            _sort_angle_distribution(
                _init_angle_distribution(getattr(f400_path, band))
                ),
            _sort_angle_distribution(
                _init_angle_distribution(getattr(f800_path, band))
                ),
        )
        _plot_focal_band_ad(band_ad_list, band, axs)
        plt.savefig("/tmp/" + band + "_gaussian_fitting_ad_ray_len.pdf", format="pdf")
        plt.show()
        plt.close()


if __name__ == "__main__":
    main()
