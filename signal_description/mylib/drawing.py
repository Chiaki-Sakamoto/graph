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
import numpy as np
import matplotlib.pyplot as plt
from .utils import retrieve_filename
from .utils import convert_to_scientific_notation
from .utils import normalize


def _judge_norm_ylabel(norm_flag, y_si_prefix):
    if norm_flag:
        plt.ylabel("Signal Voltage (arb.units)")
    else:
        plt.ylabel(f"Signal Voltage ({y_si_prefix}V)")


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


def _plot_graph(parser, axs, row, col, graph):
    (x_exponent, x_si_prefix,
        y_exponent, y_si_prefix) = _change_notation(parser, graph)
    title = graph.title[:15] + '\n' + SPACE + graph.title[15:]
    print(f"[{row}, {col}]: {graph.title}")
    if not parser.args.normalization:
        graph.y *= -1
    axs[row, col].plot(
        graph.x * 10 ** x_exponent,
        graph.y * 10 ** y_exponent
        )
    axs[row, col].set_title(title)
    axs[row, col].set_xlabel(f"Time ({x_si_prefix}s)")
    axs[row, col].set_ylabel(f"Signal Voltage ({y_si_prefix}V)")


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
    (x_exponent, x_si_prefix,
        y_exponent, y_si_prefix) = _change_notation(parser, graph)
    graph.title = retrieve_filename(graph.title)
    plt.figure()
    if not parser.args.normalization:
        graph.y *= -1
    plt.plot(graph.x * 10 ** x_exponent, graph.y * 10 ** y_exponent)
    plt.title(graph.title)
    plt.xlabel(f"Time ({x_si_prefix}s)")
    _judge_norm_ylabel(parser.args.normalization, y_si_prefix)
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
            _plot_graph(parser, axs, 0, index, graph)
        elif index > 1:
            _plot_graph(parser, axs, 1, index - 2, graph)
    plt.show()


def show_signal(parser, graph):
    number_of_graphs = len(parser.args.data_path)
    if (number_of_graphs == 1):
        _show_single_graph(parser, graph)
    elif (2 <= number_of_graphs <= 4):
        _show_multi_graphs(parser, graph)
