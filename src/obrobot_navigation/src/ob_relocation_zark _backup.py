#!/usr/bin/env python

import rospy
# from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
# import actionlib
# from actionlib_msgs.msg import *
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import OccupancyGrid 

from geometry_msgs.msg import Pose, Point, Quaternion, PointStamped, PoseWithCovarianceStamped
from geometry_msgs.msg import Twist
from std_msgs.msg import Int16, Int32, UInt16, Float32, String, Bool
import tf
import numpy
import math
from obrobot_navigation.msg import PoseDefine,PoseOperation
from obrobot_navigation.srv import *

class Relocation():
    def __init__(self):

        rospy.loginfo("......start_relocation.....")
        
        self.initial_pose_x = 0
        self.initial_pose_y = 0
        self.initial_pose_angle = 0

        self.initial_pose = PoseWithCovarianceStamped()
        self.initial_pose.header.frame_id = "map"
        self.initial_pose.pose.pose.position.x = 0
        self.initial_pose.pose.pose.position.y = 0
        self.initial_pose.pose.pose.orientation.z = 0
        self.initial_pose.pose.pose.orientation.w = 1
        self.initial_pose.pose.covariance[0] = 0.25 #0.5
        self.initial_pose.pose.covariance[7] = 0.25 #0.5
        self.initial_pose.pose.covariance[35] = 0.0685389194520094 #15deg

        # self.initpoint_pub.publish(initial_pose)
        
        # initial_pose = Pose()
        # initial_pose.orientation.w = 1
        # print(initial_pose.orientation.w)
        self.deltaangle = 0.5 / 180 * math.pi

        self.getmapflag = False
        self.img_W = 0
        self.img_H = 0
        self.img_Res = 0
        self.car_origin_x = 0
        self.car_origin_y = 0
        self.arrayz = numpy.array([])

        self.getlaserflag = False
        self.getlasercnt = 0
        self.laser_data = [0]*720
        self.laser_obs = []

        self.tflasertoodom = tf.TransformListener()
        # self.tflistener = tf.TransformListener()

        # rospy.on_shutdown(self.shutdown)
        rospy.Subscriber("/map", OccupancyGrid, self.map_callback) 
        rospy.Subscriber("/scan", LaserScan, self.getlaserdata)
        rospy.Subscriber("/initialpose", PoseWithCovarianceStamped, self.relocationcallback)
        
        self.initpoint_pub = rospy.Publisher("/initialpose", PoseWithCovarianceStamped, queue_size = 5)

        rospy.sleep(3)

        start_pose = PoseWithCovarianceStamped()

        poseoperation=PoseOperation()
        poseoperation.opt   = "select"
        poseoperation.id    = 1302
        poseoperation.floor = 1

        rospy.wait_for_service('posemanage_server')

        try:
        # if True:
            posemanage = rospy.ServiceProxy('posemanage_server', PoseManage)
            resp = posemanage(poseoperation)
            if "SUCCESS" in resp.status:
                start_pose.pose.pose.position.x = resp.posedefine.pose.position.x
                start_pose.pose.pose.position.y = resp.posedefine.pose.position.y
                start_pose.pose.pose.orientation.x = resp.posedefine.pose.orientation.x
                start_pose.pose.pose.orientation.y = resp.posedefine.pose.orientation.y
                start_pose.pose.pose.orientation.z = resp.posedefine.pose.orientation.z
                start_pose.pose.pose.orientation.w = resp.posedefine.pose.orientation.w
                print(resp.status)
                # print(resp.posedefine)
            else:
                print("cannot get the initial pose")
        except rospy.ServiceException, e:
            print "Service call failed: %s"%e

        self.relocationcallback(start_pose)
        # (_trans, _rot1) = self.tflasertoodom.lookupTransform('base_footprint', 'laser_frame', rospy.Time(0))
        # _euler1 = tf.transformations.euler_from_quaternion(_rot1)
        # yawangle = _euler1[0]

        # print(_trans[0], _trans[1], yawangle)

    def relocationcallback(self, data):
        if ((self.initial_pose.pose.pose.position.x == data.pose.pose.position.x)
        and (self.initial_pose.pose.pose.position.y == data.pose.pose.position.y)
        and (self.initial_pose.pose.pose.orientation.z == data.pose.pose.orientation.z)
        and (self.initial_pose.pose.pose.orientation.w == data.pose.pose.orientation.w)):
            return
        _rot = [0]*4
        _rot[0] = data.pose.pose.orientation.x
        _rot[1] = data.pose.pose.orientation.y
        _rot[2] = data.pose.pose.orientation.z
        _rot[3] = data.pose.pose.orientation.w
        _euler = tf.transformations.euler_from_quaternion(_rot)
        self.initial_pose_x = data.pose.pose.position.x
        self.initial_pose_y = data.pose.pose.position.y
        self.initial_pose_angle = _euler[2]
        print(self.initial_pose_x, self.initial_pose_y, self.initial_pose_angle)
        rospy.loginfo("start")
        # self.getlaserflag = False
        # self.getmapflag = False
        print(self.getlaserflag, self.getmapflag)
        while (self.getlaserflag is False):
            if rospy.is_shutdown():
                break
            rospy.sleep(0.5)
        print(self.getlaserflag, self.getmapflag)
        if (self.getlaserflag is True) and (self.getmapflag is True):
            # print(self.laser_data)
            self.laser_obs = []
            laserpoint = PointStamped()
            basepoint = PointStamped()
            laserpoint.header.stamp = rospy.Time(0)
            laserpoint.header.frame_id = "laser_frame"
            # laserpoint.point.x = 5
            # laserpoint.point.y = 0
            # basepoint = self.tflasertoodom.transformPoint('base_footprint', laserpoint)
            # print("laser", [laserpoint.point.x, laserpoint.point.y])
            # print("base", [basepoint.point.x, basepoint.point.y])
            for tempi in range(0, len(self.laser_data), 6):
                if(self.laser_data[tempi] != 0) and (self.laser_data[tempi] < 2):
                    laserpoint.point.x = -self.laser_data[tempi] * math.cos(self.deltaangle * tempi)
                    laserpoint.point.y = -self.laser_data[tempi] * math.sin(self.deltaangle * tempi)
                    basepoint = self.tflasertoodom.transformPoint('base_footprint', laserpoint)
                    self.laser_obs.append([basepoint.point.x, basepoint.point.y])

            len_laser_obs = len(self.laser_obs)
            print(len_laser_obs)

            maxscore = 0
            resultx = 0
            resulty = 0
            resulta = 0
            # for templocalx in range(xmin, xmax+1):
            #     for templocaly in range(ymin, ymax+1):
            img_Res = self.img_Res
            car_origin_x = self.car_origin_x
            car_origin_y = self.car_origin_y             
            
            # tempangle = 0
            # anglelist = [1] * 0.0174532925
            for tempdeltaangle in numpy.arange(0, math.pi, 0.0174532925*5):
                tempangle = self.initial_pose_angle + tempdeltaangle
                laser_obs_tran = []
                for templaserindex in range(0, len_laser_obs):
                    obstranX = self.laser_obs[templaserindex][0] * math.cos(tempangle) - self.laser_obs[templaserindex][1] * math.sin(tempangle)
                    obstranY = self.laser_obs[templaserindex][0] * math.sin(tempangle) + self.laser_obs[templaserindex][1] * math.cos(tempangle)
                    obsmapX = (obstranY - car_origin_y + self.initial_pose_y)/img_Res
                    obsmapY = (obstranX - car_origin_x + self.initial_pose_x)/img_Res
                    laser_obs_tran.append([obsmapX, obsmapY])
                    
                # print(len(laser_obs_tran))
                # templocalx = 0
                # templocaly = 0
                for templocalx in range(-10, 11, 1):
                    for templocaly in range(-10, 11, 1):
                
                        tempmaxscore = 0
                        for tempindex in range(0, len_laser_obs):
                            obstranXint = int(laser_obs_tran[tempindex][0] + templocalx)
                            obstranYint = int(laser_obs_tran[tempindex][1] + templocaly)
                            if(obstranXint >= self.img_H) or (obstranYint >= self.img_W):
                                continue
                            if(self.arrayz[obstranXint][obstranYint] == 100):
                                tempmaxscore += 1
                            # elif (self.arrayz[obstranXint][obstranYint] == -1):
                            #     tempmaxscore += 0.5

                        if(tempmaxscore > maxscore):
                            maxscore = tempmaxscore
                            resultx = templocalx
                            resulty = templocaly
                            resulta = tempangle
                            if(maxscore > 0.85 * len_laser_obs):
                                break
                            # print(maxscore, templocalx, templocaly, tempangle)
                    if(maxscore > 0.85 * len_laser_obs):
                        break
                # print(maxscore, resultx, resulty, resulta)
                realx = self.initial_pose_x + (resulty*img_Res)
                realy = self.initial_pose_y + (resultx*img_Res)
                realang = resulta

                # print(realx, realy, realang)

                if(maxscore > 0.85 * len_laser_obs):
                    rospy.loginfo("successfully localization!!Get the 0.85 maxscore!!")
                    break

                tempangle = self.initial_pose_angle - tempdeltaangle
                laser_obs_tran = []
                for templaserindex in range(0, len_laser_obs):
                    obstranX = self.laser_obs[templaserindex][0] * math.cos(tempangle) - self.laser_obs[templaserindex][1] * math.sin(tempangle)
                    obstranY = self.laser_obs[templaserindex][0] * math.sin(tempangle) + self.laser_obs[templaserindex][1] * math.cos(tempangle)
                    obsmapX = (obstranY - car_origin_y + self.initial_pose_y)/img_Res
                    obsmapY = (obstranX - car_origin_x + self.initial_pose_x)/img_Res
                    laser_obs_tran.append([obsmapX, obsmapY])
                    
                # print(len(laser_obs_tran))
                # templocalx = 0
                # templocaly = 0
                for templocalx in range(-15, 16, 1):
                    for templocaly in range(-16, 16, 1):
                
                        tempmaxscore = 0
                        for tempindex in range(0, len_laser_obs):
                            obstranXint = int(laser_obs_tran[tempindex][0] + templocalx)
                            obstranYint = int(laser_obs_tran[tempindex][1] + templocaly)
                            if(obstranXint >= self.img_H) or (obstranYint >= self.img_W):
                                continue
                            if(self.arrayz[obstranXint][obstranYint] == 100):
                                tempmaxscore += 1
                            # elif (self.arrayz[obstranXint][obstranYint] == -1):
                            #     tempmaxscore += 0.5

                        if(tempmaxscore > maxscore):
                            maxscore = tempmaxscore
                            resultx = templocalx
                            resulty = templocaly
                            resulta = tempangle
                            if(maxscore > 0.85 * len_laser_obs):
                                break
                            # print(maxscore, templocalx, templocaly, tempangle)
                    if(maxscore > 0.85 * len_laser_obs):
                        break
                # print(maxscore, resultx, resulty, resulta)
                realx = self.initial_pose_x + (resulty*img_Res)
                realy = self.initial_pose_y + (resultx*img_Res)
                realang = resulta

                # print(realx, realy, realang)

                if(maxscore > 0.85 * len_laser_obs):
                    rospy.loginfo("successfully localization!!Get the 0.85 maxscore!!")
                    break

        if(maxscore < 0.3 * len_laser_obs):
             rospy.loginfo("failly localization!!I'm not belong to here!!")

        else:
            print(maxscore, resultx, resulty, resulta)
            print(realx, realy, realang)
            self.initial_pose.pose.pose.position.x = realx
            self.initial_pose.pose.pose.position.y = realy
            self.initial_pose.pose.pose.orientation.z = math.sin(realang / 2.0)
            self.initial_pose.pose.pose.orientation.w = math.cos(realang / 2.0)
            self.initpoint_pub.publish(self.initial_pose)

        rospy.loginfo("stop")

        self.getlaserflag = False
        # self.getmapflag = False

                


            # print(self.laser_obs)
        rospy.loginfo("......end_relocation.....")

    def map_callback(self,data):
        # print("map_callback", self.getmapflag)
        if self.getmapflag is False:
            self.getmapflag = True
            self.img_W = data.info.width
            self.img_H = data.info.height
            self.img_Res = data.info.resolution
            self.car_origin_x = data.info.origin.position.x
            self.car_origin_y = data.info.origin.position.y
            self.arrayz = numpy.array(data.data).reshape((self.img_H, self.img_W))
            print("receive map data")

    def getlaserdata(self, laserdata):
        ''' call back of getting laser data
        '''
        if self.getlaserflag is False:
            self.getlasercnt += 1
            if(self.getlasercnt > 15):
                self.getlasercnt = 0
                self.getlaserflag = True
                for tempi in range(0, 720):
                    self.laser_data[tempi] = laserdata.ranges[tempi]
                print("receive laser data")


    # def shutdown(self):
    #     if self.get_recharge_cmd is True:
    #         self.cancel_goal_pub.publish(True)
    #         self.recharge_pub.publish(0)
    #     rospy.loginfo("Exit Auto Recharge")
    #     rospy.sleep(1)



if __name__ == '__main__':

    rospy.init_node('ob_auto_relocation', anonymous=True)
    relocation = Relocation()
    # while(not rospy.is_shutdown()):
    #     recharger.mainloop()
    rospy.spin()

