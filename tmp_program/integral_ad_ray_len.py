import re
import sys
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
from scipy.integrate import quad


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


def _integral_gaussian_fitting(band_ad_list, band, integral_value):
    for focal in ("200mm", "400mm", "800mm"):
        if focal == "200mm":
            focal_band_ad = band_ad_list.ad_f200
        if focal == "400mm":
            focal_band_ad = band_ad_list.ad_f400
        if focal == "800mm":
            focal_band_ad = band_ad_list.ad_f800
        x_list = list(focal_band_ad.keys())
        y_list = list(focal_band_ad.values())
        ad_x = np.array(x_list)
        ad_y = np.array(y_list)
        peak_index = np.argmax(ad_y)
        peak_value = np.max(ad_y) * 10 ** 3
        std = np.std(ad_y * 10 ** 3)
        print(f"std{std}, peak_index{peak_index}, peak_value{peak_value}")
        if not (band == "zband" and focal == "200mm"):
            gauss_fit = fit(gauss, ad_x, ad_y * 10 ** 3, [peak_value, peak_index, std])
            lower_limit = min(ad_x)
            uper_limit = max(ad_x)
            area, _ = quad(gauss, lower_limit, uper_limit, args=(gauss_fit[0][0], gauss_fit[0][1], gauss_fit[0][2]))
            integral_value.append(area)


def _set_label_limit(axs):
    axs.set_xlabel("Rayleigh length rato", fontsize=30)
    axs.set_xlim(0, 20)
    axs.set_xticks(np.arange(0, 21, 5))
    axs.get_xaxis().set_tick_params(pad=15)
    axs.set_ylabel("Signal voltage (mV)", fontsize=30)
    axs.set_ylim(0, 700)
    axs.set_yticks(np.arange(0, 701, 100))
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
    x = [1, 4, 16]
    fig, axs = plt.subplots(layout="tight")
    for band in ("gband", "yband", "zband"):
        integral_value = list()
        if band == "gband":
            color = 'r'
            label = "0.14 ~ 0.22 THz"
        if band == "yband":
            color = 'g'
            label = "0.22 ~ 0.33 THz"
        if band == "zband":
            color = 'b'
            label = "0.33 ~ 0.50 THz"
        _set_label_limit(axs)
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
        _integral_gaussian_fitting(band_ad_list, band, integral_value)
        if band == "zband":
            x = [4, 16]
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
    plt.savefig("/tmp/" + "integral_ad_ray_len.pdf", format="pdf")
    plt.show()
    plt.close()


if __name__ == "__main__":
    main()
