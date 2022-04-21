#!/usr/bin/env python2

import rospy
from geometry_msgs.msg import PoseStamped
from std_msgs.msg import Int16, Bool

class TOD(object):

    def __init__(self):

        self.finish_flag = True
        self.success_flag = True
        goal_id = 0
        self.relocationfinish_flag = False
        self.incharging_flag = False

        self.goal_id_pub = rospy.Publisher("ob_map_goal_id", Int16, queue_size = 5)

        rospy.Subscriber("ob_nav_finish", Int16, self.handle_callback)
        rospy.Subscriber("/ob_relocation_finish", Bool, self.relocationfinish_callback)
        rospy.Subscriber('ob_in_charging', Bool, self.incharging_cb) 

        rospy.sleep(3)

        time_last = rospy.get_time()
        try_cnt = 0

        while not rospy.is_shutdown():
            rospy.sleep(0.5)
            if (self.relocationfinish_flag is True) and (self.incharging_flag is False):
                time_now = rospy.get_time()
                if(self.finish_flag is True) or (time_now - time_last > 60):
                    if(time_now - time_last > 60):
                        rospy.loginfo("time out")
                    rospy.sleep(3)
                    time_last = rospy.get_time()
                    self.finish_flag = False
                    if(self.success_flag is True):
                        self.success_flag = False
                        try_cnt = 0
                        goal_id += 1
                        # if(goal_id == 4):
                        #     goal_id = 0
                        if(goal_id == 4):
                            goal_id = 1304
                        if(goal_id == 1305):
                            goal_id = 0
                    else:
                        try_cnt += 1
                        if try_cnt > 5:
                            try_cnt = 0
                            goal_id += 1
                            # if(goal_id == 4):
                            #     goal_id = 0
                            if(goal_id == 4):
                                goal_id = 1304
                            if(goal_id == 1305):
                                goal_id = 0
                    self.goal_id_pub.publish(goal_id)
                    rospy.loginfo("goal: id:" + str(goal_id))
                    time_last = rospy.get_time()
            else:
                time_last = rospy.get_time()
            
    def incharging_cb(self, data):
        if(data.data is True):
            self.incharging_flag = True
        else:
            self.incharging_flag = False
        
    def relocationfinish_callback(self, data):
        if(data.data is True):
            self.relocationfinish_flag = True

    def handle_callback(self,data):
        self.finish_flag = True
        if data.data == 1:
            self.success_flag = True
        elif data.data == 0:
            self.success_flag = False

  

  
if __name__ == "__main__":

    rospy.init_node("auto_map_find_goal",anonymous=True)
    tod = TOD()
    while(not rospy.is_shutdown()):
        if tod.auto_slam_finish is False:
            tod.mainloop()
        else:
            break
    # rospy.spin()

    
