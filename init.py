#!/usr/bin/env python
import sys
import rospy
from mark_tracker_tools.srv import *
import time
import naoqi
from naoqi import ALProxy
import ConfigParser
import json
import os


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

if __name__ == "__main__":

    init = read_config_file_section("config.cfg", "Init")
    LOAD = init['LOAD']
    SAVE = init['SAVE']
    INIT = init['INIT']

    MARK_INIT_PLAN = int(init['MARK_INIT_PLAN'][0])

    parser = ConfigParser.SafeConfigParser()
    parser.read("config.cfg")
    MARK_TO_ROBOT = json.loads(parser.get("Init", "MARK_TO_ROBOT"))
    MARK_TO_ROBOT_POSITION = json.loads(
        parser.get("Init", "MARK_TO_ROBOT_POSITION"))

    # print MARK_TO_ROBOT, MARK_TO_ROBOT_POSITION
    ROBOT_FRAME = json.loads(parser.get("Init", "ROBOT_FRAME"))
    print len(ROBOT_FRAME)
    print "MARK_TO_ROBOT", MARK_TO_ROBOT
    print "MARK_TO_ROBOT_POSITION", MARK_TO_ROBOT_POSITION
    print "ROBOT_FRAME", ROBOT_FRAME
    # if we want to save but all the parmaeters are not set
    if (len(MARK_TO_ROBOT) != len(
            MARK_TO_ROBOT_POSITION) or len(MARK_TO_ROBOT) != len(
            ROBOT_FRAME)) and SAVE[1] == 1:

        print """MARK_TO_ROBOT, MARK_TO_ROBOT_POSITION and ROBOT_FRAME
        need to have the same length  """
        os.system("sudo shutdown now -h -k")    # shutdown command

        # MARK_TO_ROBOT = int(init['MARK_TO_ROBOT'][0])
        # MARK_TO_ROBOT_POSITION = init['MARK_TO_ROBOT_POSITION']
        # ROBOT_FRAME = init['ROBOT_FRAME'][0]

    ADD_MARK = int(init['ADD_MARK'][0])
    PATH = init['PATH'][0]

    try:
        # give postion robot
        print "debut"

        if int(INIT[0]) == 1:  # init plan
            rospy.wait_for_service('init_plan')

            init_plan = rospy.ServiceProxy('init_plan', InitPlan)
            # init_plan(num_mark, True to save in a file )
            resp = init_plan(MARK_INIT_PLAN, int(SAVE[0]))
            print "##Initplan", resp.result

        time.sleep(1)
        if int(INIT[1]) == 1:  # init head

            for i in range(0, len(MARK_TO_ROBOT)):

                print i
                rospy.wait_for_service('init_mark_to_robot')
                init_mark_to_robot = rospy.ServiceProxy(
                    'init_mark_to_robot', InitMarkToRobot)
                resp = init_mark_to_robot(
                    MARK_TO_ROBOT[i], MARK_TO_ROBOT_POSITION[i][0],
                    MARK_TO_ROBOT_POSITION[i][1], MARK_TO_ROBOT_POSITION[i][2],
                    ROBOT_FRAME[i], int(SAVE[1]))

                print "##Init mark to head", resp.result

        if int(INIT[2]) == 1:  # init head
            rospy.wait_for_service('add_mark')
            add_mark = rospy.ServiceProxy('add_mark', AddMark)
            resp = add_mark(ADD_MARK, int(SAVE[2]))
            if resp.result == True:
                print"##new mark learnt!"
            else:
                print "##mark overwrited!"

        if int(LOAD[0]) == 1:

            rospy.wait_for_service('load_init')  # init head to robot
            load_init = rospy.ServiceProxy('load_init', LoadInit)
            resp = load_init(PATH, 0)
            print "##Initplan ", resp.result

        if int(LOAD[1]) == 1:

            rospy.wait_for_service('load_init')  # init head to robot
            load_init = rospy.ServiceProxy('load_init', LoadInit)
            resp = load_init(PATH, 1)
            print "##InitMarkToRobot ", resp.result

            # time.sleep(1)  # delay needed to broadcast of tf

        if int(LOAD[2]) == 1:
            rospy.wait_for_service('load_mark')  # load position of the mark
            load_mark = rospy.ServiceProxy('load_mark', LoadMark)
            resp = load_mark(PATH)  # todo
            print "##Initplan ", resp.result

    except rospy.ServiceException, e:
        print "Service"
