#!/usr/bin/env python

import rospy
# from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
# import actionlib
# from actionlib_msgs.msg import *
from geometry_msgs.msg import Pose, Point, Quaternion
from geometry_msgs.msg import Twist
from std_msgs.msg import Int16, Int32, UInt16, Float32, String, Bool
import tf
from obrobot_navigation.msg import PoseDefine,PoseOperation
from obrobot_navigation.srv import *



class Recharge():
    def __init__(self):

        self.recharge_pos = Pose()
        self.recharge_pos.orientation.w = 1
        rospy.on_shutdown(self.shutdown)

        self.success_flag = True
        self.finish_flag = True

        self.get_recharge_cmd = False
        self.in_recharing = 0 # 0:not recharge 1:going to recharge point 2:recharging

        rospy.Subscriber('ob_nav_finish', Int16, self.receivefinish) 

        rospy.Subscriber('ob_auto_recharge', Bool, self.obautorecharge) 
        # rospy.Subscriber("ob_rechargePose", Pose, self.updaterechargepos)
        rospy.Subscriber('ob_rechargePose_current', Bool, self.updaterechargeposcurrent) 

        self.recharge_pub = rospy.Publisher("recharge_handle", Int16, queue_size = 5)
        self.goal_pub = rospy.Publisher("ob_map_goal", Pose, queue_size = 5)
        self.cancel_goal_pub = rospy.Publisher("ob_map_goal_cancel", Bool, queue_size = 5)

        self.tflasertoodom = tf.TransformListener()

        rospy.sleep(3)

        rospy.loginfo("......wait_for_recharge_command.....")

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
            self.in_recharing = 0
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
            if self.in_recharing == 0:
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
                            if recharge_try_cnt > 5:
                                # self.get_recharge_cmd = False
                                rospy.logwarn("cannot go to recharge point!!")
                                self.in_recharing = 0
                                break
                            self.finish_flag = False
                            self.goal_pub.publish(goal)
                            rospy.loginfo("recharge_try_cnt:" + str(recharge_try_cnt))

                if self.get_recharge_cmd is False:
                    self.cancel_goal_pub.publish(True)
                    self.in_recharing = 0
                    rospy.loginfo("interupt recharging!")
            
            self.get_recharge_cmd = False
            


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
        recharger.mainloop()
    # rospy.spin()

