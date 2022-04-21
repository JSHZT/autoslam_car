#!/usr/bin/env python

'''
Copyright (c) 2015, Mark Silliman
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
'''

# TurtleBot must have minimal.launch & amcl_demo.launch
# running prior to starting this script
# For simulation: launch gazebo world & amcl_demo prior to run this script


import rospy
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
import actionlib
from actionlib_msgs.msg import *
from geometry_msgs.msg import Pose, Point, Quaternion
from geometry_msgs.msg import Twist
from std_msgs.msg import Int16, Int32, UInt16, Float32, String, Bool
from sensor_msgs.msg import LaserScan
import math
from std_srvs.srv import Empty

from obrobot_navigation.msg import PoseDefine,PoseOperation
from obrobot_navigation.srv import *



class GoToPose():
    def __init__(self):

        self.count_rec = 0
        #global count_rec
        self.goal_sent = False

        self.obstaclefront = False
        self.obstacleback = False

        # What to do if shut down (e.g. Ctrl-C or failure)
        rospy.on_shutdown(self.shutdown)
	
	    # Tell the action client that we want to spin a thread by default
        self.move_base = actionlib.SimpleActionClient("move_base", MoveBaseAction)
        rospy.loginfo("Wait for the action server to come up")
        #rospy.Timer(rospy.Duration(1),self.CMDCallback_timer) #travis
	    # Allow up to 5 seconds for the action server to come up
        self.move_base.wait_for_server(rospy.Duration(5))

        # self.pub = rospy.Publisher('cmd_vel', Twist, queue_size = 5) 
        self.nav_finish_pub = rospy.Publisher('ob_nav_finish', Int16, queue_size = 5) #travis_debug
        self.velpub = rospy.Publisher('cmd_vel', Twist, queue_size = 5) 

        rospy.Subscriber("ob_map_goal", Pose, self.setgoal)
        rospy.Subscriber("ob_map_goal_cancel", Bool, self.cancelgoal)

        rospy.Subscriber("ob_map_goal_id", Int16, self.setgoalid)
        rospy.Subscriber("scan", LaserScan, self.laser_cb) #zark

        rospy.loginfo("......wait_for_data.....")
        rospy.sleep(3)


        # self.nav_finish_pub.publish(1)


    def laser_cb(self, data):
        cnt = 0
        #for tempi in range(270, 451):
        #    tempx = data.ranges[tempi] * math.cos(0.5 * (tempi - 360) / 180 * math.pi)
        #    if(data.ranges[tempi] > 0.08) and (data.ranges[tempi] < 0.2) :
        #        cnt += 1
        for tempi in range(0, 91):
            tempx = data.ranges[tempi] * math.cos(360.0 / 800 * tempi / 180 * math.pi)
            if(data.ranges[tempi] > 0.08) and (data.ranges[tempi] < 0.2) :
                cnt += 1
        for tempi in range(710, 800):
            tempx = data.ranges[tempi] * math.cos(360.0 / 800 * tempi / 180 * math.pi)
            if(data.ranges[tempi] > 0.08) and (data.ranges[tempi] < 0.2) :
                cnt += 1
        if(cnt != 0):
            self.obstaclefront = True
            self.obstaclefront_Cnt = 10
        else:
            if True is self.obstaclefront and self.obstaclefront_Cnt>0:
                self.obstaclefront_Cnt = self.obstaclefront_Cnt - 1
                if 0==self.obstaclefront_Cnt:
                    self.obstaclefront = False
            else:
                self.obstaclefront = False

        cnt = 0
        #for tempi in [0, 1, 2, 3, 4, 5, 714, 715, 716, 717, 718, 719]:
        for tempi in range(390, 411):
            if(data.ranges[tempi] > 0.3) and (data.ranges[tempi] < 0.45) :
                cnt += 1
        if(cnt != 0):
            self.obstacleback = True
        else:
            self.obstacleback = False

    def goto(self, pos, quat):
        # Send a goal
        self.goal_sent = True
        goal = MoveBaseGoal()
        goal.target_pose.header.frame_id = 'map'
        goal.target_pose.header.stamp = rospy.Time.now()
        goal.target_pose.pose = Pose(Point(pos['x'], pos['y'], 0.000),
                                     Quaternion(quat['r1'], quat['r2'], quat['r3'], quat['r4']))
	    
        retry_cnt = 0
        
        while retry_cnt < 3:
            retry_cnt += 1
            # Start moving
                # if retry_cnt == 2:
                #     clearcostmaps_srv = rospy.ServiceProxy('move_base/clear_costmaps', Empty)
                #     tempempty = Empty()
                #     tempresult = clearcostmaps_srv()
                #     # print(tempresult)
                #     rospy.sleep(0.5)
            self.move_base.send_goal(goal)
            # Allow TurtleBot up to 120 seconds to complete task
    #0322        success = self.move_base.wait_for_result(rospy.Duration(80)) #(40))(120))# 
    
            success = self.move_base.wait_for_result(rospy.Duration(30))#(25))#(10)) #240
            state = self.move_base.get_state()
            result = False
            rospy.loginfo("success:" + str(success) + " ; " + "state:" + str(state))
            if state == GoalStatus.SUCCEEDED:
                result = True
                break
            elif (state == GoalStatus.ABORTED) or (success == False):
                if (self.obstaclefront is True) and (self.obstacleback is False):
                    twist = Twist()
                    twist.linear.x = -0.1
                    tb = rospy.get_time()
                    delta_time = 0
                    temp_time = 0
                    while ((temp_time) < 2) and (not rospy.is_shutdown()):
                        delta_time = rospy.get_time() - tb
                        tb = rospy.get_time()
                        if self.obstacleback is False:
                            temp_time += delta_time
                            self.velpub.publish(twist)
                        rospy.sleep(0.2)                                  
                    twist.linear.x = 0
                    twist.angular.z = 0
                    self.velpub.publish(twist)
                    
            else:
                self.move_base.cancel_goal()
        self.goal_sent = False
        return result

    def cancelgoal(self, data):
        if data.data is True:
            self.move_base.cancel_goal()
            rospy.loginfo("OB robot cancel goal")

    def setgoal(self, data):
        #global count_rec
        a = data.position.x
        b = data.position.y
        c = data.position.z
        d = data.orientation.x
        e = data.orientation.y
        f = data.orientation.z
        g = data.orientation.w
        position = {'x': a, 'y' : b} 
        quaternion = {'r1' : d, 'r2' : e, 'r3' : f, 'r4' : g}
        rospy.loginfo("Go to (%s, %s) pose", a, b)
        success = self.goto(position, quaternion)
            
        # rospy.sleep(1) # zark
        if success:
            rospy.loginfo("OB robot reach goal")
            self.count_rec = 0
            #count_rec  = 0
            self.nav_finish_pub.publish(1)
        else:
            rospy.loginfo("OB robot cannot reach goal")

            self.nav_finish_pub.publish(0)

    def setgoalid(self, data):
        goalpose = Pose()
        poseoperation=PoseOperation()
        poseoperation.opt   = "select"
        poseoperation.id    = data.data
        poseoperation.floor = 1

        rospy.wait_for_service('posemanage_server')

        try:
        # if True:
            posemanage = rospy.ServiceProxy('posemanage_server', PoseManage)
            resp = posemanage(poseoperation)
            if "SUCCESS" in resp.status:
                goalpose.position.x = resp.posedefine.pose.position.x
                goalpose.position.y = resp.posedefine.pose.position.y
                goalpose.position.z = resp.posedefine.pose.position.z
                goalpose.orientation.x = resp.posedefine.pose.orientation.x
                goalpose.orientation.y = resp.posedefine.pose.orientation.y
                goalpose.orientation.z = resp.posedefine.pose.orientation.z
                goalpose.orientation.w = resp.posedefine.pose.orientation.w
                # print(resp.status)
                # print(resp.posedefine)
                self.setgoal(goalpose)
            else:
                rospy.logwarn("cannot get goal pose, id:" + str(data.data))
        except rospy.ServiceException, e:
            print "Service call failed: %s"%e
        
        
            

    def shutdown(self):
        if self.goal_sent:
            self.move_base.cancel_goal()
        # twist = Twist()
        # self.pub.publish(twist)
        rospy.loginfo("Stop")
        rospy.sleep(1)



if __name__ == '__main__':

    rospy.init_node('auto_map_nav', anonymous=True)
    navigator = GoToPose()
    rospy.spin()

