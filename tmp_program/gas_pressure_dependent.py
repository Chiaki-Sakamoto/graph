import sys
import re
import matplotlib.pyplot as plt
from matplotlib.ticker import StrMethodFormatter
import numpy as np


class BAND:
    def __init__(self, gband, yband, zband):
        self.gband = gband
        self.yband = yband
        self.zband = zband


def _init_pressure_distribution(band):
    result = dict()
    for band_path in band:
        if not band_path.endswith(".txt"):
            print(
                "Error\n"
                f"{band_path}: Extension is not .txt\n"
                )
            continue
        match = re.search(r'(?<=_)([-\d]+)MPa', band_path)
        pressure = int(match.group(1))
        time, signal = np.loadtxt(
            band_path, skiprows=3, unpack=True, delimiter=',',
            )
        max_signal = -min(signal)
        result[pressure] = max_signal
    return result


def _sort_pressure_distribution(pd_band):
    result = dict(
        sorted(
            pd_band.items(),
            key=lambda x: x[0],
            reverse=True
            )
        )
    return result


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


def main():
    argv = sys.argv[1:]
    band_path = BAND(*_branch_band_path(argv))
    fig, axs = plt.subplots(layout="tight")
    for band in ("gband", "yband", "zband"):
        pd_band = _init_pressure_distribution(getattr(band_path, band))
        sorted_pd_band = _sort_pressure_distribution(pd_band)
        if band == "gband":
            color = 'r'
            label = "0.14 ~ 0.22 THz"
        if band == "yband":
            color = 'g'
            label = "0.22 ~ 0.33 THz"
        if band == "zband":
            color = 'b'
            label = "0.33 ~ 0.50 THz"
        x = np.array(list(sorted_pd_band.keys()))
        y = np.array(list(sorted_pd_band.values()))
        axs.plot(
            x * 10,
            y * 10 ** 3, color + 'o',
            label=label,
        )
        slope, intercept = np.polyfit(
            x * 10,
            y * 10 ** 3,
            1,
        )
        x_array = np.arange(50, 750, 10)
        axs.plot(
            x_array,
            x_array * slope + intercept,
            color + '-', linewidth=3,
        )
    # axs.set_xticklabels(axs.get_xticks(), rotation=20)
    # axs.xaxis.set_major_formatter(StrMethodFormatter('{x:.2f}'))
    axs.set_xlim(50, 270)
    axs.set_xticks(np.arange(50, 271, 20))
    axs.get_xaxis().set_tick_params(pad=15)
    axs.set_ylim(0, 60)
    axs.set_yticks(np.arange(0, 61, 10))
    axs.get_yaxis().set_tick_params(pad=15)
    axs.set_xlabel("Pressure (kPa)", fontsize=30)
    axs.set_ylabel("Signal voltage (mV)", fontsize=30)
    axs.legend(
        bbox_to_anchor=(0.32, 0.95),
        loc="upper right",
        borderaxespad=0
    )
    plt.savefig("/tmp/" + "gas_pressure_dependent" + ".pdf", format="pdf")
    plt.show()
    plt.close()


if __name__ == "__main__":
    main()
