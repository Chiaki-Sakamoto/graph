#!/usr/bin/python3
###############################################################################
#                                                                             #
#                         ____  ____ ______________  _____                    #
#                        / __ \/ __ `/ ___/ ___/ _ \/ ___/                    #
#                       / /_/ / /_/ / /  (__  )  __/ /                        #
#                      / .___/\__,_/_/  /____/\___/_/                         #
#                     /_/                                                     #
###############################################################################
import argparse
from . import check


def parser_main(parser):
    parser.parser = argparse.ArgumentParser(
        description="I will drow a graph!"
        )
    parser.parser.add_argument(
        'data_path',
        nargs='+',
        help='The path of the graph you want to describe'
        )
    parser.parser.add_argument(
        '-e', '--export',
        help='export pdf option',
        action='store_true',
        )
    parser.args = parser.parser.parse_args()
    if parser.args.export:
        print("export pdf.\n")
    check.check_arguments(parser, parser.args.data_path)
