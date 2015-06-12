#!/usr/bin/env python
import sys
import rospy
from mark_tracker_tools.srv import *
import time
import naoqi
from naoqi import ALProxy
import ConfigParser


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
    MARK_TO_ROBOT = int(init['MARK_TO_ROBOT'][0])
    MARK_TO_ROBOT_POSITION = init['MARK_TO_ROBOT_POSITION']
    ROBOT_FRAME = init['ROBOT_FRAME'][0]
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
            rospy.wait_for_service('init_mark_to_robot')
            init_mark_to_robot = rospy.ServiceProxy(
                'init_mark_to_robot', InitMarkToRobot)
            resp = init_mark_to_robot(
                MARK_TO_ROBOT, float(MARK_TO_ROBOT_POSITION[
                    0]), float(MARK_TO_ROBOT_POSITION[
                        1]), float(MARK_TO_ROBOT_POSITION[
                            2]), ROBOT_FRAME, int(SAVE[1]))
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
