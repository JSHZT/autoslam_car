#!/usr/bin/env python2

import rospy
import sys
import cv2

from ctypes import *
import math
import random
import cv2
import numpy as np

from math import copysign, sqrt, pow
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import OccupancyGrid 
from nav_msgs.msg import Odometry
from nav_msgs.srv import GetPlan
# from cv_bridge import CvBridge, CvBridgeError
from geometry_msgs.msg import Pose, Point, Quaternion, PoseStamped, Twist
from std_msgs.msg import Int16, Int32, UInt16, Float32, String
from nav_msgs.msg import Path
from actionlib_msgs.msg import GoalID
#from PIL import Image
# import matplotlib.pyplot as plt
import tf
import subprocess

import thread

from obrobot_navigation.msg import PoseDefine,PoseOperation
from obrobot_navigation.srv import PoseManage
# from dynamic_reconfigure.srv import Reconfigure
import dynamic_reconfigure.client

class TOD(object):

    def __init__(self):

        # self.array = []
        self.arrayz = np.array([])
        #self.frontier_pix_y = []
        #self.frontier_pix_x = []
        # self.frontier_nav_x = []
        # self.frontier_nav_y = []
        self.nav_x_start =0
        self.nav_y_start =0
        self.nav_theta_start = 0
        # self.img_count =0
        self.calc_count =0
        self.seq = 0
        self.img_W =0
        self.img_H =0
        self.img_Res =0
        self.img_L =0
        self.car_origin_x =0
        self.car_origin_y =0
        self.frontier_point_x=0
        self.frontier_point_y=0
        self.frontier_point_theta=0
        # self.mapupdateflag = False

        self.finalpose_x_pre=0
        self.finalpose_y_pre=0

        self.unknowcenterx=0
        self.unknowcentery=0
        # self.unknownpose_x_pre=0
        # self.unknownpose_y_pre=0

        self.finish_flag = False
        self.success_flag = False
        self.planning_flag = False
        self.planning_length = 0

        # self.distance_pre=0
        # self.x_pre=0
        # self.y_pre=0
        # self.dummy_point=0
        # self.frontier_point_x1=0
        # self.frontier_point_y1=0
        # self.frontier_point_x2=0
        # self.frontier_point_y2=0

        # self.bridge = CvBridge()

        self.auto_slam_finish = False
        self.auto_slam_finish_cnt = 0
        self.auto_slam_finish_cnt_threshold = 2#yimu

        self.tflasertoodom = tf.TransformListener()

        # self.arm_start_pub = rospy.Publisher("start_detect", Point, queue_size = 10)
        # self.arm_pub = rospy.Publisher("set_motor_angular", Pose, queue_size = 10)
        # rospy.sleep(0.1)

        # self.robot_obs_x_max = 8
        # self.robot_obs_x_min = -4
        # self.robot_obs_y_max = 8
        # self.robot_obs_y_min = 8
        self.already_search_point = []
        # self.no_path_point = []

        self.lastruntime = 0
        self.obstacleback = False

        self.mapmutex = thread.allocate_lock()


        self.point_pub = rospy.Publisher("ob_map_goal", Pose, queue_size = 5)
        self.driver_pub = rospy.Publisher("driver_enable", Int16, queue_size = 5)
        self.goal_pub = rospy.Publisher("move_base_simple/goal", PoseStamped, queue_size = 5)
        self.goal_cancel_pub = rospy.Publisher("move_base/cancel", GoalID, queue_size = 5)
        self.velpub = rospy.Publisher('cmd_vel', Twist, queue_size = 5) 

        self.img_sub = rospy.Subscriber("map", OccupancyGrid, self.image_callback)
        self.goal_sub = rospy.Subscriber("ob_nav_finish", Int16, self.handle_callback)
        self.path_sub = rospy.Subscriber("/move_base/GlobalPlanner/plan", Path, self.path_callback)
        # self.odom_sub = rospy.Subscriber("odom", Odometry, self.odom_callback)
        rospy.Subscriber("scan", LaserScan, self.laserCallback) #zark
        rospy.loginfo("......wait_for_data.....")
        rospy.sleep(3)

        rospy.loginfo("wait for make plan server!")
        rospy.wait_for_service('move_base/make_plan')
        rospy.loginfo("make plan server is working now!")

        # tempclient = dynamic_reconfigure.client.Client('/move_base/TebLocalPlannerROS')
        # tempclient.update_configuration({'xy_goal_tolerance': 0.2, 'yaw_goal_tolerance': 0.1})
        # dynamic_reconfigure.client.Client

        # ta = rospy.get_time()
        # tb = rospy.get_time()
        # while ((tb-ta) < 12) and (not rospy.is_shutdown()):
        #     tb = rospy.get_time()
        #     twist = Twist()
        #     twist.angular.z = 0.5
        #     self.velpub.publish(twist)
        #     rospy.sleep(0.2)   

        # twist.angular.z = 0
        # self.velpub.publish(twist)
        self.finish_flag = True     

    def laserCallback(self, data):
        cnt = 0
        # for tempi in [0, 1, 2, 3, 4, 5, 714, 715, 716, 717, 718, 719]:
        for tempi in range(390, 411):
            if(data.ranges[tempi] > 0.3) and (data.ranges[tempi] < 0.45) :
                cnt += 1
        if(cnt != 0):
            self.obstacleback = True
        else:
            self.obstacleback = False

        # print(self.obstacleback, cnt)

    def getedge(self, map, kernelsize):
        mapsize1 = map.shape[0]
        mapsize2 = map.shape[1]
        # print(mapsize1, mapsize2)
        edgeindex = []
        edgeCnt = 0
        for tempx in range(kernelsize, mapsize1 - kernelsize):
            for tempy in range(kernelsize, mapsize2 - kernelsize):
                if(map[tempx][tempy] == 0 ):
                    findobs = 0
                    freecnt = 0
                    unknowncnt = 0
                    for tempi in range(-kernelsize, kernelsize+1):
                        for tempj in range(-kernelsize, kernelsize+1):
                            tempvalue = map[tempx + tempi][tempy + tempj]
                            if(tempvalue > 0):
                                findobs = 1
                                break
                            elif(tempvalue == 0):
                                freecnt += 1
                            else:
                                unknowncnt += 1
                        if(findobs == 1):
                            break
                    if((findobs == 0) and (freecnt > 8) and (unknowncnt > 8)):
                    # if(findobs == 0):
                        edgeCnt += 1
                        edgeindex.append([tempx, tempy])
                            # print(edgeCnt)
        # print("cnt",edgeCnt)
        # print(edgeindex)
        return edgeCnt, edgeindex
                            
    def getcluster2(self, edgeCnt, edgeindex, maxregionsize):
        # print(edgeindex)
        edgegroup = np.zeros(edgeCnt,dtype=float)
        groupnum = 0
        swapindex = 1

        for tempi in range(0, edgeCnt):
            centerx = edgeindex[tempi][0]
            centery = edgeindex[tempi][1]

            if edgegroup[tempi] == 0:
                groupnum += 1
                # print(groupnum)
                edgegroup[tempi] = groupnum

            for tempj in range(swapindex, edgeCnt):
                if((abs(centerx - edgeindex[tempj][0]) <= maxregionsize) and (abs(centery - edgeindex[tempj][1]) <= maxregionsize)):
                    tempx = edgeindex[swapindex][0]
                    tempy = edgeindex[swapindex][1]
                    edgeindex[swapindex][0] = edgeindex[tempj][0]
                    edgeindex[swapindex][1] = edgeindex[tempj][1]
                    edgeindex[tempj][0] = tempx
                    edgeindex[tempj][1] = tempy
                    edgegroup[swapindex] = groupnum
                    swapindex += 1
        return groupnum, edgegroup, edgeindex

    def whetherCollision(self, globalmap, posx, posy, yaw, xmin, xmax, ymin, ymax):
        globallength = globalmap.shape[0]
        globalmapHalfsize = math.ceil(globallength / 2)
        collisionflag = 0
        for templocalx in range(xmin, xmax+1):
            for templocaly in range(ymin, ymax+1):
                tempglobalx = math.ceil(templocalx * math.cos(yaw) - templocaly * math.sin(yaw) + posx)
                tempglobaly = math.ceil(templocalx * math.sin(yaw) + templocaly * math.cos(yaw) + posy)
                if(globalmap[int(tempglobalx)][int(tempglobaly)] > 0):
                    collisionflag = 1
                    break
            if(1 == collisionflag):
                break;        
        return collisionflag


    def image_callback(self,data):
        # try:
        # if (self.img_count == 0):
        #     self.img_count += 1
        # self.array=data.data
        
        # if(not self.mapmutex.locked()):
        # rospy.loginfo("image_callback: self.mapmutex.acquire()")
        self.mapmutex.acquire()
        # self.mapupdateflag = True
        seq = data.header.seq
        self.seq = seq
        self.img_W = data.info.width
        self.img_H = data.info.height
        self.img_Res = data.info.resolution
        self.car_origin_x = data.info.origin.position.x
        self.car_origin_y = data.info.origin.position.y
        # self.img_L = self.img_W * self.img_H
        self.arrayz = np.array(data.data).reshape((self.img_H, self.img_W))
        # rospy.loginfo("data:%d",self.arrayz[5][5])
        rospy.loginfo("receive map and seq is " + str(seq))
        self.mapmutex.release()
        # rospy.loginfo("image_callback: self.mapmutex.release()")
            # rospy.sleep(0.3)
        # else:
        #     rospy.loginfo("image_callback: map is locked by other thread!")
        # except CvBridgeError as e:
        #     print (e)


    def handle_callback(self,data):
        self.finish_flag = True
        if data.data == 1:
            self.success_flag = True
        elif data.data == 0:
            self.success_flag = False

    def converanglePI(self, angle):
        if angle > math.pi:
            angle -= 2 * math.pi
        elif angle < math.pi:
            angle += 2 * math.pi
        return angle

    def mainloop(self):
        # if data.data == 0:
        #     if self.unknowcenterx != 0 or self.unknowcentery != 0:
        #         self.already_search_point.append([self.unknowcenterx, self.unknowcentery])
        # if(data.data == 1):
        # if (self.img_count > 0):#(self.img_L < 480000): #
            # self.img_count =0
            # self.frontier_nav_y = []
            # self.frontier_nav_x = []
        # if(not self.mapmutex.locked()):
        #     rospy.loginfo(str(self.mapmutex.locked()))
        #     rospy.loginfo("mainloop: self.mapmutex.acquire()")
        #     self.mapmutex.acquire()

            # self.lastruntime = rospy.get_time()
        if(self.img_Res == 0):
            rospy.loginfo("waiting for map")
            rospy.sleep(0.5)
            # self.mapmutex.release()
            # rospy.loginfo("mainloop: self.mapmutex.release()1")
            return

            # #test
            # runtimenow = rospy.get_time()
            # print("aaaa", runtimenow - self.lastruntime, self.auto_slam_finish_cnt, self.obstacleback)
            # if self.auto_slam_finish_cnt == 0 and self.obstacleback is False:
            #     rospy.logwarn("get too closed, going back!!")
            #     # self.already_search_point.pop()
            #     twist = Twist()
            #     twist.linear.x = -0.10
            #     self.velpub.publish(twist)
            #     rospy.sleep(1)
            #     twist.linear.x = 0
            #     self.velpub.publish(twist)
            #     # self.lastruntime = rospy.get_time()

        cannot_reach_value = 100000
        if ((self.finish_flag is True) and (not self.mapmutex.locked())):
            # rospy.loginfo(str(self.mapmutex.locked()))
            # rospy.loginfo("mainloop: self.mapmutex.acquire()")
            self.mapmutex.acquire()

            runtimenow = rospy.get_time()
            if(runtimenow - self.lastruntime < 4) and self.auto_slam_finish_cnt == 0 and self.obstacleback is False:
                rospy.logwarn("get too closed, going back!!")
                if  self.already_search_point:
                    self.already_search_point.pop()
                twist = Twist()
                twist.linear.x = -0.10
                self.velpub.publish(twist)
                rospy.sleep(1)
                twist.linear.x = 0
                self.velpub.publish(twist)
                
            img_Res = self.img_Res
            car_origin_x = self.car_origin_x
            car_origin_y = self.car_origin_y             

            # rospy.sleep(1.0)
            # # self.finish_flag = False
            # img_W = self.img_W
            # img_H = self.img_H
            # # L = self.img_L
            # img_Res = self.img_Res

            # rospy.loginfo("*************************************************")
            # rospy.loginfo("img_width=" + str(img_W) +","+ "img_height=" + str(img_H)+","+ "img_resolution=" + str(img_Res))
            # # rospy.loginfo("calc_count=" + str(self.calc_count) +",""real_width=" + str(real_W) +","+ "real_height=" + str(real_H))
            # rospy.loginfo("car_origin_x=" + str(car_origin_x) +","+ "car_origin_y=" + str(car_origin_y))


            # (_trans, _rot) = self.tflasertoodom.lookupTransform("/map", "/base_footprint", rospy.Time())
            self.tflasertoodom.waitForTransform("/map", "/base_footprint", rospy.Time(), rospy.Duration(30))
            (_trans, _rot) = self.tflasertoodom.lookupTransform("/map", "/base_footprint", rospy.Time())
            _euler1 = tf.transformations.euler_from_quaternion(_rot)
            self.nav_x_start=_trans[0]
            self.nav_y_start=_trans[1]
            self.nav_theta_start = _euler1[2]
            rospy.loginfo("cur_x=" + str(self.nav_x_start) + ","+ "cur_y=" + str(self.nav_y_start) + ","+ "cur_theta=" + str(self.nav_theta_start))

            tempang = self.converanglePI(math.pi/2 - _euler1[2])
            
            posecurrent = [(_trans[1] - car_origin_y)/img_Res, (_trans[0] - car_origin_x)/img_Res, tempang]
            rospy.loginfo("pcur_x=" + str(posecurrent[0]) + ","+ "pcur_y=" + str(posecurrent[1]) + ","+ "pcur_theta=" + str(posecurrent[2]))
    ##################################################
            
            tmpfindobs = 0
            tmpfindunknow = 0
            print("tmpfindobs:", tmpfindobs, "tmpfindunknow", tmpfindunknow)
            tmpx = posecurrent[0]
            tmpy = posecurrent[1]
            # print("car", int(tmpx), int(tmpy), self.arrayz[int(tmpx)][int(tmpy)])
            rospy.loginfo("car" + str([int(tmpx), int(tmpy), self.arrayz[int(tmpx)][int(tmpy)]]))
            # for tempi in range(-10, 11):               
            #     for tempj in range(-10, 11):
            for tempi in range(-5, 6):               
                for tempj in range(-5, 6):
                    # rospy.loginfo(str([int(tmpx + tempi), int(tmpy + tempj), self.arrayz[int(tmpx + tempi)][int(tmpy + tempj)]]))
                    if(self.arrayz[int(tmpx + tempi)][int(tmpy + tempj)] > 0):
                        tmpfindobs = 1
                        break
                    elif(self.arrayz[int(tmpx + tempi)][int(tmpy + tempj)] == -1):
                        tmpfindunknow += 1
                if tmpfindobs == 1:
                    break
            

            print("tmpfindobs:", tmpfindobs, "tmpfindunknow", tmpfindunknow)
            print("seq:", self.seq)

            if (tmpfindunknow > 10) and (tmpfindobs == 0):
                rospy.loginfo("find some unknown point nearby!!")

                ta = rospy.get_time()
                tb = rospy.get_time()
                while ((tb-ta) < 4) and (not rospy.is_shutdown()):
                    tb = rospy.get_time()
                    twist = Twist()
                    twist.angular.z = 0.5
                    self.velpub.publish(twist)
                    rospy.sleep(0.2)   
                
                # twist = Twist()
                # twist.angular.z = 0.5
                # self.velpub.publish(twist)
                # rospy.sleep(5)
                twist.angular.z = 0
                self.velpub.publish(twist)
                rospy.sleep(1)
                self.mapmutex.release()
                # rospy.loginfo("mainloop: self.mapmutex.release()2")
                return
                # rospy.sleep(5)

                
            self.frontier_point_x=0#travis
            self.frontier_point_y=0#travis
            img_W = self.img_W
            img_H = self.img_H
            # L = self.img_L
            img_Res = self.img_Res
            car_origin_x = self.car_origin_x
            car_origin_y = self.car_origin_y             
            # car_pixel_x = math.floor(car_origin_x/img_Res * -1.0)
            # car_pixel_y = math.floor(car_origin_y/img_Res * -1.0)
            real_W = img_W * img_Res
            real_H = img_H * img_Res
            self.calc_count += 1
            rospy.loginfo("*************************************************")
            rospy.loginfo("img_width=" + str(img_W) +","+ "img_height=" + str(img_H)+","+ "img_resolution=" + str(img_Res))
            # rospy.loginfo("calc_count=" + str(self.calc_count) +",""real_width=" + str(real_W) +","+ "real_height=" + str(real_H))
            rospy.loginfo("car_origin_x=" + str(car_origin_x) +","+ "car_origin_y=" + str(car_origin_y))
            #rospy.loginfo("car_pixel_x=" + str(car_pixel_x) +","+ "car_pixel_y=" + str(car_pixel_y))
            # rospy.loginfo("*************************************************")
            #rospy.loginfo(array[0])

            (_trans, _rot) = self.tflasertoodom.lookupTransform("/map", "/base_footprint", rospy.Time())
            _euler1 = tf.transformations.euler_from_quaternion(_rot)
            self.nav_x_start=_trans[0]
            self.nav_y_start=_trans[1]
            self.nav_theta_start = _euler1[2]
            rospy.loginfo("cur_x=" + str(self.nav_x_start) + ","+ "cur_y=" + str(self.nav_y_start) + ","+ "cur_theta=" + str(self.nav_theta_start))

            tempang = self.converanglePI(math.pi/2 - _euler1[2])
            
            posecurrent = [(_trans[1] - car_origin_y)/img_Res, (_trans[0] - car_origin_x)/img_Res, tempang]
            rospy.loginfo("pcur_x=" + str(posecurrent[0]) + ","+ "pcur_y=" + str(posecurrent[1]) + ","+ "pcur_theta=" + str(posecurrent[2]))

            edgeCnt, edgeindex = self.getedge(self.arrayz, 2)
            # print(edgeCnt, edgeindex)
            if edgeCnt == 0:
                rospy.logwarn("no edge found!!!")
                self.frontier_point_x = 0
                self.frontier_point_y = 0
                self.frontier_point_theta = 0
                # self.auto_slam_finish = True
                self.auto_slam_finish_cnt += 1
                if self.auto_slam_finish_cnt >= self.auto_slam_finish_cnt_threshold:
                    self.auto_slam_finish = True
                else:
                    self.auto_slam_finish = False

            else:

                self.driver_pub.publish(0) # disable driver
                            
                groupnum, edgegroup, edgeindex = self.getcluster2(edgeCnt, edgeindex, 10)
                # rospy.loginfo("groupnum:" + str(groupnum) + ", edgegroup:" + str(edgegroup))
                # print(groupnum, edgegroup, edgeindex)
                # globallength = self.arrayz.shape[0]
                # globalmapHalfsize = globallength / 2

                tempgoal = np.zeros((groupnum, 3))
                tempgroupindex = 0
                xmax = 0
                xmin = 0
                ymax = 0
                ymin = 0
                regioncnt = 0
                sumx = 0
                sumy = 0
                sumcnt = 0
                # dmin = 10000
                # dmin2 = 10000
                # dminindex = 0
                # dminindex2 = 0

                tempstartx = PoseStamped()
                tempstartx.header.frame_id = "/map"
                tempstartx.pose.position.x = _trans[0]
                tempstartx.pose.position.y = _trans[1]
                tempstartx.pose.position.z = 0.0
                tempstartx.pose.orientation.x = _rot[0]
                tempstartx.pose.orientation.y = _rot[1]
                tempstartx.pose.orientation.z = _rot[2]
                tempstartx.pose.orientation.w = _rot[3]

                # tempgetplan = rospy.ServiceProxy('move_base/make_plan', GetPlan)
                tempgetplan = rospy.ServiceProxy('/move_base/GlobalPlanner/make_plan', GetPlan)

                for tempi in range(0, edgeCnt + 1):
                    if(tempi < edgeCnt) and (edgegroup[tempi] == tempgroupindex):
                        if(edgeindex[tempi][0] > xmax):
                            xmax = edgeindex[tempi][0]
                        if(edgeindex[tempi][0] < xmin):
                            xmin = edgeindex[tempi][0]
                        if(edgeindex[tempi][1] > ymax):
                            ymax = edgeindex[tempi][1]
                        if(edgeindex[tempi][1] < ymin):
                            ymin = edgeindex[tempi][1]
                        sumx = sumx + edgeindex[tempi][0]
                        sumy = sumy + edgeindex[tempi][1]
                        sumcnt = sumcnt + 1
                    else:
                        # rospy.loginfo("test")
                        # print(xmax - xmin, ymax - ymin, ymax - xmin, xmax - ymin)
                        if((xmax - xmin > 10) or (ymax - ymin > 10) or ((abs(ymax - xmin) + abs(xmax - ymin)) > 10)):
                            tempgoal[regioncnt, 0] = math.ceil(float(sumx) / sumcnt)
                            tempgoal[regioncnt, 1] = math.ceil(float(sumy) / sumcnt)
                            tempgoal[regioncnt, 2] = math.sqrt((tempgoal[regioncnt, 0] - posecurrent[0])**2 + (tempgoal[regioncnt, 1] - posecurrent[1])**2)
                            # if(tempgoal[regioncnt, 2]  < dmin):
                            #     dmin2 = dmin
                            #     dmin = tempgoal[regioncnt, 2]
                            #     dminindex2 = dminindex
                            #     dminindex = regioncnt
                            tempang = math.atan2(tempgoal[regioncnt, 1] - posecurrent[1], tempgoal[regioncnt, 0] - posecurrent[0])
                            tempang -= posecurrent[2]
                            tempang = self.converanglePI(tempang) 
                            # tempgoal[regioncnt, 2] = (1 + abs(tempang)) * math.sqrt((tempgoal[regioncnt, 0] - posecurrent[0])**2 + (tempgoal[regioncnt, 1] - posecurrent[1])**2)
                            # print("pose start")
                            tempgoalx = PoseStamped()
                            tempgoalx.header.frame_id = "/map"
                            tempgoalx.pose.position.x = car_origin_x + (tempgoal[regioncnt, 1]*img_Res)
                            tempgoalx.pose.position.y = car_origin_y + (tempgoal[regioncnt, 0]*img_Res)
                            tempgoalx.pose.position.z = 0.0
                            tempgoalx.pose.orientation.x = 0.0
                            tempgoalx.pose.orientation.y = 0.0
                            tempgoalx.pose.orientation.z = 0.0
                            tempgoalx.pose.orientation.w = 1.0

                            self.planning_length = -1

                            # tempplan = Path()
                            #tempplan = tempgetplan(tempstartx, tempgoalx, 0.1)
                            #self.planning_length = len(tempplan.plan.poses)
		       	    self.goal_pub.publish(tempgoalx)
			    # rospy.sleep(0.1)
			    # rate = rospy.Rate(10)
			    planning_timeout = 0
			    while self.planning_length == -1 and not rospy.is_shutdown():
			        planning_timeout += 1
			        if(planning_timeout > 50):
			            planning_timeout = 0
			            self.goal_pub.publish(tempgoalx)
			            rospy.loginfo("resend goal!")
			        rospy.sleep(0.1)
			        # rate.sleep()
			        # rospy.loginfo("waiting")
			        # rospy.spin()

                            if self.planning_length == 0:
                                tempgoal[regioncnt, 2] = cannot_reach_value
                                # self.no_path_point.append([tempgoal[regioncnt, 0], tempgoal[regioncnt, 1]])
                            
                            else:
                                # rospy.loginfo("planning_length:" + str(self.planning_length))
                                # tempgoal[regioncnt, 2] = (1 + abs(tempang) * 0.3) * self.planning_length
                                tempgoal[regioncnt, 2] = self.planning_length
                            print(regioncnt, tempgoal[regioncnt, 0], tempgoal[regioncnt, 1], tempgoal[regioncnt, 2])
                            goalidtemp = GoalID()
                            self.goal_cancel_pub.publish(goalidtemp) 
                            regioncnt = regioncnt + 1
                            # rospy.sleep(5)
                        
                        if tempi < edgeCnt:
                            tempgroupindex = edgegroup[tempi]
                            xmin = edgeindex[tempi][0]
                            xmax = edgeindex[tempi][0]
                            ymin = edgeindex[tempi][1]
                            ymax = edgeindex[tempi][1]
                            sumx = edgeindex[tempi][0]
                            sumy = edgeindex[tempi][1]
                            sumcnt = 1

                # if((xmax - xmin > 10) or (ymax - ymin > 10) or ((abs(ymax - xmin) + abs(xmax - ymin)) > 10)):
                #     rospy.sleep(5)
                #     tempgoal[regioncnt, 0] = math.ceil(float(sumx) / sumcnt)
                #     tempgoal[regioncnt, 1] = math.ceil(float(sumy) / sumcnt)
                #     tempang = math.atan2(tempgoal[regioncnt, 1] - posecurrent[1], tempgoal[regioncnt, 0] - posecurrent[0])
                #     tempang -= posecurrent[2]
                #     tempang = self.converanglePI(tempang) 
                #     # tempgoal[regioncnt, 2] = (1 + abs(tempang)) * math.sqrt((tempgoal[regioncnt, 0] - posecurrent[0])**2 + (tempgoal[regioncnt, 1] - posecurrent[1])**2)
                #     # print("pose start")
                #     tempgoalx = PoseStamped()
                #     tempgoalx.header.frame_id = "/map"
                #     tempgoalx.pose.position.x = car_origin_x + (tempgoal[regioncnt, 1]*img_Res)
                #     tempgoalx.pose.position.y = car_origin_y + (tempgoal[regioncnt, 0]*img_Res)
                #     tempgoalx.pose.position.z = 0.0
                #     tempgoalx.pose.orientation.x = 0.0
                #     tempgoalx.pose.orientation.y = 0.0
                #     tempgoalx.pose.orientation.z = 0.0
                #     tempgoalx.pose.orientation.w = 1.0

                #     self.planning_length = -1

                #     self.goal_pub.publish(tempgoalx)
                #     # rospy.sleep(5)
                #     # rate = rospy.Rate(10)
                #     while self.planning_length == -1 and not rospy.is_shutdown():
                #         rospy.sleep(0.1)
                #         # rate.sleep()
                #         # rospy.loginfo("waiting")
                #         # rospy.spin()
                #     if self.planning_length == 0:
                #         self.planning_length = 100000
                #     else:
                #         rospy.loginfo("planning_length:" + str(self.planning_length))
                #     tempgoal[regioncnt, 2] = (1 + abs(tempang)) * self.planning_length
                #     print(regioncnt, tempgoal[regioncnt, 0], tempgoal[regioncnt, 1], tempgoal[regioncnt, 2])
                #     goalidtemp = GoalID()
                #     self.goal_cancel_pub.publish(goalidtemp) 
                #     # if(tempgoal[regioncnt, 2]  < dmin):
                #     #     dmin2 = dmin
                #     #     dmin = tempgoal[regioncnt, 2]
                #     #     dminindex2 = dminindex
                #     #     dminindex = regioncnt
                #     regioncnt = regioncnt + 1

                for tempi in range(1, regioncnt):
                    for tempj in range(tempi, 0, -1):
                        if tempgoal[tempj, 2] < tempgoal[tempj-1, 2]:
                            tempx = tempgoal[tempj-1, 0]
                            tempy = tempgoal[tempj-1, 1]
                            tempz = tempgoal[tempj-1, 2]
                            tempgoal[tempj-1, 0] = tempgoal[tempj, 0]
                            tempgoal[tempj-1, 1] = tempgoal[tempj, 1]
                            tempgoal[tempj-1, 2] = tempgoal[tempj, 2]
                            tempgoal[tempj, 0] = tempx
                            tempgoal[tempj, 1] = tempy
                            tempgoal[tempj, 2] = tempz
                        else:
                            break

                self.unknowcenterx = 0
                self.unknowcentery = 0

                for tempi in range(0, regioncnt):
                    in_cannot_reach_flag = 0
                    for tempj in range(0, len(self.already_search_point)):
                        if (abs(tempgoal[tempi, 0] - self.already_search_point[tempj][0])<5 and abs(tempgoal[tempi, 1] - self.already_search_point[tempj][1])<5) or (tempgoal[tempi, 2] == cannot_reach_value):
                            in_cannot_reach_flag = 1
                            break
                    if in_cannot_reach_flag == 0:
                        self.unknowcenterx = tempgoal[tempi, 0]
                        self.unknowcentery = tempgoal[tempi, 1]
                        break

                # if abs(self.unknowcenterx - self.unknownpose_x_pre)<10 and abs(unknowcentery - self.unknownpose_y_pre)<10:
                #     self.unknowcenterx = tempgoal[dminindex2, 0]
                #     self.unknowcentery = tempgoal[dminindex2, 1]


                # self.unknownpose_x_pre = self.unknowcenterx
                # self.unknownpose_y_pre = self.unknowcentery
                print("already_search_point", self.already_search_point)

                if self.unknowcenterx == 0 and self.unknowcentery == 0:
                    rospy.loginfo("there is not any unknown in map")
                    # rospy.set_param("/move_base/TebLocalPlannerROS/xy_goal_tolerance", 0.1)
                    # rospy.set_param("/move_base/TebLocalPlannerROS/yaw_goal_tolerance", 0.05)
                    # tempsetparam = rospy.ServiceProxy('/move_base/TebLocalPlannerROS/set_parameters', Reconfigure)
                    
                    # tempsetparam()
                    tempclient = dynamic_reconfigure.client.Client('/move_base/TebLocalPlannerROS')
                    # tempclient.update_configuration({'xy_goal_tolerance': 0.2})
                    tempclient.update_configuration({'xy_goal_tolerance': 0.1, 'yaw_goal_tolerance': 0.1})

                    # tempparams = {"config: doubles:- {name: 'xy_goal_tolerance', value: 0.1}"}
                    self.frontier_point_x = 0
                    self.frontier_point_y = 0
                    self.frontier_point_theta = 0
                    # self.auto_slam_finish = True
                    if(abs(self.nav_x_start) < 1) and (abs(self.nav_y_start) < 1):
                        self.auto_slam_finish_cnt += 1
                        if self.auto_slam_finish_cnt >= self.auto_slam_finish_cnt_threshold:
                            self.auto_slam_finish = True
                        # elif self.auto_slam_finish_cnt >= (self.auto_slam_finish_cnt_threshold - 1):
                        #     rospy.set_param("/move_base/TebLocalPlannerROS/xy_goal_tolerance", 0.1)
                        #     rospy.set_param("/move_base/TebLocalPlannerROS/yaw_goal_tolerance", 0.05)
                        else:
                            self.auto_slam_finish = False
                        rospy.loginfo("self.auto_slam_finish_cnt:" + str(self.auto_slam_finish_cnt))
                
                else:

                    self.auto_slam_finish_cnt = 0

                    self.already_search_point.append([self.unknowcenterx, self.unknowcentery])
                    
                    # print(tempgoal)
                    rospy.loginfo(["unknowcenterx", self.unknowcenterx, "unknowcentery", self.unknowcentery])

                    # _ang_cur_to_unknown = math.atan2(self.unknowcentery - posecurrent[1], self.unknowcenterx - posecurrent[0])

                    finalpose = np.zeros(3)
                    # nextpose = np.zeros(3)

                    finalpose[0] = self.unknowcenterx
                    finalpose[1] = self.unknowcentery
                    rospy.loginfo("set the unknown center as final pose")

                    directtheta = math.atan2(finalpose[1] - posecurrent[1], finalpose[0] - posecurrent[0])
                    finalpose[2] = directtheta


                    self.finalpose_x_pre=finalpose[0]
                    self.finalpose_y_pre=finalpose[1]
                    self.finalpose_theta_pre=finalpose[2]

                    self.frontier_point_x = car_origin_x + (finalpose[1]*img_Res)
                    self.frontier_point_y = car_origin_y + (finalpose[0]*img_Res)
                    self.frontier_point_theta = math.pi/2 - finalpose[2]

    ###############

            self.driver_pub.publish(1) # enable driver
            rospy.loginfo("frontier_x=" + str(self.frontier_point_x) + ","+ "frontier_y=" + str(self.frontier_point_y) + ","+ "frontier_theta=" + str(self.frontier_point_theta))
            pose = Pose()
            pose.position.x = self.frontier_point_x 
            pose.position.y = self.frontier_point_y
            pose.position.z = 0.0
            pose.orientation.x = 0.0
            pose.orientation.y = 0.0
            pose.orientation.z = math.sin(self.frontier_point_theta / 2.0)
            pose.orientation.w = math.cos(self.frontier_point_theta / 2.0)

            self.point_pub.publish(pose)

            self.lastruntime = rospy.get_time()


            if self.auto_slam_finish is True:
                # self.tflasertoodom.waitForTransform("/map", "/base_footprint", rospy.Time(), rospy.Duration(60))
                # (_trans, _rot) = self.tflasertoodom.lookupTransform("/map", "/base_footprint", rospy.Time())
                poseoperation=PoseOperation()
                poseoperation.opt   = "update"
                poseoperation.id    = 1302
                poseoperation.name  = "initialpose"
                #poseoperation.type  = "origin"
                poseoperation.floor = 1
                # poseoperation.pose.position.x = _trans[0]
                # poseoperation.pose.position.y = _trans[1]
                # poseoperation.pose.position.z = 0    
                # posdefine.pose.orientation.x = _rot[0]
                # posdefine.pose.orientation.y = _rot[1]
                # posdefine.pose.orientation.z = _rot[2]
                # posdefine.pose.orientation.w = _rot[3]
                rospy.wait_for_service('posemanage_server')

                try:
                # if True:
                    posemanage = rospy.ServiceProxy('posemanage_server', PoseManage)
                    resp = posemanage(poseoperation)
                    if "SUCCESS" in resp.status:
                        print(resp.status)
                        rospy.logwarn("save initial pose, id:1302")
                    else:
                        rospy.logwarn("cannot save initial pose, id:1302")
                except rospy.ServiceException, e:
                    print "Service call failed: %s"%e

                rospy.loginfo("---------------------------OB auto slam is finish!!!---------------------------")
                subprocess.call('cd ~/.ob/map; rosrun map_server map_saver -f ob_autoslam', shell=True)
                subprocess.call('cd ~/map; rosrun map_server map_saver -f ob', shell=True)
                # if (self.dummy_point<=29):
                #     self.point_pub.publish(pose)

                # if (30==self.dummy_point):
                #     pose = Pose()
                #     pose.position.x = 90 
                #     self.arm_pub.publish(pose)
                #     rospy.sleep(2)
                # #if (50==self.dummy_point):
                #     point = Point()
                #     point.x = 0
                #     point.y = 0
                #     point.z = 0
                #     self.arm_start_pub.publish(point)
                #     rospy.loginfo("-----------arm_dummy point="+ str(self.dummy_point)+ "------------")

            self.success_flag = False

            self.finish_flag = False

            self.mapmutex.release()
            # rospy.loginfo("mainloop: self.mapmutex.release()3")
            # rospy.sleep(0.3)



##################################################################


    def path_callback(self, data):
        self.planning_length = len(data.poses)
      # print(len(data.poses))
      # rospy.loginfo("planning_length" + str(self.planning_length))

    # def odom_callback(self,data):
    #     self.nav_x_start=data.pose.pose.position.x
    #     self.nav_y_start=data.pose.pose.position.y
    #     rospy.loginfo("nav_x_start=" + str(self.nav_x_start) + ","+ "nav_y_start=" + str(self.nav_y_start))

        
  

  
if __name__ == "__main__":

    rospy.init_node("auto_map_find_goal",anonymous=True)
    tod = TOD()
    while(not rospy.is_shutdown()):
        if tod.auto_slam_finish is False:
            tod.mainloop()
            rospy.sleep(0.3)
        else:
            break
    # rospy.spin()

    
