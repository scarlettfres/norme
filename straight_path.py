#!/usr/bin/env python
import sys
import rospy
from mark_tracker_tools.srv import *
import time
import ConfigParser

import datetime
import naoqi
from naoqi import ALProxy
from os import chdir


def sign(var):
    """
    signe function
    """
    if var > 0:
        return 1
    if var == 0:
        return 0
    return -1


def timeStamped(fname, fmt='%Y-%m-%d-%H-%M-%S_{fname}'):
    """
    create a file_name with the date and hour
    """
    return datetime.datetime.now().strftime(fmt).format(fname=fname)


def read_config_file_section(config_file_path, section):
    """
        Use ConfigParser for reading a configuration file.
        Returns an dictionnary with keys/values of the section.
    """
    config = ConfigParser.ConfigParser()
    config.optionxform = str
    config.read(config_file_path)

    if config.has_section(section):
        configSection = config._sections[section]
        configSection.pop("__name__")

        return {key: value.split() for key, value in configSection.items()}
    else:
        return {}


def go_to_init_zone(NBR_POSITIONEMENT_DEPART, POSITION_DEPART):
    """
        go to POSITION_DEPART
    """
    k = 0
    while k < NBR_POSITIONEMENT_DEPART:

        if len(POSITION_DEPART) == 1:
            rospy.wait_for_service('how_to_go_to_mark')
            how_to_go_to_mark = rospy.ServiceProxy(
                'how_to_go_to_mark', HowToGoToMark)
            resp = how_to_go_to_mark(POSITION_DEPART[0])  # or to 0,0,0 ??
            print resp
            if resp.result == False:     # to fiiiix
                k = k - 1
        if len(POSITION_DEPART) == 3:
            rospy.wait_for_service('how_to_go')
            how_to_go = rospy.ServiceProxy(
                'how_to_go', HowToGo)
            # or to 0,0,0 ??
            resp = how_to_go(
                POSITION_DEPART[0], POSITION_DEPART[1], POSITION_DEPART[2])
            print resp

        # au 2e iteration , pas de grd mvts normalement
        if k == 1 or k == 2:
            if abs(resp.x) > SECU or abs(resp.y) > SECU:
                print "##secuuu :  ", resp.x, resp.y, resp.theta
                print "k=", k
                resp.x = 0
                resp.y = 0
                resp.theta = 0
        print "##I need to :  ", resp.x, resp.y, resp.theta
        if motionProxy.moveIsActive() == False:
            motionProxy.post.moveTo(resp.x, resp.y, resp.theta)
            motionProxy.waitUntilMoveIsFinished()
            k += 1

if __name__ == "__main__":
    straight = read_config_file_section("config.cfg", "Straight")
    PATH = straight['PATH'][0]
    TITLE = straight['TITLE'][0]
    NBR_ESSAIS = int(straight['NBR_ESSAIS'][0])
    POSITION_DEPART = straight['POSITION_DEPART']

    if len(POSITION_DEPART) == 1:
        POSITION_DEPART = [int(POSITION_DEPART[0])]
    elif len(POSITION_DEPART) == 3:
        POSITION_DEPART = [float(
            POSITION_DEPART[0]), float(
            POSITION_DEPART[1]), float(POSITION_DEPART[2])]

    NBR_POSITIONEMENT_DEPART = int(straight['NBR_POSITIONEMENT_DEPART'][0])
    FRAME_TO_TRACK = straight['FRAME_TO_TRACK'][0]
    CMD_VALUE = (float(
        straight['CMD_VALUE'][0]), float(straight['CMD_VALUE'][
            1]), float(straight['CMD_VALUE'][2]))

    SECU = float(straight['SECU'][0])
    IP = straight['IP'][0]
    PORT = int(straight['PORT'][0])
    chdir(PATH)

    try:
        motionProxy = ALProxy("ALMotion", IP, PORT)
        outf = open(timeStamped('straight_line.csv'), 'w')
        outf.write('number,x,y,theta,cmd_value \n')

        for i in range(0, NBR_ESSAIS):
            # go to depart zone
            # 3 times to be sure it is in the right depart zone
            go_to_init_zone(NBR_POSITIONEMENT_DEPART, POSITION_DEPART)
            time.sleep(1)
            begin = time.time()
            # go to command value
            motionProxy.post.moveTo(CMD_VALUE)
            compteur = 0
            while motionProxy.moveIsActive():
                if compteur == 2:   # variable magique
                    rospy.wait_for_service('where_is')
                    where_is = rospy.ServiceProxy('where_is', WhereIs)
                    resp_fin = where_is(FRAME_TO_TRACK, "map")
                    tete_fin = where_is("ar_marker_16", "map")
                    odom_fin = where_is("tf_odom_to_baselink", "map")

                    # save the data in a file
                    message = str(i) + "," + str(time.time() - begin) + "," + str(
                        resp_fin.x) + ","
                    message = message + str(
                        resp_fin.y) + "," + str(resp_fin.theta)
                    message = message + "," + str(tete_fin.x) + "," + str(
                        tete_fin.y) + "," + str(tete_fin.theta)
                    message = message + "," + str(odom_fin.x) + "," + str(
                        odom_fin.y) + "," + str(odom_fin.theta)
                    message = message + "," + str(CMD_VALUE) + "\n"
                    outf.write(message)
                    print "message \n : ", message
                    compteur = 0
                compteur += 1
            time.sleep(1)

    except rospy.ServiceException, e:
        print "Service call failed: %s" % e
    except KeyboardInterrupt:
        outf.close()
