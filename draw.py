#!/usr/bin/python

import numpy
import csv
from matplotlib import pyplot as plt
import math as m
import cv2
import sys
from matplotlib import pyplot
from math import sin, cos, ceil

# string1 = "fakeshop_16_04_position_prises.txt"
# fichier1 = numpy.genfromtxt(string1, skiprows=1, delimiter=' ')

# x_calcul = fichier1[:, 1] * 100
# y_calcul = fichier1[:, 2]
# z_calcul = fichier1[:, 3]
# rho = fichier1[:, 4]
# theta = fichier1[:, 5]
# phi = fichier1[:, 6]


# print ",,,", x_reel
# phi = phi - phi[0]
# print "phi", phi
# print "x_reel", x_reel
# plt.plot(x_reel,x_calcul,label='x_calcul')
# plt.plot(x_reel,y_calcul)
# plt.plot(x_reel,z_calcul)
# plt.plot(x_reel, abs(x_reel - phi), 'm', label='erreur')

# plt.axis([0, 160, 0, 160])

# plt.title(
#     ' mesures angles 1 marque de 20cm, au sol, pan:-20,tilt:-76.5, bof fin ')
# plt.xlabel('angle_reel (cm)')
# plt.ylabel('angle mesure (degre)')
# plt.legend()

# plt.show()

if __name__ == '__main__':
    docname = "csv/" + sys.argv[1]
    fichier1 = numpy.genfromtxt(docname, skiprows=1, delimiter=',')
    testnum = fichier1[:, 0]
    # print "OOOOOOOOOO", type(testnum)
    # print fichier1

    x = fichier1[:, 1]
    y = fichier1[:, 2]
    theta = fichier1[:, 3]

    x_head = fichier1[:, 4]
    y_head = fichier1[:, 5]
    theta_head = fichier1[:, 6]

    x_odom = fichier1[:, 7]
    y_odom = -fichier1[:, 8]
    theta_odom = fichier1[:, 9]

    command = fichier1[0][10]
    nbr_essais = int(testnum.max()) + 1
    print nbr_essais

    final_tab = [[] for i in range(0, nbr_essais)]
    # print final_tab
    for i in range(0, len(testnum)):    # pour chaque ligne
        for it in range(0, nbr_essais):  # pour chaque essai
            if testnum[i] == it:
                final_tab[it].append(
                    [x[i], y[i], theta[i], x_head[i], y_head[i], theta_head[i], x_odom[i], y_odom[i], theta_odom[i]])
    for it in range(0, nbr_essais):

        print it
        vect = final_tab[it]
        print len(vect)
        vect = numpy.asarray(vect)
        size = len(vect)
        f = plt.figure(it)
        f, (pl1, pl2) = plt.subplots(1, 2, sharex=True, sharey=True)
        pl1.set_title("base_link ")
        pl1.grid(True)
        # print vect
        # pl1.arrow(10, 10, 11, 11, head_width=0.005,
        #           head_length=0.01, color='r', label="odometrie ")
        # pl1.arrow(10, 10, 11, 11, head_width=0.005,
        #           head_length=0.01, label="mark tracking ")
        # pl1.legend()
        # pl1.plot([0, 0], [-2, 2])   # TODO

        # 111111111111111111111111111111111111111111111111111111111
        for i in range(0, size):    # pour chaque ligne

            dx = cos(vect[i][2]) / 20
            dy = sin(vect[i][2]) / 20
            dx_nor = dx / ceil(dx ** 2 + dy ** 2)
            dy_nor = dy / ceil(dx ** 2 + dy ** 2)

            dx_odom = cos(vect[i][8]) / 20
            dy_odom = sin(vect[i][8]) / 20
            dx_odom_nor = dx_odom / ceil(dx_odom ** 2 + dy_odom ** 2)
            dy_odom_nor = dy_odom / ceil(dx_odom ** 2 + dy_odom ** 2)

            pl1.arrow(
                vect[i][0], vect[i][1], dx_nor, dy_nor, head_width=0.005, head_length=0.01)
            pl1.arrow(
                vect[i][6], vect[i][7], dx_odom_nor, dy_odom_nor, head_width=0.005, head_length=0.01, color='r')
        pl1.axis([-2, 2, -2, 2])

        pl2.set_title("head ")
        pl2.grid(True)
        # print vect
        # pl2.arrow(10, 10, 11, 11, head_width=0.005,
        #           head_length=0.01, color='r', label="odometrie ")
        # pl2.arrow(10, 10, 11, 11, head_width=0.005,
        #           head_length=0.01, label="mark tracking ")
        # pl2.legend()

        # pl2.plot([0, 0], [-2, 2])

        # 2222222222222222222222222222222222222222222222222222222
        for i in range(0, size):    # pour chaque ligne
            dx_tete = cos(vect[i][5]) / 20
            dy_tete = sin(vect[i][5]) / 20
            dx_nor_tete = dx_tete / ceil(dx_tete ** 2 + dy_tete ** 2)
            dy_nor_tete = dy_tete / ceil(dx_tete ** 2 + dy_tete ** 2)

            dx_odom = cos(vect[i][8]) / 20
            dy_odom = sin(vect[i][8]) / 20
            dx_odom_nor = dx_odom / ceil(dx_odom ** 2 + dy_odom ** 2)
            dy_odom_nor = dy_odom / ceil(dx_odom ** 2 + dy_odom ** 2)

            pl2.arrow(
                vect[i][3], vect[i][4], dx_nor_tete, dy_nor_tete, head_width=0.005, head_length=0.01)
            pl2.arrow(
                vect[i][6], vect[i][7], dx_odom_nor, dy_odom_nor, head_width=0.005, head_length=0.01, color='r')
        pl2.axis([-2, 2, -2, 2])

        plt.title(sys.argv[1] + "command= " + str(command))
    plt.draw()
    plt.show()
