#!/usr/bin/python3
###############################################################################
#                                            _                                #
#                                __ _  ___ _(_)__                             #
#                               /  ' \/ _ `/ / _ \                            #
#                              /_/_/_/\_,_/_/_//_/                            #
#                                                                             #
###############################################################################

import sys

import matplotlib as mpl
import signal_description.mylib as mylib


class Env:
    def __init__(self, argv, rc_file):
        self.argvs = argv
        self.rc_file = rc_file


class Graph:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Data:
    def __init__(self, env, graph):
        self.env = env
        self.graph = graph


def main():
    data = Data(
        Env(sys.argv, mpl.matplotlib_fname()),
        Graph(None, None)
        )
    mylib.print_env.print_env(data.env)
    mylib.print_env.print_argvs(data.env.argvs)
    mylib.drawing.show_signal_description(data.env, data.graph)
