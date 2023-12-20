#!/usr/bin/python

import sys
import os

# プロジェクトのルートディレクトリをsys.pathに追加
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

import sys
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as num
from mylib import print_env

class data:
	pass

def main():
	data.args = sys.argv
	data.rc_file = mpl.matplotlib_fname()
	print(f"using matplotlibrc : {data.rc_file}")
	print_env(f"using matplotlibrc : {data}")
	for index,path in enumerate(data.args):
		if index != 0:
			print(f"data_path : {path}")
