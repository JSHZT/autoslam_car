#!/usr/bin/env python


import rospy
import os,sys
import json

from obrobot_navigation.srv import *
from geometry_msgs.msg import Pose
from obrobot_navigation.msg import PoseDefine,PoseOperation


def posemanage_client(poseoperation):
    rospy.wait_for_service('posemanage_server')
    try:
        posemanage = rospy.ServiceProxy('posemanage_server', PoseManage)
        resp = posemanage(poseoperation)
        print(resp.status)
        print(resp.posedefine)
        return resp
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e


if __name__ == "__main__":

    #test code
    poseoperation=PoseOperation()
    # poseoperation.opt   = "update"
    # poseoperation.id    = 0
    # poseoperation.name  = "pose1"
    # poseoperation.type  = "normal"
    # poseoperation.floor = 1

    # poseoperation.opt   = "update"
    # poseoperation.id    = 5
    # poseoperation.name  = "pose1"
    # poseoperation.type  = "normal"
    # poseoperation.floor = 1

    poseoperation.opt   = "update"
    poseoperation.id    = 1302
    poseoperation.name  = "initialpose"
    poseoperation.type  = "initial"
    poseoperation.floor = 1
    posemanage_client(poseoperation)

    # poseoperation.opt   = "insert"
    # poseoperation.id    = 1304
    # poseoperation.name  = "chargepose"
    # poseoperation.type  = "charge"
    # poseoperation.floor = 1
    
    posemanage_client(poseoperation)
    
