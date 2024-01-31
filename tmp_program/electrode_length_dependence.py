import sys
import matplotlib.pyplot as plt
import numpy as np


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


def _get_max_signal(paths):
    result = list()
    for length in ("e10mm", "e30mm", "e50mm"):
        peak = 0
        for path in getattr(paths, length):
            time, signal = np.loadtxt(
                path,
                skiprows=3,
                unpack=True,
                delimiter=',',
                )
            tmp_peak = -min(signal)
            if peak < tmp_peak:
                peak = tmp_peak
        result.append(peak)
    return result


def main():
    argv = sys.argv[1:]
    electrode_len = [10, 30, 50]
    band_path = BAND(*_branch_band_path(argv))
    fig, axs = plt.subplots(layout="tight")
    for band in ("gband", "yband", "zband"):
        if band == "gband":
            color = 'r'
            label = "0.14 ~ 0.22 THz"
        if band == "yband":
            color = 'g'
            label = "0.22 ~ 0.33 THz"
        if band == "zband":
            color = 'b'
            label = "0.33 ~ 0.50 THz"
        electrode_length_path = ELECTRODE_LEN(*_branch_electrode_len(getattr(band_path, band)))
        max_signal_electrode_len = _get_max_signal(electrode_length_path)
        slope, intercept = np.polyfit(
            np.array(electrode_len),
            np.array(max_signal_electrode_len) * 10 ** 3,
            1,
        )
        x_array = np.arange(5, 56, 5)
        axs.plot(
            electrode_len,
            np.array(max_signal_electrode_len) * 10 ** 3,
            color + 'o',
            label=label
            )
        axs.plot(
            x_array,
            x_array * slope + intercept,
            color + '-',
            linewidth=3
            )
    axs.set_xlim(5, 55)
    axs.set_xticks(np.arange(5, 56, 5))
    axs.get_xaxis().set_tick_params(pad=15)
    axs.set_xlabel("Electrode length (mm)", fontsize=30)
    axs.set_ylim(0, 35)
    axs.set_yticks(np.arange(0, 36, 5))
    axs.get_yaxis().set_tick_params(pad=5)
    axs.set_ylabel("Signal voltage (mV)", fontsize=30)
    axs.legend(
        bbox_to_anchor=(1.37, 1),
        loc="upper right",
        borderaxespad=0
    )
    plt.savefig("/tmp/" + "electrode_length_dependence" + ".pdf", format="pdf")
    plt.show()
    plt.close()
    return


if __name__ == "__main__":
    main()
