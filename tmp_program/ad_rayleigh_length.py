import re
import sys
import matplotlib.pyplot as plt
import numpy as np


class BAND_PATH:
    def __init__(self, G_band_path, Y_band_path, Z_band_path):
        self.gband = G_band_path
        self.yband = Y_band_path
        self.zband = Z_band_path


class AD_LIST:
    def __init__(self, G_band_ad, Y_band_ad, Z_band_ad):
        self.ad_gband = G_band_ad
        self.ad_yband = Y_band_ad
        self.ad_zband = Z_band_ad


class BAND_AD_LIST:
    def __init__(self, f200_ad, f400_ad, f800_ad):
        self.ad_f200 = f200_ad
        self.ad_f400 = f400_ad
        self.ad_f800 = f800_ad

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
    f200_ad = AD_LIST(
        _sort_angle_distribution(_init_angle_distribution(f200_path.gband)),
        _sort_angle_distribution(_init_angle_distribution(f200_path.yband)),
        _sort_angle_distribution(_init_angle_distribution(f200_path.zband)),
    )
    f400_ad = AD_LIST(
        _sort_angle_distribution(_init_angle_distribution(f400_path.gband)),
        _sort_angle_distribution(_init_angle_distribution(f400_path.yband)),
        _sort_angle_distribution(_init_angle_distribution(f400_path.zband)),
    )
    f800_ad = AD_LIST(
        _sort_angle_distribution(_init_angle_distribution(f800_path.gband)),
        _sort_angle_distribution(_init_angle_distribution(f800_path.yband)),
        _sort_angle_distribution(_init_angle_distribution(f800_path.zband)),
    )
    for band in ("G-band", "Y-band", "Z-band"):
        fig, axs = plt.subplots(layout="tight")
        axs.set_xlabel("Angle (degree)")
        axs.set_ylabel("Signal voltage (mV)")
        axs.set_xlim(-35, 35)
        axs.set_xticks(np.arange(-35, 36, 5))
        if band == "G-band":
            axs.set_ylim(0, 35)
            axs.set_title("0.14 ~ 0.22 THz")
            focal_ad_list = BAND_AD_LIST(f200_ad.ad_gband, f400_ad.ad_gband, f800_ad.ad_gband)
        if band == "Y-band":
            axs.set_ylim(0, 25)
            axs.set_title("0.22 ~ 0.33 THz")
            focal_ad_list = BAND_AD_LIST(f200_ad.ad_yband, f400_ad.ad_yband, f800_ad.ad_yband)
        if band == "Z-band":
            axs.set_ylim(0, 3)
            axs.set_title("0.33 ~ 0.50 THz")
            focal_ad_list = BAND_AD_LIST(f200_ad.ad_zband, f400_ad.ad_zband, f800_ad.ad_zband)
        for focal in ("200mm", "400mm", "800mm"):
            if focal == "200mm":
                focal_band_ad = focal_ad_list.ad_f200
                color = 'r'
            if focal == "400mm":
                focal_band_ad = focal_ad_list.ad_f400
                color = 'g'
            if focal == "800mm":
                focal_band_ad = focal_ad_list.ad_f800
                color = 'b'
            label = "f = " + focal
            x = np.array(list(focal_band_ad.keys()))
            y = np.array(list(focal_band_ad.values()))
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
        plt.show()
        plt.close()


if __name__ == "__main__":
    main()
