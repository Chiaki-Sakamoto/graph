import sys
import matplotlib.pyplot as plt
import numpy as np


def _init_max_signal_voltage(rayleigh_length_ratioratio, argv, band):
    path_in_200 = list()
    path_in_400 = list()
    path_in_800 = list()
    for index, ratio in enumerate(rayleigh_length_ratioratio):
        for path in argv:
            if "Lens" in path and "200mm" in path and band in path:
                path_in_200.append(path)
            if "Lens" in path and "400mm" in path and band in path:
                path_in_400.append(path)
            if "Lens" in path and "800mm" in path and band in path:
                path_in_800.append(path)
    return path_in_200, path_in_400, path_in_800


def _get_max_rayleigh_length_ratio(path_in_200, path_in_400, path_in_800):
    result = list()
    max_signal = 0
    for array in (path_in_200, path_in_400, path_in_800):
        for path in array:
            time, signal = np.loadtxt(
                path, skiprows=3, unpack=True, delimiter=','
            )
            peak_signal = -min(signal)
            if peak_signal > max_signal:
                max_signal = peak_signal
        result.append(max_signal)
    return result


def main():
    ratio = [1, 4, 16]
    argv = sys.argv[1:]
    fig, axs = plt.subplots(layout='tight')
    for band in ("G-band", "Y-band", "Z-band"):
        if band == "G-band":
            color = 'r'
            label = "0.14 ~ 0.22 THz"
        elif band == "Y-band":
            color = 'g'
            label = "0.22 ~ 0.33 THz"
        elif band == "Z-band":
            color = 'b'
            label = "0.33 ~ 0.50 THz"
        (path_band_200,
            path_band_400,
            path_band_800) = _init_max_signal_voltage(ratio, argv, band)
        max_band = _get_max_rayleigh_length_ratio(
            path_band_200,
            path_band_400,
            path_band_800,
        )
        slope, intercept = np.polyfit(
            np.array(ratio),
            np.array(max_band) * 10 ** 3,
            1,
        )
        axs.plot(
            np.array(ratio),
            np.array(max_band) * 10 ** 3,
            color + 'o',
            label=label,
        )
        x_array = np.array(range(21))
        axs.plot(
            x_array,
            x_array * slope + intercept,
            color + '-',
            linewidth=3,
        )
    axs.set_xlabel("Rayleigh length ratio", fontsize=30)
    axs.set_ylabel("Signal voltage (mV)", fontsize=30)
    axs.set_xlim(0, 20)
    axs.set_ylim(0, 35)
    axs.set_xticks(np.arange(0, 21, 5))
    axs.set_yticks(np.arange(0, 36, 5))
    axs.get_xaxis().set_tick_params(pad=15)
    axs.get_yaxis().set_tick_params(pad=5)
    axs.legend(bbox_to_anchor=(1.36, 1), loc='upper right', borderaxespad=0)
    plt.savefig("/tmp/" + "rayleigh_length_ratio" + ".pdf", format="pdf")
    plt.show()
    plt.close()


if __name__ == "__main__":
    main()
