#!/usr/bin/env python

import rospy
# from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
# import actionlib
# from actionlib_msgs.msg import *
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Pose, Point, Quaternion
from geometry_msgs.msg import Twist
from std_msgs.msg import Int16, Int32, UInt16, Float32, String, Bool
import tf
from obrobot_navigation.msg import PoseDefine,PoseOperation
from obrobot_navigation.srv import *
import math



class Recharge():
    def __init__(self):

        self.recharge_pos = Pose()
        self.recharge_pos.orientation.w = 1
        self.recharge_pos_angle = 0.0
        rospy.on_shutdown(self.shutdown)

        self.success_flag = True
        self.finish_flag = True
        self.ir_data = hex(0)
        self.angular_vel = 0.1
        self.linear_vel = 0.07
        self.my_recharge_status = 0
        self.distancefront = -1
        self.back_vel = -0.1
        self.back_time = 5
        

        self.vel_table = [
        [0, self.linear_vel,	self.linear_vel,	self.linear_vel,	0,	self.linear_vel,	0,	self.linear_vel],
        [0,	0,	0,	0,	0,	0,	0,	0],
        [self.linear_vel,	0,	self.linear_vel,	self.linear_vel,	self.linear_vel,	self.linear_vel,	self.linear_vel,	self.linear_vel],
        [0,	0,	self.linear_vel,	0,	self.linear_vel,	self.linear_vel,	self.linear_vel,	self.linear_vel,],
        [0,	self.linear_vel,	self.linear_vel,	0,	0,	0,	0,	0],
        [self.linear_vel,	0,	self.linear_vel,	self.linear_vel,	0,	self.linear_vel,	self.linear_vel,	self.linear_vel],
        [0,	self.linear_vel,	self.linear_vel,	self.linear_vel,	self.linear_vel,	self.linear_vel,	self.linear_vel,	self.linear_vel],
        [0,	self.linear_vel,	self.linear_vel,	self.linear_vel,	self.linear_vel,	self.linear_vel,	self.linear_vel,	self.linear_vel]]

        self.angular_table = [
        [0,	0,	0,	0,	-self.angular_vel,	0,	-self.angular_vel,	0],
        [self.angular_vel,	self.angular_vel,	self.angular_vel,	self.angular_vel,	self.angular_vel,	self.angular_vel,	self.angular_vel,	self.angular_vel],
        [0,	self.angular_vel,	0,	0,	0,	0,	0,	0],
        [self.angular_vel,	self.angular_vel,	0,	self.angular_vel,	0,	0,	0,	0],
        [-self.angular_vel,	0,	0,	-self.angular_vel,	-self.angular_vel,	-self.angular_vel,	-self.angular_vel,	-self.angular_vel],
        [0,	self.angular_vel,	0,	0,	self.angular_vel,	0,	0,	0],
        [self.angular_vel,	0,	0,	0,	0,	0,	0,	0],
        [self.angular_vel,	0,	0,	0,	0,	0,	0,	0]]


        # print(self.vel_table[0][1], self.vel_table[1][0], self.vel_table[3][2])
        # print(self.angular_table[0][1], self.angular_table[1][0], self.angular_table[3][2])
        self.get_recharge_cmd = False
        self.in_recharing = 0 # 0:not recharge 1:going to recharge point 2:matching the ir 3:start recharging
        rospy.Subscriber("distancefront", Int16, self.distancefrontCallback)
        rospy.Subscriber('ob_nav_finish', Int16, self.receivefinish) 

        rospy.Subscriber('ob_auto_recharge', Bool, self.obautorecharge) 
        rospy.Subscriber('recharge_status', Int16, self.recharge_status_cb)
        rospy.Subscriber('voltage_value', Int32, self.recharge_value_cb)
        # rospy.Subscriber("ob_rechargePose", Pose, self.updaterechargepos)
        rospy.Subscriber('ob_rechargePose_current', Bool, self.updaterechargeposcurrent) 
        rospy.Subscriber('ir_data', Int16, self.ir_data_callback)
        rospy.Subscriber("scan", LaserScan, self.laser_cb) #zark
        rospy.Subscriber("/ob_relocation_finish", Bool, self.relocationfinish_callback)

        self.obstaclefront = False
        self.obstacleback = False
        self.obstaclefront_Cnt = 0     
        self.relocationfinish_flag = False   

        self.recharge_pub = rospy.Publisher("recharge_handle", Int16, queue_size = 5)
        self.goal_pub = rospy.Publisher("ob_map_goal", Pose, queue_size = 5)
        self.cancel_goal_pub = rospy.Publisher("ob_map_goal_cancel", Bool, queue_size = 5)
        self.velpub = rospy.Publisher('cmd_vel', Twist, queue_size = 5) 
        self.inchargingpub = rospy.Publisher('ob_in_charging', Bool, queue_size = 5) 

        self.tflasertoodom = tf.TransformListener()

        rospy.sleep(3)

        rospy.loginfo("......wait_for_recharge_command.....")

    def relocationfinish_callback(self, data):
        if(data.data is True):
            self.relocationfinish_flag = True

    def laser_cb(self, data):
        cnt = 0
        # for tempi in range(270, 451):
        for tempi in range(0, 91):
            tempx = data.ranges[tempi] * math.cos(0.5 * (tempi - 360) / 180 * math.pi)
            if(data.ranges[tempi] > 0.08) and (data.ranges[tempi] < 0.2) :
                cnt += 1
        for tempi in range(710, 801):
            tempx = data.ranges[tempi] * math.cos(0.5 * (tempi - 360) / 180 * math.pi)
            if(data.ranges[tempi] > 0.08) and (data.ranges[tempi] < 0.2) :
                cnt += 1
            tempx = data.ranges[tempi] * math.cos(0.5 * (tempi - 360) / 180 * math.pi)
            if(data.ranges[tempi] > 0.08) and (data.ranges[tempi] < 0.15) :
                cnt += 1
        # if(cnt != 0):
        #     self.obstaclefront = True
        #     self.obstaclefront_Cnt = 10
        # else:
        #     if True is self.obstaclefront and self.obstaclefront_Cnt>0:
        #         self.obstaclefront_Cnt = self.obstaclefront_Cnt - 1
        #         if 0==self.obstaclefront_Cnt:
        #             self.obstaclefront = False
        #     else:
        #         self.obstaclefront = False

        cnt = 0
        for tempi in [0, 1, 2, 3, 4, 5, 714, 715, 716, 717, 718, 719]:
            if(data.ranges[tempi] > 0.3) and (data.ranges[tempi] < 0.45) :
                cnt += 1
        if(cnt != 0):
            self.obstacleback = True
        else:
            self.obstacleback = False


        # print("self.obstaclefront:", self.obst

        # print("self.obstaclefront:", self.obstaclefront,self.obstaclefront_Cnt)

    def recharge_value_cb(self, data):
        if(data.data <= 250) and (self.get_recharge_cmd is False):
            poseoperation=PoseOperation()
            poseoperation.opt   = "select"
            poseoperation.id    = 1304
            poseoperation.floor = 1
            
            rospy.wait_for_service('posemanage_server')
            try:
            # if True:
                posemanage = rospy.ServiceProxy('posemanage_server', PoseManage)
                resp = posemanage(poseoperation)
                if "SUCCESS" in resp.status:
                    self.recharge_pos.position.x = resp.posedefine.pose.position.x
                    self.recharge_pos.position.y = resp.posedefine.pose.position.y
                    self.recharge_pos.position.z = resp.posedefine.pose.position.z
                    self.recharge_pos.orientation.x = resp.posedefine.pose.orientation.x
                    self.recharge_pos.orientation.y = resp.posedefine.pose.orientation.y
                    self.recharge_pos.orientation.z = resp.posedefine.pose.orientation.z
                    self.recharge_pos.orientation.w = resp.posedefine.pose.orientation.w
                    _rot = [self.recharge_pos.orientation.x, self.recharge_pos.orientation.y, self.recharge_pos.orientation.z, self.recharge_pos.orientation.w]
                    self.recharge_pos_angle = tf.transformations.euler_from_quaternion(_rot)[2]
                    print(resp.status)
                    print(resp.posedefine)
                else:
                    print("cannot get the recharge pose")
            except rospy.ServiceException, e:
                print "Service call failed: %s"%e
                
            self.get_recharge_cmd = True
            rospy.loginfo("low voltage!!auto recharge!!")

    def distancefrontCallback(self, data):
        self.distancefront = data.data
        # print("self.distancefront",self.distancefront)        

    def recharge_status_cb(self, data):
        self.my_recharge_status = data.data
        # print("self.my_recharge_status:", self.my_recharge_status)

    def ir_data_callback(self, data):
        self.ir_data = data.data
        # print("self.ir_data",hex(self.ir_data))
        # print("self.ir_data",self.ir_data/256)
        # print("self.ir_data",self.ir_data&0xff)

    def receivefinish(self, data):
        self.finish_flag = True
        if data.data == 1:
            self.success_flag = True
        elif data.data == 0:
            self.success_flag = False

    def obautorecharge(self, data):
        if(data.data is True):
            poseoperation=PoseOperation()
            poseoperation.opt   = "select"
            poseoperation.id    = 1304
            poseoperation.floor = 1
            
            rospy.wait_for_service('posemanage_server')
            try:
            # if True:
                posemanage = rospy.ServiceProxy('posemanage_server', PoseManage)
                resp = posemanage(poseoperation)
                if "SUCCESS" in resp.status:
                    self.recharge_pos.position.x = resp.posedefine.pose.position.x
                    self.recharge_pos.position.y = resp.posedefine.pose.position.y
                    self.recharge_pos.position.z = resp.posedefine.pose.position.z
                    self.recharge_pos.orientation.x = resp.posedefine.pose.orientation.x
                    self.recharge_pos.orientation.y = resp.posedefine.pose.orientation.y
                    self.recharge_pos.orientation.z = resp.posedefine.pose.orientation.z
                    self.recharge_pos.orientation.w = resp.posedefine.pose.orientation.w
                    _rot = [self.recharge_pos.orientation.x, self.recharge_pos.orientation.y, self.recharge_pos.orientation.z, self.recharge_pos.orientation.w]
                    self.recharge_pos_angle = tf.transformations.euler_from_quaternion(_rot)[2]
                    print(resp.status)
                    print(resp.posedefine)
                else:
                    print("cannot get the recharge pose")
            except rospy.ServiceException, e:
                print "Service call failed: %s"%e
                
            self.get_recharge_cmd = True
            rospy.loginfo("receive auto charge command!")
        else:
            # if self.get_recharge_cmd is True:
            # if self.in_recharing == 3:
            #     print("back!!")
            #     twist = Twist()
            #     twist.linear.x = -0.2
            #     self.velpub.publish(twist)
            #     rospy.sleep(2)
            #     twist.linear.x = 0
            #     twist.angular.z = 0
            #     self.velpub.publish(twist)
                
            # self.in_recharing = 0
            self.recharge_pub.publish(0)
            self.get_recharge_cmd = False
            rospy.loginfo("receive cancel auto charge command!")
            
    # def updaterechargepos(self, data):
    #     self.recharge_pos.position.x = data.position.x
    #     self.recharge_pos.position.y = data.position.y
    #     rospy.loginfo("self.recharge_pos_x:" + str(self.recharge_pos.position.x) + ",self.recharge_pos_y:" + str(self.recharge_pos.position.y))

    def updaterechargeposcurrent(self, data):
        if(data.data is True):
            try:
            # if 1:
                poseoperation=PoseOperation()
                poseoperation.opt   = "update"
                poseoperation.id    = 1304
                poseoperation.name  = "chargepose"
                poseoperation.type  = "charger"
                poseoperation.floor = 1
                
                rospy.wait_for_service('posemanage_server')
                try:
                    posemanage = rospy.ServiceProxy('posemanage_server', PoseManage)
                    resp = posemanage(poseoperation)
                    print(resp.status)
                    print(resp.posedefine)
                except rospy.ServiceException, e:
                    print "Service call failed: %s"%e
                
                # (_trans, _rot) = self.tflasertoodom.lookupTransform("/map", "/base_footprint", rospy.Time())
                # self.recharge_pos.position.x = _trans[0]
                # self.recharge_pos.position.y = _trans[1]
                # self.recharge_pos.position.z = 0
                # self.recharge_pos.orientation.x = _rot[0]
                # self.recharge_pos.orientation.y = _rot[1]
                # self.recharge_pos.orientation.z = _rot[2]
                # self.recharge_pos.orientation.w = _rot[3]
                # rospy.loginfo("self.recharge_pos_x:" + str(self.recharge_pos.position.x) + ",self.recharge_pos_y:" + str(self.recharge_pos.position.y))
            except:
		        rospy.logerr("cannot get the transform from map to base_footprint!!")

    def mainloop(self):
        if self.get_recharge_cmd is True:
            self.inchargingpub.publish(True)
            # while not rospy.is_shutdown():
            while not rospy.is_shutdown() and self.get_recharge_cmd is True:

                # elif (self.ir_data == hex(0x603)) or  (self.ir_data == hex(0x602)) :
                #     print("turn right")
                # elif (self.ir_data == hex(0x603)) or  (self.ir_data == hex(0x602)) :
                #     print("turn left")
                # print(self.ir_data & hex(0x202))
                # if self.in_recharing == 0:
                #     # self.in_recharing = 2
                #     # twist = Twist()
                #     # twist.linear.x = self.linear_vel
                #     # self.velpub.publish(twist)
                #     # rospy.sleep(1)
                #     # twist.linear.x = 0
                #     # self.velpub.publish(twist)
                #     # print(hex(0x703))
                #     print("go")

                rospy.loginfo("going to recharging point")
                self.in_recharing = 1
                self.finish_flag = False
                self.success_flag = False
                goal = Pose()
                goal.position.x = self.recharge_pos.position.x
                goal.position.y = self.recharge_pos.position.y
                goal.orientation.x = self.recharge_pos.orientation.x
                goal.orientation.y = self.recharge_pos.orientation.y
                goal.orientation.z = self.recharge_pos.orientation.z
                goal.orientation.w = self.recharge_pos.orientation.w
                print(goal)
                self.goal_pub.publish(goal)
                recharge_try_cnt = 0
                while not rospy.is_shutdown() and self.get_recharge_cmd is True:
                    rospy.sleep(0.1)
                    if self.finish_flag is True:
                        if self.success_flag is True:
                            # self.get_recharge_cmd = False
                            rospy.loginfo("reach recharge point and start recharge")
                            self.in_recharing = 2
                            self.recharge_pub.publish(1)
                            break
                        else:
                            recharge_try_cnt += 1
                            # if recharge_try_cnt > 5:
                            #     # self.get_recharge_cmd = False
                            #     rospy.logwarn("cannot go to recharge point!!")
                            #     self.in_recharing = 0
                            #     break
                            self.finish_flag = False
                            self.goal_pub.publish(goal)
                            rospy.loginfo("recharge_try_cnt:" + str(recharge_try_cnt))
                
                find_ir = False
                turnning_cnt = 0
                find_ir_left = False
                find_ir_right = False
                find_edge = 0
                left_edge = 0
                right_edge = 0
                center_angle = 0
                ir_data_last = self.ir_data
                rotate_direction = 1
                find_ir_cnt = 0
                matching_cnt = 0
                find_ir_init_flag = False
                obstaclefindcnt = 0
                rotation_cnt = 0
                move_left = 0
                move_right = 0
                while (not rospy.is_shutdown()) and (self.get_recharge_cmd is True) and (self.in_recharing >= 2):
                    if find_ir is False:
                        print("self.my_recharge_status:", self.my_recharge_status)
                        print("self.ir_data",hex(self.ir_data))

                        if find_ir_init_flag is False:
                            # find_ir_init_flag = True
                            # if (self.ir_data == int(0x404)):
                            #     rotate_direction = -1
                            if self.finish_flag is True:
                                self.finish_flag = False
                                if self.success_flag is True:
                                    self.success_flag = False
                                    recharge_try_cnt = 0

                                    if self.ir_data & int(0x202):
                                        find_ir_init_flag = True
                                    elif self.ir_data & int(0x101):

                                        rospy.loginfo("move left")
                                        # (_trans, _rot) = self.tflasertoodom.lookupTransform("/map", "/base_footprint", rospy.Time())
                                        # _euler1 = tf.transformations.euler_from_quaternion(_rot)
                                        move_left += 0.2
                                        _temp_yaw = self.recharge_pos_angle + math.pi/2 # 0.5 is about 30 degrees
                                        goal = Pose()
                                        goal.position.x = self.recharge_pos.position.x + move_left * math.cos(_temp_yaw)
                                        goal.position.y = self.recharge_pos.position.y + move_left * math.sin(_temp_yaw)
                                        goal.orientation.x = self.recharge_pos.orientation.x
                                        goal.orientation.y = self.recharge_pos.orientation.y
                                        goal.orientation.z = self.recharge_pos.orientation.z
                                        goal.orientation.w = self.recharge_pos.orientation.w
                                        # print(goal)
                                        self.goal_pub.publish(goal)

                                    elif self.ir_data & int(0x404):
                                        rospy.loginfo("move right")
                                        # (_trans, _rot) = self.tflasertoodom.lookupTransform("/map", "/base_footprint", rospy.Time())
                                        # _euler1 = tf.transformations.euler_from_quaternion(_rot)
                                        move_right += 0.2
                                        _temp_yaw = self.recharge_pos_angle - math.pi/2 # 0.5 is about 30 degrees
                                        goal = Pose()
                                        goal.position.x = self.recharge_pos.position.x + move_right * math.cos(_temp_yaw)
                                        goal.position.y = self.recharge_pos.position.y + move_right * math.sin(_temp_yaw)
                                        goal.orientation.x = self.recharge_pos.orientation.x
                                        goal.orientation.y = self.recharge_pos.orientation.y
                                        goal.orientation.z = self.recharge_pos.orientation.z
                                        goal.orientation.w = self.recharge_pos.orientation.w
                                        # print(goal)
                                        self.goal_pub.publish(goal)

                                    else:
                                        turnning_cnt += 1
                                        if (turnning_cnt >= 25):
                                            turnning_cnt = 0
                                            rospy.loginfo("already move one cycle")
                                            rotation_cnt += 1
                                            if(rotation_cnt == 1):
                                                rospy.loginfo("no charger! move left")
                                                move_left = 0.5
                                                # (_trans, _rot) = self.tflasertoodom.lookupTransform("/map", "/base_footprint", rospy.Time())
                                                # _euler1 = tf.transformations.euler_from_quaternion(_rot)
                                                _temp_yaw = self.recharge_pos_angle + math.pi/2 # 0.5 is about 30 degrees
                                            elif(rotation_cnt == 2):
                                                rospy.loginfo("no charger! move right")
                                                move_right = 0.5
                                                # (_trans, _rot) = self.tflasertoodom.lookupTransform("/map", "/base_footprint", rospy.Time())
                                                # _euler1 = tf.transformations.euler_from_quaternion(_rot)
                                                _temp_yaw = self.recharge_pos_angle - math.pi/2 # 0.5 is about 30 degrees

                                            if(rotation_cnt <= 2):
                                            # print(goal)
                                                goal = Pose()
                                                goal.position.x = self.recharge_pos.position.x + 0.5 * math.cos(_temp_yaw)
                                                goal.position.y = self.recharge_pos.position.y + 0.5 * math.sin(_temp_yaw)
                                                goal.orientation.x = self.recharge_pos.orientation.x
                                                goal.orientation.y = self.recharge_pos.orientation.y
                                                goal.orientation.z = self.recharge_pos.orientation.z
                                                goal.orientation.w = self.recharge_pos.orientation.w
                                                self.goal_pub.publish(goal)
                                            else:
                                                break
                                                

                                        else:
                                            # turnning_cnt < 25
                                            rospy.loginfo("turning around and turnning_cnt:"+str([turnning_cnt]))
                                            (_trans, _rot) = self.tflasertoodom.lookupTransform("/map", "/base_footprint", rospy.Time())
                                            _euler1 = tf.transformations.euler_from_quaternion(_rot)
                                            if turnning_cnt==7:
                                                turnning_cnt = 19
                                                _goal_yaw = _euler1[2] + 12*rotate_direction* 15 * math.pi/180 # 0.5 is about 30 degrees
                                            else:
                                                _goal_yaw = _euler1[2] + rotate_direction* 15 * math.pi/180 # 0.5 is about 30 degrees                                                
                                            goal = Pose()
                                            goal.position.x = _trans[0]
                                            goal.position.y = _trans[1]
                                            goal.orientation.x = 0
                                            goal.orientation.y = 0
                                            goal.orientation.z = math.sin(_goal_yaw / 2.0)
                                            goal.orientation.w = math.cos(_goal_yaw / 2.0)
                                            # print(goal)
                                            self.goal_pub.publish(goal)
                                            rospy.loginfo("goal:"+str([goal.position.x, goal.position.y, _goal_yaw]))
                                            rospy.loginfo("cannot find the recharger!!")
                                            # rospy.sleep(0.5)

                                else:                                    
                                    if recharge_try_cnt < 3:
                                        recharge_try_cnt += 1
                                        self.goal_pub.publish(goal)
                                    else:
                                        recharge_try_cnt = 0
                                        self.finish_flag = True
                                        self.success_flag = True
                                    rospy.loginfo("recharge_try_cnt:" + str(recharge_try_cnt))


                        else:

                            # 0819
                            # if (self.ir_data != 0) and (ir_data_last == 0):
                            #     find_edge += 1
                            #     rotate_direction *= -1
                            #     (_trans, _rot) = self.tflasertoodom.lookupTransform("/map", "/base_footprint", rospy.Time())
                            #     _euler1 = tf.transformations.euler_from_quaternion(_rot)
                            #     right_edge = _euler1[2]
                            # if (self.ir_data == 0) and (ir_data_last != 0):
                            #     find_edge += 1
                            #     rotate_direction *= -1
                            #     (_trans, _rot) = self.tflasertoodom.lookupTransform("/map", "/base_footprint", rospy.Time())
                            #     _euler1 = tf.transformations.euler_from_quaternion(_rot)
                            #     left_edge = _euler1[2]
                            # ir_data_last = self.ir_data
                            
                            # 0819
                            # if self.ir_data & int(0x101):
                            #     find_ir_right = True
                            # if self.ir_data & int(0x404):
                            #     find_ir_left = True

                            if self.ir_data & int(0x202):
                                find_ir = True
                                rospy.loginfo("find the recharger!!")
                            # elif (find_ir_left is True) and (find_ir_right is True):
                            #     find_ir_left = False
                            #     find_ir_right = False
                            #     find_ir = True
                            #     rospy.loginfo("find the recharger!! left and right")

                            # 0819
                            # else:
                            #     print(self.finish_flag, self.success_flag, find_ir, find_ir_left, find_ir_right)
                            #     if self.finish_flag is True:
                            #         self.finish_flag = False
                            #         if self.success_flag is True:
                            #             self.success_flag = False

                            #             if find_edge >= 2:
                            #                 rospy.loginfo("already find two edges")
                            #                 find_edge = 0
                            #                 if(right_edge > left_edge):
                            #                     right_edge += 2 * math.pi
                            #                 center_angle = (left_edge + right_edge) / 2
                            #                 turnning_cnt = 25
                                            
                                        
                            #             turnning_cnt += 1
                            #             if (turnning_cnt >= 25):
                            #                 rospy.loginfo("already move one cycle")
                            #                 turnning_cnt = 0
                            #                 if (find_ir_left is True) and (find_ir_right is True):
                            #                     find_ir_left = False
                            #                     find_ir_right = False
                            #                     find_ir = True
                            #                     rospy.loginfo("find the recharger!!")
                            #                     rospy.loginfo("move to middle point")
                            #                     (_trans, _rot) = self.tflasertoodom.lookupTransform("/map", "/base_footprint", rospy.Time())
                            #                     # _euler1 = tf.transformations.euler_from_quaternion(_rot)
                            #                     if(right_edge > left_edge):
                            #                         right_edge += 2 * math.pi
                            #                     _temp_yaw =  (left_edge + right_edge) / 2# 0.5 is about 30 degrees
                            #                     goal = Pose()
                            #                     goal.position.x = _trans[0]
                            #                     goal.position.y = _trans[1]
                            #                     goal.orientation.x = 0
                            #                     goal.orientation.y = 0
                            #                     goal.orientation.z = math.sin(_temp_yaw/2)
                            #                     goal.orientation.w = math.cos(_temp_yaw/2)
                            #                     # print(goal)
                            #                     self.goal_pub.publish(goal)
                            #                     rospy.loginfo("goal:"+str([goal.position.x, goal.position.y, _goal_yaw]))

                                            
                            #                 elif (find_ir_left is True):
                            #                     find_ir_left = False
                            #                     rospy.loginfo("cannot find the recharger!!")
                            #                     rospy.loginfo("move to right point")
                            #                     (_trans, _rot) = self.tflasertoodom.lookupTransform("/map", "/base_footprint", rospy.Time())
                            #                     # _euler1 = tf.transformations.euler_from_quaternion(_rot)
                            #                     _temp_yaw = self.recharge_pos_angle - math.pi/2 # 0.5 is about 30 degrees
                            #                     goal = Pose()
                            #                     goal.position.x = _trans[0] + 0.2 * math.cos(_temp_yaw)
                            #                     goal.position.y = _trans[1] + 0.2 * math.sin(_temp_yaw)
                            #                     goal.orientation.x = self.recharge_pos.orientation.x
                            #                     goal.orientation.y = self.recharge_pos.orientation.y
                            #                     goal.orientation.z = self.recharge_pos.orientation.z
                            #                     goal.orientation.w = self.recharge_pos.orientation.w
                            #                     # print(goal)
                            #                     self.goal_pub.publish(goal)
                            #                     rospy.loginfo("goal:"+str([goal.position.x, goal.position.y, _goal_yaw]))

                            #                 elif (find_ir_right is True):
                            #                     find_ir_right = False
                            #                     rospy.loginfo("cannot find the recharger!!")
                            #                     rospy.loginfo("move to left point")
                            #                     (_trans, _rot) = self.tflasertoodom.lookupTransform("/map", "/base_footprint", rospy.Time())
                            #                     # _euler1 = tf.transformations.euler_from_quaternion(_rot)
                            #                     _temp_yaw = self.recharge_pos_angle + math.pi/2 # 0.5 is about 30 degrees
                            #                     goal = Pose()
                            #                     goal.position.x = _trans[0] + 0.2 * math.cos(_temp_yaw)
                            #                     goal.position.y = _trans[1] + 0.2 * math.sin(_temp_yaw)
                            #                     goal.orientation.x = self.recharge_pos.orientation.x
                            #                     goal.orientation.y = self.recharge_pos.orientation.y
                            #                     goal.orientation.z = self.recharge_pos.orientation.z
                            #                     goal.orientation.w = self.recharge_pos.orientation.w
                            #                     # print(goal)
                            #                     self.goal_pub.publish(goal)
                            #                     rospy.loginfo("goal:"+str([goal.position.x, goal.position.y, _goal_yaw]))
                                                
                            #                 else:
                            #                     rospy.loginfo("no recharger here!!")

                            #             else:
                            #                 # turnning_cnt < 25
                            #                 rospy.loginfo("turning around and turnning_cnt:"+str([turnning_cnt]))
                            #                 (_trans, _rot) = self.tflasertoodom.lookupTransform("/map", "/base_footprint", rospy.Time())
                            #                 _euler1 = tf.transformations.euler_from_quaternion(_rot)
                            #                 _goal_yaw = _euler1[2] + rotate_direction* 15 * math.pi/180 # 0.5 is about 30 degrees
                            #                 goal = Pose()
                            #                 goal.position.x = _trans[0]
                            #                 goal.position.y = _trans[1]
                            #                 goal.orientation.x = 0
                            #                 goal.orientation.y = 0
                            #                 goal.orientation.z = math.sin(_goal_yaw / 2.0)
                            #                 goal.orientation.w = math.cos(_goal_yaw / 2.0)
                            #                 # print(goal)
                            #                 self.goal_pub.publish(goal)
                            #                 rospy.loginfo("goal:"+str([goal.position.x, goal.position.y, _goal_yaw]))
                            #                 rospy.loginfo("cannot find the recharger!!")
                            #                 # rospy.sleep(0.5)

                            #         else:
                            #             self.goal_pub.publish(goal)
                            #             rospy.loginfo("recharge_try_cnt:" + str(recharge_try_cnt))

                        rospy.sleep(1)
                                    


                    else:
                        # find_ir is true


                        # rospy.sleep(0.05)
                        # self.finish_flag = True
                        # self.success_flag = True
                        # if self.finish_flag is True:
                        #     if self.success_flag is True:
                        if self.my_recharge_status == 0:

                            # print("self.ir_data",hex(self.ir_data))
                            # print("self.my_recharge_status:", self.my_recharge_status)
                            if self.obstaclefront is True:
                                print("obstacle!!",obstaclefindcnt)
                                obstaclefindcnt += 1
                                if obstaclefindcnt == 1:
                                    rospy.loginfo("try!!")
                                    twist = Twist()
                                    twist.linear.x = 0.05
                                    ta = rospy.get_time()
                                    tb = rospy.get_time()
                                    while ((tb-ta) < 1.0) and (not rospy.is_shutdown()):
                                        tb = rospy.get_time()
                                        self.velpub.publish(twist)
                                        # rospy.sleep(0.05)                                  
                                    twist.linear.x = 0
                                    twist.angular.z = 0
                                elif(obstaclefindcnt > 15):
                                    rospy.loginfo("find obstacle!! back!!")
                                    twist = Twist()
                                    twist.linear.x = self.back_vel
                                    # ta = rospy.get_time()
                                    tb = rospy.get_time()
                                    delta_time = 0
                                    temp_time = 0
                                    while ((temp_time) < self.back_time) and (not rospy.is_shutdown()):
                                        delta_time = rospy.get_time() - tb
                                        tb = rospy.get_time()
                                        if self.obstacleback is False:
                                            temp_time += delta_time
                                            self.velpub.publish(twist)
                                        # rospy.sleep(0.05)                                  
                                    twist.linear.x = 0
                                    twist.angular.z = 0
                                    self.velpub.publish(twist)
                                    break
                                rospy.sleep(1)
                            else:
                                obstaclefindcnt = 0
                                twist = Twist()
                                # temp_linear_vel_turn = self.distancefront*0.02-0.1
                                # if temp_linear_vel_turn<0:
                                #     temp_linear_vel_turn = 0
                                # elif temp_linear_vel_turn>1:
                                #     temp_linear_vel_turn = 1
                                # temp_linear_vel_turn = temp_linear_vel_turn * self.linear_vel

                                if self.ir_data == 0:
                                    # self.in_recharing = 3
                                    twist.linear.x = 0
                                    twist.angular.z = 0
                                    print("stop!! cannot find recharger!!")
                                    if find_ir_cnt < 40:
                                        find_ir_cnt += 1
                                    else:
                                        find_ir = False
                                    rospy.sleep(1)
                                    # break

                                else:
                                    # print("self.ir_data",self.ir_data/256)
                                    # print("self.ir_data",self.ir_data&0xff)
                                    print("left:", self.ir_data/256, "right:", self.ir_data&0xff)
                                    twist.linear.x = self.vel_table[self.ir_data/256][self.ir_data&0xff]
                                    # if twist.linear.x ==0:
                                    #     twist.linear.x =0.01
                                    twist.angular.z = self.angular_table[self.ir_data/256][self.ir_data&0xff]
                                    # print("twist.linear.x:", twist.linear.x, "twist.angular.z:", twist.angular.z)
                                    # self.velpub.publish(twist)
                                    tb = rospy.get_time()
                                    delta_time = 0
                                    temp_time = 0
                                    while ((temp_time) < 0.1) and (not rospy.is_shutdown()):
                                        delta_time = rospy.get_time() - tb
                                        tb = rospy.get_time()
                                        temp_time += delta_time
                                        self.velpub.publish(twist)
                                # elif self.ir_data & int(0x002):
                                    
                                #     if self.ir_data & int(0x200):
                                #         twist.linear.x = self.linear_vel
                                #         twist.angular.z = 0
                                #         print("go straight")
                                #     else:
                                #         # twist.linear.x = temp_linear_vel_turn
                                #         twist.linear.x = 0
                                #         twist.angular.z = -self.angular_vel
                                #         # (_trans, _rot) = self.tflasertoodom.lookupTransform("/map", "/base_footprint", rospy.Time())
                                #         # _euler1 = tf.transformations.euler_from_quaternion(_rot)
                                #         print("turn straight right")
                                #     # print(hex(0x703))
                                # #     print("go")
                                # elif self.ir_data & int(0x200):
                                #     # twist.linear.x = temp_linear_vel_turn
                                #     twist.linear.x = 0
                                #     twist.angular.z = self.angular_vel
                                #     print("turn straight left")
                                # # elif (self.ir_data & int(0x004)) and (self.ir_data & int(0x400)):
                                # #     twist.linear.x = self.linear_vel
                                # #     twist.angular.z = -self.angular_vel
                                # #     print("turn straight right")
                                # # elif (self.ir_data & int(0x001)) and (self.ir_data & int(0x100)):
                                # #     twist.linear.x = self.linear_vel
                                # #     twist.angular.z = self.angular_vel
                                # #     print("turn straight left")
                                # elif self.ir_data & int(0x004):
                                #     # twist.linear.x = temp_linear_vel_turn
                                #     twist.linear.x = 0
                                #     twist.angular.z = -self.angular_vel
                                #     print("turn right")
                                # elif self.ir_data & int(0x100):
                                #     # twist.linear.x = temp_linear_vel_turn
                                #     twist.linear.x = 0
                                #     twist.angular.z = self.angular_vel
                                #     print("turn left")
                                # else:
                                #     print("cannot find recharge station")
                                #     rospy.sleep(1)
                                # self.velpub.publish(twist)

                        elif self.my_recharge_status == 2:
                            if matching_cnt < 5:
                                matching_cnt += 1
                                twist = Twist()
                                twist.linear.x = 0.05
                                twist.angular.z = 0
                                self.velpub.publish(twist)
                                rospy.loginfo("recharger is matching!!")
                            if matching_cnt < 100:
                                matching_cnt += 1
                                twist = Twist()
                                twist.linear.x = 0
                                twist.angular.z = 0
                                self.velpub.publish(twist)
                                rospy.sleep(0.1)
                            else:
                                matching_cnt = 0
                                rospy.loginfo("recharger matched fail!! back!!")
                                twist = Twist()
                                twist.linear.x = self.back_vel
                                # ta = rospy.get_time()
                                tb = rospy.get_time()
                                delta_time = 0
                                temp_time = 0
                                while ((temp_time) < self.back_time) and (not rospy.is_shutdown()):
                                    delta_time = rospy.get_time() - tb
                                    tb = rospy.get_time()
                                    if self.obstacleback is False:
                                        temp_time += delta_time
                                        self.velpub.publish(twist)
                                    # rospy.sleep(0.05)                                  
                                twist.linear.x = 0
                                twist.angular.z = 0
                                self.velpub.publish(twist)
                            # rospy.sleep(0.1)
                                

                        elif self.my_recharge_status == 3:
                            self.in_recharing = 3
                            rospy.sleep(2)
                            # rospy.loginfo("recharger matched successfully!! charging!!")

                        elif self.my_recharge_status == 5:
                            self.get_recharge_cmd = False
                            rospy.loginfo("battery is full!! back!!")
                            twist = Twist()
                            twist.linear.x = self.back_vel
                            # self.velpub.publish(twist)
                            # rospy.sleep(self.back_time)
                            # ta = rospy.get_time()
                            tb = rospy.get_time()
                            delta_time = 0
                            temp_time = 0
                            while ((temp_time) < self.back_time) and (not rospy.is_shutdown()):
                                delta_time = rospy.get_time() - tb
                                tb = rospy.get_time()
                                if self.obstacleback is False:
                                    temp_time += delta_time
                                    self.velpub.publish(twist)
                                # rospy.sleep(0.05)                                  
                            twist.linear.x = 0
                            twist.angular.z = 0
                            self.velpub.publish(twist)
                            self.recharge_pub.publish(0)

                        # if twist.linear.x != 0:
                        #     rospy.sleep(0.5)
                        # else:
                        #     rospy.sleep(1)
                        # rospy.sleep(0.2)
                        # twist.linear.x = 0
                        # twist.angular.z = 0
                        # self.velpub.publish(twist)

                if self.get_recharge_cmd is False:
                    if (self.in_recharing == 1) or (self.in_recharing == 2):
                        self.cancel_goal_pub.publish(True)
                    elif self.in_recharing == 3:
                        print("back!!")
                        twist = Twist()
                        twist.linear.x = self.back_vel
                        # self.velpub.publish(twist)
                        # rospy.sleep(self.back_time)
                        # ta = rospy.get_time()
                        tb = rospy.get_time()
                        delta_time = 0
                        temp_time = 0
                        while ((temp_time) < self.back_time) and (not rospy.is_shutdown()):
                            delta_time = rospy.get_time() - tb
                            tb = rospy.get_time()
                            if self.obstacleback is False:
                                temp_time += delta_time
                                self.velpub.publish(twist)
                            # rospy.sleep(0.05)                                  
                        twist.linear.x = 0
                        twist.angular.z = 0
                        self.velpub.publish(twist)
                    self.in_recharing = 0
                    rospy.loginfo("interupt recharging!")
            
            # self.get_recharge_cmd = False
        else:
            self.inchargingpub.publish(False)
            rospy.sleep(1)


    def shutdown(self):
        if self.get_recharge_cmd is True:
            self.cancel_goal_pub.publish(True)
            self.recharge_pub.publish(0)
        rospy.loginfo("Exit Auto Recharge")
        rospy.sleep(1)



if __name__ == '__main__':

    rospy.init_node('ob_auto_recharge', anonymous=True)
    recharger = Recharge()
    while(not rospy.is_shutdown()):
        if recharger.relocationfinish_flag is True:
            recharger.mainloop()
        
    rospy.loginfo("Exit Auto Recharge,end")
    # rospy.spin()

