#!/usr/bin/python3
###############################################################################
#                               _       __                                    #
#                   ____  _____(_)___  / /_    ___  ____ _   __               #
#                  / __ \/ ___/ / __ \/ __/   / _ \/ __ \ | / /               #
#                 / /_/ / /  / / / / / /_    /  __/ / / / |/ /                #
#                / .___/_/  /_/_/ /_/\__/____\___/_/ /_/|___/                 #
#               /_/                    /_____/                                #
###############################################################################
def print_env(data):
    print("\nprint_env")
    print(f"using matplotlibrc : {data.rc_file}")
    print(f"package : {__package__}\n")


def print_argvs(argv):
    for index, path in enumerate(argv):
        print(f"data_path : {path}\n")
        if index == 4:
            print("omitted hereafter\n")
            break