#!/usr/bin/python3
###############################################################################
#                                _      __                                    #
#                      ___  ____(_)__  / /_  ___ ___ _  __                    #
#                     / _ \/ __/ / _ \/ __/ / -_) _ \ |/ /                    #
#                    / .__/_/ /_/_//_/\__/__\__/_//_/___/                     #
#                   /_/                 /___/                                 #
###############################################################################
def print_env(data):
    print("\nprint_env")
    print(f"using matplotlibrc : {data.rc_file}")
    print(f"package : {__package__}\n")


def print_argvs(argv):
    for index, path in enumerate(argv):
        if index == 5:
            print("omitted hereafter\n")
            break
        elif index != 0:
            print(f"data_path : {path}\n")
