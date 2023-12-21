#!/usr/bin/python

import sys

import matplotlib as mpl
import matplotlib.pyplot as plt
import signal_description.mylib as mylib


class data:
    pass


def main():
    data.args = sys.argv
    data.rc_file = mpl.matplotlib_fname()
    print(f"using matplotlibrc : {data.rc_file}")
    print(f"package:{__package__}")
    mylib.print_env.print_env(f"using matplotlibrc : {data}")
    for index, path in enumerate(data.args):
        if index != 0:
            print(f"data_path : {path}")
    plt.plot([1, 2, 3, 4])
    plt.ylabel('some number')
    plt.show()
