#!/usr/bin/python3

def print_env(data):
    print('print_env')
    print(f"using matplotlibrc : {data.rc_file}")
    print(f"package:{__package__}")


def print_argvs(argv):
    for index, path in enumerate(argv):
        if index != 0:
            print(f"data_path : {path}")
