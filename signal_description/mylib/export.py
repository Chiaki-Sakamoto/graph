#!/usr/bin/python3
###############################################################################
#                                                    __                       #
#                        ___  _  ______  ____  _____/ /_                      #
#                       / _ \| |/_/ __ \/ __ \/ ___/ __/                      #
#                      /  __/>  </ /_/ / /_/ / /  / /_                        #
#                      \___/_/|_/ .___/\____/_/   \__/                        #
#                              /_/                                            #
###############################################################################
import numpy as np
import matplotlib.pyplot as plt
from .utils import retrieve_filename
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


def export_signal(parser, graph):
    for index, path in enumerate(parser.args.data_path):
        if not path.endswith(".txt"):
            print(
                "Error\n"
                f"{path}: Extension is not .txt\n"
                )
            continue
        graph.x, graph.y = np.loadtxt(
            path, skiprows=3, unpack=True, delimiter=','
            )
        graph.title = retrieve_filename(path)
        (x_exponent, x_si_prefix,
            y_exponent, y_si_prefix) = _change_notation(parser, graph)
        fig, axs = plt.subplots()
        if not parser.args.normalization:
            graph.y *= -1
        axs.plot(graph.x * 10 ** x_exponent, graph.y * 10 ** y_exponent)
        axs.set_title(graph.title)
        axs.set_xlabel(f"Time ({x_si_prefix}s)")
        axs.set_ylabel(f"Signal Voltage ({y_si_prefix}V)")
        if parser.args.output:
            plt.savefig(
                parser.args.output + graph.title + '.pdf',
                format='pdf'
                )
        else:
            plt.savefig('/tmp/' + graph.title + '.pdf', format='pdf')
        print(f"export {graph.title}.pdf\n")
        plt.close()
