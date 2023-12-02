#!/usr/bin/python

import sys
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as num
import mylib as mylib

class data:
	pass

def main():
	data.args = sys.argv
	data.rc_file = mpl.matplotlib_fname()
	mylib.print_env(data)
	print(f"using matplotlibrc : {data.rc_file}")
	for index,path in enumerate(data.args):
		if index != 0:
			print(f"data_path : {path}")
