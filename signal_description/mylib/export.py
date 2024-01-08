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
        plt.figure()
        plt.plot(graph.x, -graph.y)
        plt.title(graph.title)
        if parser.args.output:
            plt.savefig(
                parser.args.output + graph.title + '.pdf',
                format='pdf'
                )
        else:
            plt.savefig('/tmp/' + graph.title + '.pdf', format='pdf')
        print(f"export {graph.title}.pdf\n")
        plt.close()
