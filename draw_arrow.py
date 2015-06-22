#!/usr/bin/python

import numpy
import csv
from matplotlib import pyplot as plt
import math as m
import cv2
import sys
from matplotlib import pyplot
from math import sin, cos, ceil

if __name__ == '__main__':
    docname = "csv/" + sys.argv[1]
    fichier1 = numpy.genfromtxt(docname, skiprows=1, delimiter=',')
    testnum = fichier1[:, 0]
    # print "OOOOOOOOOO", type(testnum)
    # print fichier1
    temps = fichier1[:, 1]
    x = fichier1[:, 2]
    y = fichier1[:, 3]
    theta = fichier1[:, 4]  # - fichier1[0][3]

    x_head = fichier1[:, 5]
    y_head = fichier1[:, 6]
    theta_head = fichier1[:, 7]  # - fichier1[0][6]

    x_odom = fichier1[:, 8]
    y_odom = fichier1[:, 9]
    theta_odom = fichier1[:, 10]  # - fichier1[0][9]

    command = fichier1[0][11]
    nbr_essais = int(testnum.max()) + 1
    print nbr_essais

    final_tab = [[] for i in range(0, nbr_essais)]
    # print final_tab
    for i in range(0, len(testnum)):    # pour chaque ligne
        for it in range(0, nbr_essais):  # pour chaque essai
            if testnum[i] == it:
                final_tab[it].append(
                    [temps[i], x[i], y[i], theta[i], x_head[i], y_head[i], theta_head[i], x_odom[i], y_odom[i], theta_odom[i]])
    for it in range(0, nbr_essais):

        vect = final_tab[it]
        print final_tab[0][0]
        print len(vect)
        vect = numpy.asarray(vect)
        size = len(vect)
        f = plt.figure(it)

        f, (pl1, pl2) = plt.subplots(1, 2, sharex=True, sharey=True)
        pl1.set_title("base_link ")
        pl1.grid(True)

        for i in range(0, size):    # pour chaque ligne

            dx = cos(vect[i][3]) / 20
            dy = sin(vect[i][3]) / 20
            dx_nor = dx / ceil(dx ** 2 + dy ** 2)
            dy_nor = dy / ceil(dx ** 2 + dy ** 2)

            dx_odom = cos(vect[i][9]) / 20
            dy_odom = sin(vect[i][9]) / 20
            dx_odom_nor = dx_odom / ceil(dx_odom ** 2 + dy_odom ** 2)
            dy_odom_nor = dy_odom / ceil(dx_odom ** 2 + dy_odom ** 2)

            pl1.arrow(
                vect[i][1], vect[i][2], dx_nor, dy_nor, head_width=0.005, head_length=0.01)
            pl1.arrow(
                vect[i][7], vect[i][8], dx_odom_nor, dy_odom_nor, head_width=0.005, head_length=0.01, color='r')
        pl1.axis([-2, 2, -2, 2])
        pl1.set_xlabel('x(m)')
        pl1.set_ylabel('y(m)')

        pl2.set_title("head ")
        pl2.grid(True)

        for i in range(0, size):    # pour chaque ligne
            dx_tete = cos(vect[i][6]) / 20
            dy_tete = sin(vect[i][6]) / 20
            dx_nor_tete = dx_tete / ceil(dx_tete ** 2 + dy_tete ** 2)
            dy_nor_tete = dy_tete / ceil(dx_tete ** 2 + dy_tete ** 2)

            dx_odom = cos(vect[i][9]) / 20
            dy_odom = sin(vect[i][9]) / 20
            dx_odom_nor = dx_odom / ceil(dx_odom ** 2 + dy_odom ** 2)
            dy_odom_nor = dy_odom / ceil(dx_odom ** 2 + dy_odom ** 2)

            pl2.arrow(
                vect[i][4], vect[i][5], dx_nor_tete, dy_nor_tete, head_width=0.005, head_length=0.01)
            pl2.arrow(
                vect[i][7], vect[i][8], dx_odom_nor, dy_odom_nor, head_width=0.005, head_length=0.01, color='r')
        pl2.axis([-2, 2, -2, 2])
        pl2.set_xlabel('x(m)')
        pl2.set_ylabel('y(m)')

    titre = "trial " + str(it)
    plt.title(titre)
    plt.draw()
    plt.show()
