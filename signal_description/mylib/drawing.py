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


def _check_number_of_graphs(env):
    return len(env.argvs)


def show_signal_description(env, graph):
    if (_check_number_of_graphs(env) == 2):
        print("single graph:" + str(len(env.argvs)))
    graph.x, graph.y = np.loadtxt(
        env.argvs[1], skiprows=3, unpack=True, delimiter=','
        )
    plt.figure()
    plt.plot(graph.x, -graph.y)
    plt.show()
