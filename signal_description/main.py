#!/usr/bin/python3
###############################################################################
#                                             _                               #
#                            ____ ___  ____ _(_)___                           #
#                           / __ `__ \/ __ `/ / __ \                          #
#                          / / / / / / /_/ / / / / /                          #
#                         /_/ /_/ /_/\__,_/_/_/ /_/                           #
#                                                                             #
###############################################################################

import sys
import matplotlib as mpl
import signal_description.mylib as mylib
from signal_description.mylib.macro import *


class Env:
    def __init__(self, argv, rc_file):
        self.argvs = argv
        self.rc_file = rc_file


class Parser:
    def __init__(self, parser, args):
        self.parser = parser
        self.args = args


class Graph:
    def __init__(self, x, y, title):
        self.x = x
        self.y = y
        self.title = title


class Data:
    def __init__(self, env, parser, graph):
        self.env = env
        self.parser = parser
        self.graph = graph


def init():
    data = Data(
        Env(sys.argv, mpl.matplotlib_fname()),
        Parser(None, None),
        Graph(None, None, None)
        )
    return data


def main():
    data = init()
    mylib.parser.parser_main(data.parser)
    mylib.print_env.print_env(data.env)
    mylib.print_env.print_argvs(data.parser.args.data_path)
    if data.parser.args.export:
        mylib.export.export_signal(data.parser, data.graph)
    elif data.parser.args.angle_distribution:
        mylib.angle_distribution.angle_distribution_main(
            data.parser,
            data.graph
            )
    else:
        mylib.drawing.show_signal(data.parser, data.graph)
    return EXIT_SUCESS
