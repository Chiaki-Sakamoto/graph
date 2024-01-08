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


def angle_distribution_main(parser, graph):
    angle_distribution = dict()
    print("plot angle distribution\n")
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

    sorted_angle_distribution = dict(
        sorted(
            angle_distribution.items(),
            key=lambda x: x[0],
            reverse=True
            )
        )
    graph.x = list(sorted_angle_distribution.keys())
    graph.y = list(sorted_angle_distribution.values())
    for index, (x, y) in enumerate(zip(graph.x, graph.y)):
        print(f"Index: {index}, x: {x}, y:{y}")
    plt.figure()
    plt.plot(graph.x, graph.y, 'o')
    # plt.title(graph.title)
    # print(f"show {graph.title}")
    plt.show()
    plt.close()
