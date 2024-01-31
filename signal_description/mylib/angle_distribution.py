#!/usr/bin/python3
###############################################################################
#                                              __                             #
#                           ____ _____  ____ _/ /__                           #
#                          / __ `/ __ \/ __ `/ / _ \                          #
#                         / /_/ / / / / /_/ / /  __/                          #
#                         \__,_/_/ /_/\__, /_/\___/                           #
#                  ___      __       /____/        __  _                      #
#             ____/ (_)____/ /______(_) /_  __  __/ /_(_)___  ____            #
#            / __  / / ___/ __/ ___/ / __ \/ / / / __/ / __ \/ __ \           #
#           / /_/ / (__  ) /_/ /  / / /_/ / /_/ / /_/ / /_/ / / / /           #
#           \__,_/_/____/\__/_/  /_/_.___/\__,_/\__/_/\____/_/ /_/            #
#                                                                             #
###############################################################################
import re
import numpy as np
import matplotlib.pyplot as plt
from .utils import convert_to_scientific_notation
from .utils import normalize


def _change_notation(parser, graph):
    x_exponent, x_si_prefix = convert_to_scientific_notation(graph.x)
    if parser.args.normalization:
        graph.y = normalize(graph.y)
        y_exponent, y_si_prefix = convert_to_scientific_notation(graph.y)
    else:
        y_exponent, y_si_prefix = convert_to_scientific_notation(graph.y)
    print(
        f"x_exp: {x_exponent}, x_si_prefix: {x_si_prefix}\n"
        f"y_exp: {y_exponent}, y_si_prefix: {y_si_prefix}"
        )
    return x_exponent, x_si_prefix, y_exponent, y_si_prefix


def _init_angle_distribution(parser):
    angle_distribution = dict()
    for index, path in enumerate(parser.args.data_path):
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


def _print_angle_distribution(graph):
    for index, (x, y) in enumerate(zip(graph.x, graph.y)):
        print(f"Index: {index}, x: {x}, y:{y}")


def angle_distribution_main(parser, graph):
    print("plot angle distribution\n")
    angle_distribution = _init_angle_distribution(parser)
    sorted_angle_distribution = _sort_angle_distribution(angle_distribution)
    graph.x = list(sorted_angle_distribution.keys())
    graph.y = list(sorted_angle_distribution.values())
    graph.x = np.array(graph.x)
    graph.y = np.array(graph.y)
    print(type(graph.y))
    (x_exponent, x_si_prefix,
        y_exponent, y_si_prefix) = _change_notation(parser, graph)
    # _print_angle_distribution(graph)
    fig, axs = plt.subplots()
    axs.plot(
        graph.x * 10 ** x_exponent,
        graph.y * 10 ** y_exponent, 'o'
        )
    axs.set_xlabel("Angle (°)", fontsize=30)
    axs.set_ylabel(f"Signal Voltage ({y_si_prefix}V)", fontsize=30)
    if parser.args.export:
        plt.savefig('/tmp/' + "angle_distribution" + '.pdf', format='pdf')
        print("export angle_distribution.pdf in /tmp\n")
    else:
        plt.show()
    plt.close()
