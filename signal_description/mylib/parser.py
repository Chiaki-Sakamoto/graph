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
        help='export pdf option.',
        action='store_true',
        )
    parser.parser.add_argument(
        '-ad', '--angle_distribution',
        help='plot angle distribution.',
        action='store_true',
        )
    parser.parser.add_argument(
        '-o', '--output',
        help='output directory path.',
        )
    parser.parser.add_argument(
        '-n', '--normalization',
        help='normalize signal voltage.',
        action='store_true',
        )
    parser.parser.add_argument(
        '-f', '--fitting',
        help='fitting the graph.',
        action='store_true',
    )
    parser.parser.add_argument(
        '-add', '--add',
        help='add the graph',
    )
    parser.args = parser.parser.parse_args()
    if parser.args.export:
        print("export pdf.\n")
    if parser.args.normalization:
        print("normalize signal voltage.\n")
    if parser.args.angle_distribution:
        print("plot angle distribution.\n")
    if parser.args.output:
        check.check_output_path(parser.args.export, parser.args.output)
    check.check_arguments(parser, parser.args.data_path)
