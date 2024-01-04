#!/usr/bin/python3
###############################################################################
#                           __                _                               #
#                       ___/ /______ __    __(_)__  ___ _                     #
#                      / _  / __/ _ `/ |/|/ / / _ \/ _ `/                     #
#                      \_,_/_/  \_,_/|__,__/_/_//_/\_, /                      #
#                                                 /___/                       #
###############################################################################
import numpy as np
import matplotlib.pyplot as plt


def _plot_graph(axs, graph, row, col):
    title = graph.title
    split_str = int(len(graph.title) / 2)
    axs[row, col].plot(graph.x, -graph.y)
    axs[row, col].set_title(title[:split_str] + '\n' + title[:split_str:])


def _show_single_graph(env, graph):
    graph.x, graph.y = np.loadtxt(
        env.argvs[1], skiprows=3, unpack=True, delimiter=','
        )
    plt.figure()
    plt.plot(graph.x, -graph.y)
    plt.show()


def _show_multi_graphs(env, graph):
    fig, axs = plt.subplots(2, 2, sharex=True, sharey=True)
    for index, path in enumerate(env.argvs):
        if index != 0:
            graph.x, graph.y = np.loadtxt(
                path, skiprows=3, unpack=True, delimiter=','
                )
            graph.title = path
        if index != 0 and index < 3:
            _plot_graph(axs, graph, 0, index - 1)
        elif index != 0 and index > 2:
            _plot_graph(axs, graph, 1, index - 3)
    plt.show()


def show_signal_description(env, graph):
    number_of_graphs = len(env.argvs)
    if (number_of_graphs == 2):
        print("show single graph")
        _show_single_graph(env, graph)
    elif (number_of_graphs == 5):
        print("show multi graph\n")
        _show_multi_graphs(env, graph)
    else:
        print("Error\nAre there too many graphs to display?\n")
