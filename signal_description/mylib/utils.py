#!/usr/bin/python3
###############################################################################
#                                      __  _ __                               #
#                               __  __/ /_(_) /____                           #
#                              / / / / __/ / / ___/                           #
#                             / /_/ / /_/ / (__  )                            #
#                             \__,_/\__/_/_/____/                             #
#                                                                             #
###############################################################################
import os


def _judge_positive_power(exponent):
    if 3 <= exponent and exponent <= 5:
        return (-3, 'k')
    elif 6 <= exponent and exponent <= 8:
        return (-6, 'M')
    elif 9 <= exponent and exponent <= 11:
        return (-9, 'G')
    elif 12 <= exponent and exponent <= 14:
        return (-12, 'T')
    elif 15 <= exponent and exponent <= 17:
        return (-15, 'P')
    elif 18 <= exponent and exponent <= 20:
        return (-18, 'E')
    elif 21 <= exponent and exponent <= 23:
        return (-21, 'Z')
    elif 24 <= exponent and exponent <= 26:
        return (-24, 'Y')
    else:
        return (None, None)


def _judge_negative_power(exponent):
    if -3 <= exponent and exponent <= -2:
        return (3, 'm')
    elif -6 <= exponent and exponent <= -4:
        return (6, 'μ')
    elif -9 <= exponent and exponent <= -7:
        return (9, 'n')
    elif -12 <= exponent and exponent <= -10:
        return (12, 'p')
    elif -15 <= exponent and exponent <= -11:
        return (15, 'f')
    elif -18 <= exponent and exponent <= -12:
        return (18, 'a')
    elif -21 <= exponent and exponent <= -19:
        return (21, 'z')
    elif -24 <= exponent and exponent <= -22:
        return (24, 'y')
    else:
        return (None, None)


def _judge_SI_prefix(exponent):
    if exponent == 0 or exponent == -1 or exponent == 1 or exponent == 2:
        return (0, None)
    result, si_prefix = _judge_positive_power(exponent)
    if result:
        return (result, si_prefix)
    result, si_prefix = _judge_negative_power(exponent)
    if result:
        return (result, si_prefix)
    print(
        "Error\n"
        "unexpected error\n"
        )
    return (None, None)


def retrieve_filename(path):
    path = path.split('/')[-1]
    result = os.path.splitext(path)[0]
    return result


def convert_to_scientific_notation(value_array):
    exponent_array = list()
    for index, value in enumerate(value_array):
        exponent = 0
        if abs(value) < 1:
            while abs(value) < 1:
                value *= 10
                exponent -= 1
        elif abs(value) >= 10:
            while abs(value) >= 10:
                value /= 10
                exponent += 1
        exponent_array.append(exponent)
    ave_exponent = int(sum(exponent_array)/len(exponent_array))
    print(f"ave_exponent: {ave_exponent}")
    result_exponent, si_prefix = _judge_SI_prefix(ave_exponent)
    return (result_exponent, si_prefix)


def normalize(value_array):
    if abs(max(value_array)) >= abs(min(value_array)):
        max_value = max(value_array)
    else:
        max_value = min(value_array)
    for index, value in enumerate(value_array):
        value_array[index] = value / max_value
    return -value_array
