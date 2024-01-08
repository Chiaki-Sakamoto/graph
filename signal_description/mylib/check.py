#!/usr/bin/python3
###############################################################################
#                                __              __                           #
#                          _____/ /_  ___  _____/ /__                         #
#                         / ___/ __ \/ _ \/ ___/ //_/                         #
#                        / /__/ / / /  __/ /__/ ,<                            #
#                        \___/_/ /_/\___/\___/_/|_|                           #
#                                                                             #
###############################################################################
from .macro import *
import os


def check_arguments(parser, args):
    nbr_args = len(args)

    if nbr_args == 0:
        exit(EXIT_FAILURE)
    elif (
        not parser.args.export and
        not parser.args.angle_distribution and
        nbr_args > 4
    ):
        print("Error\nAre there too many graphs to display?\n")
        exit(EXIT_FAILURE)


def check_output_path(path):
    if os.path.isfile(path):
        print(
            "Error\n"
            "This is the path to the file\n"
            "Output to /tmp\n"
            )
        path = None
    elif not os.path.isdir(path):
        print(
            "Error\n"
            "Directory does not exitst\n"
            "Output to /tmp\n"
            )
        path = None
