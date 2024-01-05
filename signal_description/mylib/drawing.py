#!/usr/bin/python3
###############################################################################
#                         __                   _                              #
#                    ____/ /________ _      __(_)___  ____ _                  #
#                   / __  / ___/ __ \ | /| / / / __ \/ __ `/                  #
#                  / /_/ / /  / /_/ / |/ |/ / / / / / /_/ /                   #
#                  \__,_/_/   \____/|__/|__/_/_/ /_/\__, /                    #
#                                                  /____/                     #
###############################################################################
from .macro import *
import os
import numpy as np
import matplotlib.pyplot as plt
from .utils import retrieve_filename


def _plot_graph(axs, graph, row, col):
    title = graph.title
    print(f"[{row}, {col}]: {graph.title}")
    axs[row, col].plot(graph.x, -graph.y)
    axs[row, col].set_title(title)


def _show_single_graph(parser, graph):
    graph.title = parser.args.data_path[0]
    if not graph.title.endswith(".txt"):
        print(
            "Error\n"
            f"{graph.title}: Extension is not .txt\n"
            )
        exit(EXIT_FAILURE)
    graph.x, graph.y = np.loadtxt(
        graph.title, skiprows=3, unpack=True, delimiter=','
        )
    graph.title = retrieve_filename(graph.title)
    plt.figure()
    plt.plot(graph.x, -graph.y)
    plt.title(graph.title)
    print(f"show {graph.title}")
    plt.show()
    plt.close()


def _show_multi_graphs(parser, graph):
    fig, axs = plt.subplots(2, 2, sharex=True, sharey=True)
    for index, path in enumerate(parser.args.data_path):
        if not path.endswith(".txt"):
            print(
                "\nError\n"
                f"{graph.title}: Extension is not .txt\n"
                )
            continue
        graph.x, graph.y = np.loadtxt(
            path, skiprows=3, unpack=True, delimiter=','
            )
        graph.title = retrieve_filename(path)
        if index < 2:
            _plot_graph(axs, graph, 0, index)
        elif index > 1:
            _plot_graph(axs, graph, 1, index - 2)
    plt.show()


def show_signal(parser, graph):
    number_of_graphs = len(parser.args.data_path)
    if (number_of_graphs == 1):
        _show_single_graph(parser, graph)
    elif (2 <= number_of_graphs <= 4):
        _show_multi_graphs(parser, graph)
