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


def check_arguments(parser, args):
    nbr_args = len(args)

    if (nbr_args == 0):
        exit(EXIT_FAILURE)
    elif (not parser.args.export and nbr_args > 4):
        print("Error\nAre there too many graphs to display?\n")
        exit(EXIT_FAILURE)
