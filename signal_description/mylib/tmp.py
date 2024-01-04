#!/usr/bin/python3
###############################################################################
#                                 __                                          #
#                                / /___ _  ___                                #
#                               / __/  ' \/ _ \                               #
#                               \__/_/_/_/ .__/                               #
#                                       /_/                                   #
###############################################################################

# plt.axis Determine the range of axes.
import numpy as np
import matplotlib.pyplot as plt


def tmp_straight_line():
    plt.plot([1, 2, 3, 4])
    plt.axis((0, 3, 1, 4))
    plt.ylabel('some number')
    plt.show()


def tmp_x_versus_y_line():
    plt.plot([1, 2, 3, 4], [1, 4, 9, 16])
    plt.xlabel('x label')
    plt.ylabel('y label')
    plt.show()


def tmp_point_graph():
    plt.plot([1, 2, 3, 4], [1, 4, 9, 16], 'bo')
    plt.axis((0, 6, 0, 20))
    plt.xlabel('x label')
    plt.ylabel('y label')
    plt.show()


def tmp_histogram():
    mu, sigma = 100, 15
    x = mu + sigma * np.random.randn(10000)

    # the histogram of the data
    n, bins, patches = plt.hist(x, 50, density=True, facecolor='g', alpha=0.7)

    plt.xlabel('Smarts')
    plt.ylabel('Probability')
    plt.title('Histogram of IQ')
    plt.text(70, .025, r'$\mu=100,\ \sigma=15$')
    plt.axis([40, 160, 0, 0.03])
    plt.grid(True)
    plt.show()


def tmp_exp_graph1():
    # evenly sampled time at 200ms intervals
    t = np.arange(0., 5., 0.2)

    # red dashes, blue squares and green triangles
    plt.plot(t, t, 'r--', t, t**2, 'bs', t, t**3, 'g^')
    plt.show()


def tmp_exp_graph2():
    data = {
        'a': np.arange(50),
        'c': np.random.randint(0, 50, 50),
        'd': np.random.randn(50)
        }
    data['b'] = data['a'] + 10 * np.random.randn(50)
    data['d'] = np.abs(data['d']) * 100

    plt.scatter('a', 'b', c='c', s='d', data=data)
    plt.xlabel('entry a')
    plt.ylabel('entry b')
    plt.show()


def tmp_exp_graph3():
    names = ['group_a', 'group_b', 'group_c']
    values = [1, 10, 100]

    plt.figure(figsize=(9, 3))

    plt.subplot(131)
    plt.bar(names, values)
    plt.subplot(132)
    plt.scatter(names, values)
    plt.subplot(133)
    plt.plot(names, values)
    plt.suptitle('Categorical Plotting')
    plt.show()


def tmp_exp_graph4():
    def f(t):
        return np.exp(-t) * np.cos(2 * np.pi * t)

    t1 = np.arange(0.0, 5.0, 0.1)
    t2 = np.arange(0.0, 5.0, 0.02)

    plt.figure()
    plt.subplot(211)
    plt.plot(t1, f(t1), 'bo', t2, f(t2), 'k')

    plt.subplot(212)
    plt.plot(t2, np.cos(2 * np.pi * t2), 'r--')
    plt.show()


def tmp_exp_graph5():
    t = np.arange(0.0, 5.0, 0.01)
    s = np.cos(2 * np.pi * t)
    line, = plt.plot(t, s, lw=2)

    plt.annotate(
        'local max', xy=(2, 1), xytext=(3, 1.5),
        arrowprops=dict(facecolor='black', shrink=0.05),
        )

    plt.ylim(-2, 2)
    plt.show()
