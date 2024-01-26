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
    for focal in ("200mm", "400mm", "800mm"):
        fig, axs = plt.subplots(layout="tight")
        if focal == "200mm":
            focal_ad = f200_ad
        if focal == "400mm":
            focal_ad = f400_ad
        if focal == "800mm":
            focal_ad = f800_ad
        for band in ("G-band", "Y-band", "Z-band"):
            if band == "G-band":
                focal_band_ad = focal_ad.ad_gband
                color = 'r'
                label = "0.14 ~ 0.22 THz"
            if band == "Y-band":
                focal_band_ad = focal_ad.ad_yband
                color = 'g'
                label = "0.22 ~ 0.33 THz"
            if band == "Z-band":
                focal_band_ad = focal_ad.ad_zband
                color = 'b'
                label = "0.33 ~ 0.50 THz"
            x = np.array(list(focal_band_ad.keys()))
            y = np.array(list(focal_band_ad.values()))
            axs.plot(
                x,
                y * 10 ** 3,
                color + 'o',
                label=label,
                )
        axs.legend(
            bbox_to_anchor=(1.32, 1),
            loc='upper right',
            borderaxespad=0
            )
        plt.show()
        plt.close()


if __name__ == "__main__":
    main()
