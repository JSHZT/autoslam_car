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
from std_msgs.msg import Int16, Int32, UInt16, Float32, String
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Odometry
import math
import numpy as np
from math import copysign, sqrt, pow
from math import sin,cos,atan2,acos,asin
import tf
from math import radians, copysign
import PyKDL
from math import pi


def quat_to_angle(quat):
    rot = PyKDL.Rotation.Quaternion(quat.x, quat.y, quat.z, quat.w)
    return rot.GetRPY()[2]
        
def normalize_angle(angle):
    res = angle
    while res > pi:
        res -= 2.0 * pi
    while res < -pi:
        res += 2.0 * pi
    return res


class GoToPose():
    def __init__(self):

        self.goal_sent = False
        # What to do if shut down (e.g. Ctrl-C or failure)
        rospy.on_shutdown(self.shutdown)
	

        #self.sub = rospy.Subscriber("car_changeposition", Point, self.setgoal)
        #self.pub = rospy.Publisher("car_changeok", Point, queue_size=5)

        self.pub = rospy.Publisher("car_move_edu_ok", Point, queue_size=5)
        self.sub = rospy.Subscriber("ob_move_edu", Pose, self.setgoal)
        
        # Publisher to control the robot's speed
        self.cmd_vel = rospy.Publisher('/cmd_vel', Twist, queue_size=5)  
        
        rospy.loginfo("......wait_for_ob_move.....")
        #rospy.sleep(3)


    def setgoal(self, data):

        # How fast will we check the odometry values?
        self.rate = rospy.get_param('~rate', 30)#20)#10)
        r = rospy.Rate(self.rate) 

        '''time_give = data.x #time
        angular_give = data.y #angular,degree
        distance_give = data.z #distance,m'''
        time_give = data.position.x
        angular_give = data.position.y
        distance_give = data.position.z * -1
        speed_move_give = data.orientation.x
        speed_tolerance_give = data.orientation.y
        speed_rotate_give = data.orientation.z
        rotate_tolerance_give = data.orientation.w

      
        # Set the distance to travel
#        self.test_distance = rospy.get_param('~test_distance', 1.0) #5.0) # meters
        self.speed_move = rospy.get_param('~speed_move', speed_move_give)#0.18) #0.25) # meters per second
        self.speed_tolerance = rospy.get_param('~speed_tolerance', speed_tolerance_give)#0.01) #0.015) # meters #0.01
        self.odom_linear_scale_correction = rospy.get_param('~odom_linear_scale_correction', 1.0)
#        self.start_test = rospy.get_param('~start_test', True)

        # The test angle is 360 degrees
#        self.test_angle = radians(rospy.get_param('~test_angle', 360.0))

#        self.speed_rotate = rospy.get_param('~speed_rotate', speed_rotate_give)#0.02) #0.15)#0.3) #0.05 radians per second
        self.speed_rotate = rospy.get_param('~speed_rotate', speed_rotate_give)#0.3) #0.02) #0.15)0.05 radians per second

#        self.rotate_tolerance = radians(rospy.get_param('~rotate_tolerance', 2.0))#3)) # degrees converted to radians 
        self.rotate_tolerance = radians(rospy.get_param('~rotate_tolerance', rotate_tolerance_give))#3)) # degrees converted to radians 


#1degree
        self.odom_angular_scale_correction = rospy.get_param('~odom_angular_scale_correction', 1.0)
#        self.start_test = rospy.get_param('~start_test', True)

        
       
        # The base frame is base_footprint for the TurtleBot but base_link for Pi Robot
        self.base_frame = rospy.get_param('~base_frame', '/base_footprint')
        # The odom frame is usually just /odom
        self.odom_frame = rospy.get_param('~odom_frame', '/odom')
        # Initialize the tf listener
        self.tf_listener = tf.TransformListener()        
        # Give tf some time to fill its buffer
        rospy.sleep(2)        
        # Make sure we see the odom and base frames
        self.tf_listener.waitForTransform(self.odom_frame, self.base_frame, rospy.Time(), rospy.Duration(60.0))        


        rospy.loginfo("------------- New Goal --------------")
        self.odom_angle = self.get_odom_angle() #rad
        self.current_yaw = self.odom_angle
        self.current_yaw_deg = self.current_yaw*180.0/3.141593 #degree
        self.position = Point()        
        self.position = self.get_position()        
        self.current_x = self.position.x
        self.current_y = self.position.y
        rospy.loginfo("current_x=" + str(self.current_x) + ","+ "current_y=" + str(self.current_y) + ","+ "current_yaw_deg=" + str(self.current_yaw_deg))



        '''time_give = data.x #time
        angular_give = data.y #angular,degree
        distance_give = data.z #distance,m'''

        rospy.loginfo("time_give=" + str(time_give) + ","+ "angular_give=" + str(angular_give) + ","+ "distance_give=" + str(distance_give))


        rotate_angular1 = angular_give

        move_distance = distance_give
        if (distance_give>0):
            fangxiang = -1
            move_distance = distance_give

        if (distance_give<0):
            fangxiang = 1
            move_distance = -1 * distance_give



        rospy.loginfo("rotate_angular1=" + str(rotate_angular1)+ ","+ "rotate_speed=" + str(self.speed_rotate))        
        self.test_angle = radians(rospy.get_param('~test_angle', rotate_angular1))#45))#360.0))
        self.start_test = rospy.get_param('~start_test', True)
        reverse = 1        
        while not rospy.is_shutdown():
            if (self.start_test):# and rotate_angular1!=0):
                # Get the current rotation angle from tf
                self.odom_angle = self.get_odom_angle()                
                last_angle = self.odom_angle
                turn_angle = 0
                self.test_angle *= reverse
                error = self.test_angle - turn_angle                                
                # Alternate directions between tests
                reverse = -reverse                
                while abs(error) > self.rotate_tolerance and self.start_test:
                    if rospy.is_shutdown():
                        return                    
                    # Rotate the robot to reduce the error
                    move_cmd = Twist()
                    move_cmd.angular.z = copysign(self.speed_rotate, error)
                    self.cmd_vel.publish(move_cmd)
                    r.sleep()                 
                    # Get the current rotation angle from tf                   
                    self.odom_angle = self.get_odom_angle()                    
                    # Compute how far we have gone since the last measurement
                    delta_angle = self.odom_angular_scale_correction * normalize_angle(self.odom_angle - last_angle)
                    
                    # Add to our total angle so far
                    turn_angle += delta_angle
                    # Compute the new error
                    error = self.test_angle - turn_angle
                    # Store the current angle for the next comparison
                    last_angle = self.odom_angle                                    
                # Stop the robot
                self.cmd_vel.publish(Twist())                
                # Update the status flag
                self.start_test = False
                params = {'start_test': False}

                rospy.loginfo("action in rotate") #travis
                break #travis
                
            rospy.sleep(0.5)                    
        # Stop the robot
        self.cmd_vel.publish(Twist())

        rospy.sleep(0.1)
            
        #rospy.loginfo("move distance")
        rospy.loginfo("move_distance=" + str(move_distance)+ ","+ "move_speed=" + str(self.speed_move))        
        self.test_distance = rospy.get_param('~test_distance', move_distance) #5.0) # meters 
        self.start_test = rospy.get_param('~start_test', True) #travis
        self.position = Point()        
        # Get the starting position from the tf transform between the odom and base frames
        self.position = self.get_position()        
        x_start = self.position.x
        y_start = self.position.y            
        move_cmd = Twist()            
        while not rospy.is_shutdown():
            # Stop the robot by default
            move_cmd = Twist()            
            if (self.start_test):# and move_distance!=0):
                # Get the current position from the tf transform between the odom and base frames
                self.position = self.get_position()                
                # Compute the Euclidean distance from the target point
                distance = sqrt(pow((self.position.x - x_start), 2) +
                                pow((self.position.y - y_start), 2))                                
                # Correct the estimated distance by the correction factor
                distance *= self.odom_linear_scale_correction                
                # How close are we?
                error =  distance - self.test_distance                
                # Are we close enough?
                if not self.start_test or abs(error) <  self.speed_tolerance:
                    self.start_test = False
                    params = {'start_test': False}
                    #rospy.loginfo(params)

                    rospy.loginfo("action in move") #travis
                    break #travis
 
                else:
                    # If not, move in the appropriate direction
                    move_cmd.linear.x = fangxiang * copysign(self.speed_move, -1 * error)
            else:
                self.position = self.get_position()
                x_start = self.position.x
                y_start = self.position.y                
            self.cmd_vel.publish(move_cmd)
            r.sleep()
        # Stop the robot
        self.cmd_vel.publish(Twist())

        #rospy.sleep(1)
        point = Point()
        point.x = 1 #time
        point.y = 1 #
        point.z = 0 #
        print("car_move_edu_ok..........11")
        self.pub.publish(point)


        '''rospy.sleep(2)

        rospy.loginfo("rotate_angular2=" + str(rotate_angular2)+ ","+ "rotate_speed=" + str(self.speed_rotate))        
        self.test_angle = radians(rospy.get_param('~test_angle', rotate_angular2))#-3))#360.0))
        self.start_test = rospy.get_param('~start_test', True) #travis        
        reverse = 1        
        while not rospy.is_shutdown():
            if self.start_test:
                # Get the current rotation angle from tf
                self.odom_angle = self.get_odom_angle()                
                last_angle = self.odom_angle
                turn_angle = 0
                self.test_angle *= reverse
                error = self.test_angle - turn_angle                                
                # Alternate directions between tests
                reverse = -reverse                
                while abs(error) > self.rotate_tolerance and self.start_test:
                    if rospy.is_shutdown():
                        return                    
                    # Rotate the robot to reduce the error
                    move_cmd = Twist()
                    move_cmd.angular.z = copysign(self.speed_rotate, error)
                    self.cmd_vel.publish(move_cmd)
                    r.sleep()                 
                    # Get the current rotation angle from tf                   
                    self.odom_angle = self.get_odom_angle()                    
                    # Compute how far we have gone since the last measurement
                    delta_angle = self.odom_angular_scale_correction * normalize_angle(self.odom_angle - last_angle)
                    
                    # Add to our total angle so far
                    turn_angle += delta_angle
                    # Compute the new error
                    error = self.test_angle - turn_angle
                    # Store the current angle for the next comparison
                    last_angle = self.odom_angle                                    
                # Stop the robot
                self.cmd_vel.publish(Twist())                
                # Update the status flag
                self.start_test = False
                params = {'start_test': False}

                rospy.loginfo("action in rotate") #travis
                break #travis
                
            rospy.sleep(0.5)                    
        # Stop the robot
        self.cmd_vel.publish(Twist())'''

        
    def get_odom_angle(self):
        # Get the current transform between the odom and base frames
        try:
            (trans, rot)  = self.tf_listener.lookupTransform(self.odom_frame, self.base_frame, rospy.Time(0))
        except (tf.Exception, tf.ConnectivityException, tf.LookupException):
            rospy.loginfo("TF Exception")
            return        
        # Convert the rotation from a quaternion to an Euler angle
        return quat_to_angle(Quaternion(*rot))


    def get_position(self):
        # Get the current transform between the odom and base frames
        try:
            (trans, rot)  = self.tf_listener.lookupTransform(self.odom_frame, self.base_frame, rospy.Time(0))
        except (tf.Exception, tf.ConnectivityException, tf.LookupException):
            rospy.loginfo("TF Exception")
            return
        return Point(*trans)

        
    def shutdown(self):
        # Always stop the robot when shutting down the node
        rospy.loginfo("Stopping the robot...")
        #self.cmd_vel.publish(Twist())
        move_cmd = Twist()
        self.cmd_vel.publish(move_cmd)
        rospy.sleep(1)




if __name__ == '__main__':

    rospy.init_node('ob_move_edu_node', anonymous=True)
    navigator = GoToPose()
    rospy.spin()

